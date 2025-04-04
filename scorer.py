"""
scorer.py

Ranks articles based on keyword relevance + risk matrix model.


"""

import os

# Keyword weights per category
KEYWORD_WEIGHTS = {
    'org_tech': 10,                # Directly used technologies (e.g., CrowdStrike, Azure)
    'ics_keywords': 9,             # ICS/OT/SCADA targets (critical infrastructure)
    'business_partners': 10,       # Third-party vendors with potential exposure
    'threat_intel': 6,             # General threat activity (malware, phishing, etc.)
    'exploit_keywords': 6,         # PoC terms, exploit language
    'trusted_sources': 3,          # Signals higher confidence in source
    'low_priority': -5,            # Low-signal/noisy terms to suppress
    'geo_keywords': 4,             # Targeted geographic regions (e.g., “Australia”)
    'threat_actor_keywords': 7,    # Known threat actor names (APT29, FIN7)
    'severity_keywords': 8,        # Keywords like "critical", "widespread"
    'ttp_keywords': 7,             # Novel techniques (BYOVD, sideloading)
    'crown_jewel_keywords': 9      # High-value targets (AD, SAP, VPNs, IAM)
}

# File paths (you can customize this later to pull from config.yaml)
KEYWORD_FILES = {
    'org_tech': 'Keywords/Private/org_tech_keywords.txt',
    'ics_keywords': 'Keywords/Public/ics_oilandgas_keywords.txt',
    'business_partners': 'Keywords/Private/business_partner_keywords.txt',
    'threat_intel': 'Keywords/Public/threat_intel_keywords.txt',
    'exploit_keywords': 'Keywords/Public/exploit_keywords.txt',
    'trusted_sources': 'Keywords/Public/trusted_sources.txt',
    'low_priority': 'Keywords/Public/low_priority_keywords.txt',
    'geo_keywords': 'Keywords/Private/geo_keywords.txt',
    'threat_actor_keywords': 'Keywords/Public/threat_actor_keywords.txt',
    'severity_keywords': 'Keywords/Public/severity_keywords.txt',
    'ttp_keywords': 'Keywords/Public/ttp_keywords.txt',
    'crown_jewel_keywords': 'Keywords/Private/crown_jewel_keywords.txt'
}

def load_keywords(filepath):
    """Loads a list of keywords from a text file, lowercased."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return [line.strip().lower() for line in f if line.strip()]

def score_article(article, keyword_dict):
    """
    Scores a single article using keyword categories + risk matrix.

    Returns:
        score, risk_score, breakdown dict
    """
    score = 0
    text = (article['title'] + ' ' + article['summary']).lower()
    source = article.get('source', '').lower()
    breakdown = {}

    # Match keywords and apply weights
    for category, keywords in keyword_dict.items():
        matches = [kw for kw in keywords if kw in text]
        if matches:
            if category == 'trusted_sources' and any(s in source for s in keywords):
                score += KEYWORD_WEIGHTS[category]
                breakdown[category] = ['SOURCE MATCH']
            elif category != 'trusted_sources':
                score += KEYWORD_WEIGHTS[category]
                breakdown[category] = matches

    
    # Ransomware override: if a ransomware feed AND partner mentioned → force critical
    if article.get('source_type') == 'ransomware' and 'business_partners' in breakdown:
        score = 100
        article['critical'] = True
        breakdown['ransom_override'] = True
    
    # Risk Matrix Mapping
    impact = 1  # default
    if 'business_partners' in breakdown:
        impact = 2
    if 'ics_keywords' in breakdown:
        impact = max(impact, 2)
    if 'org_tech' in breakdown:
        impact = 3
    if 'ics_keywords' in breakdown and 'threat_actor_keywords' in breakdown:
        impact = max(impact, 4)

    likelihood = 1
    if 'exploit_keywords' in breakdown:
        likelihood = 2
    if 'threat_intel' in breakdown:
        likelihood = max(likelihood, 2)
    if 'trusted_sources' in breakdown:
        likelihood = 3


    risk_score = impact * likelihood
    final_rank = score + (risk_score * 2)

    return score, risk_score, final_rank, breakdown

def score_articles(articles):
    """
    Scores and sorts articles by final_rank (score + 2*risk).

    Returns:
        List[dict]: articles with score, risk_score, breakdown
    """
    # Load all keyword lists
    keyword_dict = {
        cat: load_keywords(path)
        for cat, path in KEYWORD_FILES.items()
    }

    for article in articles:
        score, risk_score, final_rank, breakdown = score_article(article, keyword_dict)
        article['score'] = score
        article['risk_score'] = risk_score
        article['final_rank'] = final_rank
        article['score_breakdown'] = breakdown

    return sorted(articles, key=lambda a: a['final_rank'], reverse=True)
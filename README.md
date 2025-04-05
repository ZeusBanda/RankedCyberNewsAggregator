# RankedCyberNewsAggregator (RCNA)
*A Python tool for aggregating and scoring cybersecurity news and threat intelligence — tailored for operational relevance.*

RCNA was built out of necessity: trying to cut through the noise and quickly figure out which cyber stories actually matter.  
Its scoring engine prioritizes articles based on custom keywords, threat relevance, and context — so you can focus on what’s high-impact, not just what’s trending.

Originally tuned for ICS/OT environments, it’s flexible enough to support any niche or industry.

## Why This Tool Matters

Threat feeds are noisy. Headlines rarely align with what your organization *actually* cares about. RCNA helps you cut through the noise and prioritize the signal.

With minor edits to the keyword lists, this tool can be adapted to **any industry or sector**. By default, it’s tuned for ICS/OT environments in oil and gas, but it can just as easily be used in finance, healthcare, education, or tech.

Like all good threat intelligence work, this tool gets stronger the better you understand your organization.

---

## How It Works

1. **Scrapes recent articles** from curated RSS and intel feeds
2. **Scores** each article based on keyword matches and a risk matrix
3. **Sorts** articles by relevance and saves a clean `.txt` daily digest

No API keys. No external servers. No EULA violations.  
Just Python + YAML + common sense.

---

## Keyword Files

Keywords drive the prioritization logic. They’re divided into logical categories:

| File Name                     | Purpose |
|------------------------------|---------|
| `org_tech_keywords.txt`       | Technologies in use at your organization (e.g., Azure, Fortinet) |
| `ics_keywords.txt`            | ICS/OT terms like PLCs, SCADA, and industrial protocols |
| `business_partner_keywords.txt`| Vendors, cloud providers, or third parties your org depends on |
| `threat_intel_keywords.txt`   | Indicators of malware, C2s, and general threat activity |
| `exploit_keywords.txt`        | Mentions of exploits, PoCs, CVEs, and attack chains |
| `geo_keywords.txt`            | Country or region references relevant to your org |
| `threat_actor_keywords.txt`   | APT groups, ransomware gangs, or ICS-targeting actors |
| `severity_keywords.txt`       | “Widespread,” “critical,” “emergency patch,” etc. |
| `ttp_keywords.txt`            | Novel techniques like DLL sideloading, BYOVD |
| `crown_jewel_keywords.txt`    | AD, SAP, VPNs, and other high-value assets |
| `low_priority_keywords.txt`   | Suppresses noisy topics like training, awareness weeks |
| `trusted_sources.txt`         | Boosts confidence in sources like CISA, Microsoft, Unit42 |
*** The information in these files was generated using OpenAI***


---

## Script Flow
rcna.py → scraper.py → scorer.py → Output/

1. `rcna.py` = main controller (run this script)
2. `scraper.py` = pulls and filters articles from RSS feeds
3. `scorer.py` = assigns scores using keyword matches and risk logic
4. Output saved as timestamped `.txt` file in `/Output`

---

## Virtual Environment Setup

Use a Python virtual environment named `.RCNA` to isolate dependencies.

### macOS/Linux:
```bash
python3 -m venv .RCNA
source .RCNA/bin/activate
```

### Windows
```cmd
python -m venv .RCNA
.RCNA\Scripts\activate
```

#### Activate the virtual environme
Once activated, your terminal will show something like:
```bash
(.RCNA) your-user@your-machine %
```

## Running the tool
```bash
(.RCNA) your-user@your-machine % python rcna.py
```

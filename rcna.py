# rcna.py
# This is the controller script for RankedCyberNewsAggregator.
# It pulls, scores, and outputs articles for the past 24 hours by default.

from scraper import get_articles
from scorer import score_articles
from datetime import datetime
import os

def print_and_save_articles(articles, hours_lookback, save_to_file):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')  # For human readability
    filename = f"Output/{timestamp} - Cyber Intel Digest.txt"

    lines = []
    lines.append("=" * 60)
    lines.append("===== RankedCyberNewsAggregator - Daily Intel Report =====")
    lines.append(f"Generated: {timestamp} | Filter: Last {hours_lookback} Hours")
    lines.append("=" * 60)

    for article in articles:
        lines.append("")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Title         : {article['title']}")
        lines.append(f"Source        : {article['source']}")
        lines.append(f"Published     : {article['published']}")
        lines.append(f"Link          : {article['link']}")
        lines.append(f"Final Score   : {article['final_rank']}")
        # lines.append(f"Risk Score    : {article['risk_score']}")
        # lines.append(f"Score         : {article['score']}")
        # lines.append(f"Breakdown     : {article['score_breakdown']}")
        summary = article['summary'].strip().replace('\n', ' ')
        lines.append(f"Summary       : {summary[:300]}{'...' if len(summary) > 300 else ''}")
        lines.append("")

    full_output = "\n".join(lines)

    # Uncomment this block below if you want to preview the output in the terminal
    
    """
    print(full_output)
    """

    if save_to_file:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_output)
        print(f"\n📁 Report saved to: {filename}")

if __name__ == "__main__":
    print("🚀 RCNA: Script is running...")

    # Default time window — override later via CLI or config
    # Change this line to change the lookback time in hours
    HOURS_LOOKBACK = 24

    # Default Output Saved to txt file - Can print to terminal
    SAVE_TO_FILES=True

    # Step 1: Load recent articles
    articles = get_articles(HOURS_LOOKBACK)
    #articles = get_articles()
    # Step 2: Score and sort them
    ranked_articles = score_articles(articles)

    # Step 3: Write formatted report
    print_and_save_articles(ranked_articles, HOURS_LOOKBACK, SAVE_TO_FILES)

    print("✅ RCNA: Done.")
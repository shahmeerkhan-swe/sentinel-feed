import os 
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.rss import scrape_hacker_news, scrape_techcrunch, scrape_reddit
from app.crud.article import save_articles

def main():

    all_articles = []

    try: 
        hn_articles = scrape_hacker_news()
        all_articles.extend(hn_articles)
        print(f"[✓] Hacker News scraped ({len(hn_articles)} articles)")
    except Exception as e: 
        print(f"[!] Hacker News failed: {e}")

    try: 
        tc_articles = scrape_techcrunch()
        all_articles.extend(tc_articles)
        print(f"[✓] TechCrunch scraped ({len(tc_articles)} articles)")
    except Exception as e: 
        print(f"[!] TechCrunch failed: {e}")

    try: 
        reddit_articles = scrape_reddit("technology", limit=10)
        all_articles.extend(reddit_articles)
        print(f"[✓] Reddit scraped ({len(reddit_articles)})")
    except Exception as e: 
        print(f"[!] Reddit failed: {e}")

    save_articles(all_articles)
    print(f"[✓] {len(all_articles)} total articles saved.")

if __name__ == "__main__": 
    main()
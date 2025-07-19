import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.email import get_articles_since_yesterday, send_email_digest

if __name__ == "__main__":
    articles = get_articles_since_yesterday()
    send_email_digest(articles)
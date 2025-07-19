import os 
from datetime import datetime, timedelta
from dotenv import load_dotenv 
from app.database import SessionLocal
from app.models.article import Article
import yagmail

load_dotenv()

def get_articles_since_yesterday():
    db = SessionLocal()
    since = datetime.now() - timedelta(days=1)
    articles = db.query(Article).filter(Article.scraped_at >= since).all()
    db.close()
    return articles

def send_email_digest(articles):
    if not articles: 
        print("[i] No new articles to send.")
        return
    
    sender = os.getenv("EMAIL_USER")
    receiver = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_PASSWORD")

    yag = yagmail.SMTP(user=sender, password=password)

    subject = f"📰 Sentinel Feed Digest - {datetime.now().strftime('%Y-%m-%d')}"
    body = ""
    body += "Here are your top articles scraped in the last 24 hours:\n\n"

    for art in articles:
        body += f"🔹 [{art.source}] {art.title}\n{art.url}\n\n"

    yag.send(to=receiver, subject=subject, contents=body)
    print(f"[✓] Digest sent to {receiver} with {len(articles)} articles.")
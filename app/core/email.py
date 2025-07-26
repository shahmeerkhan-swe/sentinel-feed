import os 
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from dotenv import load_dotenv 
from app.database import SessionLocal
from app.models.article import Article
from jinja2 import Environment, FileSystemLoader, select_autoescape 

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
    
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('digest.html.j2')
    html_content = template.render(articles=articles, now=datetime.now())
    
    sender = os.getenv("EMAIL_USER")
    receiver = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_host = os.getenv("EMAIL_HOST", "sandbox.smtp.mailtrap.io")
    smtp_port = int(os.getenv("EMAIL_PORT", 2525))

    msg = EmailMessage()
    msg['Subject'] = f"📰 Sentinel Feed Digest - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content("Your email client does not support HTML.")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP(smtp_host, smtp_port) as server: 
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        print(f"[✓] Digest sent to {receiver} with {len(articles)} articles.")
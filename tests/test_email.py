import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def test_render_email_digest():
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'app', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('digest.html.j2')

    # Dummy articles
    articles = [{
        "title": "Test Article",
        "url": "https://example.com",
        "summary": "This is a test summary",
        "source": "TechCrunch"
    }]

    rendered = template.render(articles=articles, now=datetime.now())

    assert "<html" in rendered
    assert "Test Article" in rendered
    assert "https://example.com" in rendered
    assert "This is a test summary" in rendered

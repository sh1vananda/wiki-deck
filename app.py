from flask import Flask, render_template, session, request
import requests
import time
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-truly-final-and-robust-secret-key'

def get_article_by_title(title):
    if not title: return get_random_article()
    encoded_title = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
    try:
        response = requests.get(url, headers={'User-Agent': 'HTMX-Example-App/1.0'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException: return {"title": title, "extract": "Could not re-fetch this article.", "thumbnail": None, "content_urls": {"desktop": {"page": "#"}}}

def get_random_article():
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    try:
        response = requests.get(url, headers={'User-Agent': 'HTMX-Example-App/1.0'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException: return {"title": "Error", "extract": "Could not fetch an article.", "thumbnail": None, "content_urls": {"desktop": {"page": "#"}}}

@app.route("/")
def index():
    first_article = get_random_article()
    session['history_titles'] = [first_article.get('title')]
    session['current_index'] = 0
    return render_template("index.html", article=first_article, is_first=True)

@app.route("/navigate")
def navigate():
    direction = request.args.get('direction', 'next')
    history = session.get('history_titles', [])
    current_index = session.get('current_index', 0)
    article_to_show = None

    if direction == 'next':
        current_index += 1
        if current_index < len(history):
            title_to_show = history[current_index]
            article_to_show = get_article_by_title(title_to_show)
        else:
            article_to_show = get_random_article()
            history.append(article_to_show.get('title'))
    elif direction == 'previous' and current_index > 0:
        current_index -= 1
        title_to_show = history[current_index]
        article_to_show = get_article_by_title(title_to_show)
    else:
        current_index = 0
        article_to_show = get_article_by_title(history[0]) if history else get_random_article()
    
    session['history_titles'] = history
    session['current_index'] = current_index
    session.modified = True
    
    is_now_first = (current_index == 0)
    time.sleep(0.2)
    
    return render_template("_slide_and_controls.html", article=article_to_show, is_first=is_now_first)

if __name__ == "__main__":
    app.run(debug=True)
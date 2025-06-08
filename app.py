from flask import Flask, render_template, session
import requests
import time
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-super-secret-key-that-you-should-change-for-good'

def get_article_by_title(title):
    if not title: return get_random_article()
    encoded_title = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
    try:
        response = requests.get(url, headers={'User-Agent': 'HTMX-Example-App/1.0'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"!!! WIKIPEDIA API ERROR (by title): {e}")
        return {"title": title, "extract": "Could not re-fetch this article.", "thumbnail": None, "content_urls": {"desktop": {"page": "#"}}}

def get_random_article():
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    try:
        response = requests.get(url, headers={'User-Agent': 'HTMX-Example-App/1.0'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"!!! WIKIPEDIA API ERROR (random): {e}")
        return {"title": "Error", "extract": "Could not fetch an article.", "thumbnail": None, "content_urls": {"desktop": {"page": "#"}}}

@app.route("/")
def index():
    print("--- ROUTE: / (index) | Resetting session ---")
    first_article = get_random_article()
    session['history_titles'] = [first_article.get('title')]
    session['current_index'] = 0
    return render_template("index.html", article=first_article, is_first=True)

@app.route("/navigate")
def navigate():
    direction = request.args.get('direction', 'next')
    print(f"--- ROUTE: /navigate | Direction: {direction} ---")

    history = session.get('history_titles', [])
    current_index = session.get('current_index', 0)

    article_to_show = None

    if direction == 'next':
        if current_index < len(history) - 1:
            current_index += 1
            print(f"--- Navigating forward in history to index {current_index} ---")
            title_to_show = history[current_index]
            article_to_show = get_article_by_title(title_to_show)
        else:
            print("--- At end of history, fetching new random article ---")
            article_to_show = get_random_article()
            history.append(article_to_show.get('title'))
            current_index += 1 

    elif direction == 'previous':
        if current_index > 0:
            current_index -= 1
            print(f"--- Navigating back in history to index {current_index} ---")
        title_to_show = history[current_index]
        article_to_show = get_article_by_title(title_to_show)

    session['history_titles'] = history
    session['current_index'] = current_index
    session.modified = True
    
    is_now_first = (current_index == 0)

    time.sleep(0.2)
    
    return render_template("_slide_and_controls.html", article=article_to_show, is_first=is_now_first)

from flask import request

if __name__ == "__main__":
    app.run(debug=True)
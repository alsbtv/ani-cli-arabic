from flask import Flask, jsonify
from src.api import AnimeAPI
import traceback

app = Flask(__name__)
scraper = AnimeAPI()

@app.route('/latest')
def latest():
    try:
        episodes = scraper.get_latest_episodes(limit=20)
        if not episodes:
            # تشخيص: إذا لم يجد حلقات، نطبع حالة الاتصال وكود الصفحة
            s = scraper._get_session()
            r = s.get("https://anime3rb.com", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            return jsonify({
                "error": "No episodes found.",
                "status_code": r.status_code,
                "html_snippet": r.text[:1500] if r.status_code == 200 else "Failed to load",
                "url_requested": r.url
            })
        
        results = []
        for ep in episodes:
            results.append({
                "title": ep["title"],
                "poster": ep["thumbnail"],
                "url": ep["slug"], 
                "episode": ep["ep_num"]
            })
        return jsonify(results)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
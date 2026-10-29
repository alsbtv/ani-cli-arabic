from flask import Flask, jsonify, request
from src.api import AnimeAPI

app = Flask(__name__)
scraper = AnimeAPI()

@app.route('/latest')
def latest():
    try:
        episodes = scraper.get_latest_episodes(limit=20)
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
        return jsonify({"error": str(e)}), 500

@app.route('/stream/<slug>/<int:ep_num>')
def stream(slug, ep_num):
    try:
        servers = scraper.get_streaming_servers(slug, str(ep_num))
        if servers:
            qualities = [q.__dict__ for q in servers.get("Qualities", [])]
            return jsonify({
                "qualities": qualities, 
                "direct": servers.get("DirectStreams", {})
            })
        return jsonify({"error": "No streams found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
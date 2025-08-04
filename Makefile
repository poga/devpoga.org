up:
	git add . && git commit -m "update" && git push

rss:
	uv run generate_rss.py

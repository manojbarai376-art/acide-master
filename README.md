## Render deployment

Run the web app and scraper as separate Render services so Gunicorn worker
restarts cannot stop scraping or start duplicate scrape loops.

1. Create a Render PostgreSQL database and a Web Service from this repository.
2. Set the Web Service build command to `pip install -r requirements.txt` and
	the start command to `gunicorn --workers 2 --bind 0.0.0.0:$PORT main:app`.
3. Create a Background Worker from the same repository. Use the same build
	command and set its start command to `python -m scraper.scheduler`.
4. Set `DATABASE_URL` on both services to the database's internal connection
	string. Both services must be in a region that can reach that database.
5. Optionally set `SCRAPE_INTERVAL_SECONDS` on the worker; it defaults to 600.

The worker scrapes immediately on startup and then repeats on the configured
interval. The web app reads the same PostgreSQL records, so updates are visible
without redeploying and are not tied to Render's ephemeral application disk.
On first connection to an empty database, the bundled `database/storage.json`
dataset is imported automatically so the site has content before its first
successful scrape.
If `DATABASE_URL` is not set, the app uses `database/storage.json` for local
development; that file is not durable storage on Render.

The scraper logs failed HTTP responses and keeps the last successful dataset.
Cloudflare or other upstream access controls can still reject requests; no
client-side scraper can guarantee access when the source blocks the host.

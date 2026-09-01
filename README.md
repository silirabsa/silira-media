# SILIRA Media

A small FastAPI web app for searching Pexels photos and videos for SILIRA projects.

## Run locally

1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Put your Pexels API key in `.env` as `PEXELS_API_KEY=...`.
5. Start the app:

```bash
uvicorn app.main:app --reload
```

6. Open `http://127.0.0.1:8000`.

Never commit `.env` or expose your Pexels API key in frontend code.

Pexels requires a prominent link back to Pexels and recommends photographer attribution when possible.

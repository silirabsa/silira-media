import os

from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .pexels import search_photos, search_videos

load_dotenv()

app = FastAPI(title="SILIRA Media", version="0.1.0")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/search")
async def search(
    q: str = Query(..., min_length=1, max_length=200),
    media_type: str = Query("photo", pattern="^(photo|video)$"),
    page: int = Query(1, ge=1, le=1000),
):
    query = " ".join(q.split())
    try:
        data = await (search_photos(query, page) if media_type == "photo" else search_videos(query, page))
    except RuntimeError as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)
    except Exception:
        return JSONResponse({"error": "Pexels search failed. Check your API key and try again."}, status_code=502)

    if media_type == "photo":
        results = [
            {
                "id": item["id"],
                "type": "photo",
                "title": item.get("alt") or "Pexels photo",
                "creator": item.get("photographer") or "Unknown photographer",
                "creator_url": item.get("photographer_url"),
                "preview": item.get("src", {}).get("medium") or item.get("src", {}).get("large"),
                "media_url": item.get("src", {}).get("original"),
                "pexels_url": item.get("url"),
            }
            for item in data.get("photos", [])
        ]
    else:
        results = []
        for item in data.get("videos", []):
            files = item.get("video_files", [])
            files = sorted(files, key=lambda f: (f.get("width") or 0) * (f.get("height") or 0), reverse=True)
            best_file = files[0] if files else {}
            results.append(
                {
                    "id": item["id"],
                    "type": "video",
                    "title": "Pexels video",
                    "creator": item.get("user", {}).get("name") or "Unknown creator",
                    "creator_url": item.get("user", {}).get("url"),
                    "preview": item.get("image"),
                    "media_url": best_file.get("link"),
                    "pexels_url": item.get("url"),
                }
            )

    return {
        "query": query,
        "media_type": media_type,
        "page": data.get("page", page),
        "per_page": data.get("per_page", len(results)),
        "total_results": data.get("total_results", 0),
        "results": results,
    }


@app.get("/health")
async def health():
    return {"status": "ok", "pexels_key_configured": bool(os.getenv("PEXELS_API_KEY"))}

import sys
import io
import uvicorn

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

if __name__ == "__main__":
    print("=" * 60)
    print(">> Starting Lumea Python FastAPI Backend Server...")
    print(">> Local API URL:    http://127.0.0.1:8000")
    print(">> Interactive Docs: http://127.0.0.1:8000/docs")
    print(">> ReDoc Docs:       http://127.0.0.1:8000/redoc")
    print(">> Vue Frontend:     http://localhost:5173")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

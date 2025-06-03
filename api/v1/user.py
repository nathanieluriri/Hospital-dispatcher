
from fastapi import APIRouter, HTTPException,Depends, Body
router = APIRouter()

@router.get("/username")
def check_username(username: str, request: Request):
    bloom = request.app.state.bloom_filter

    if username in bloom:
        # Might exist, check DB to be sure
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM user WHERE username = ?", (username,))
        exists = cursor.fetchone() is not None
        conn.close()
        return {"exists": exists, "maybe": True}
    else:
        # Definitely does not exist
        return {"exists": False, "maybe": False}

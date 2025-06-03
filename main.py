from fastapi import FastAPI,Depends,Request
from security.auth import verify_admin_token,verify_user_token
# from api.v1 import 
from fastapi.middleware.cors import CORSMiddleware
from pybloom_live import BloomFilter
import sqlite3


DB_PATH = "db.db"
app = FastAPI(title="Hospital FastAPI Backend",summary="""Backend for the "Mie Novel-app", providing RESTful endpoints to manage users, novel content (books, chapters, pages), bookmarks, and likes. Features JWT-based authentication supporting both traditional credentials and Google sign-in, including token refresh capabilities.""")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
    
    


BLOOM_CAPACITY = 100_000
ERROR_RATE = 0.001


@app.on_event("startup")
def load_bloom_filter():
    # Connect to the database and fetch usernames
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM user")
    usernames = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Create and populate the Bloom filter
    bloom = BloomFilter(capacity=BLOOM_CAPACITY, error_rate=ERROR_RATE)
    for username in usernames:
        bloom.add(username)

    # Store in app state
    app.state.bloom_filter = bloom
    print(f"Loaded {len(usernames)} usernames into Bloom filter.")



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.receipts import router as receipts_router

app = FastAPI(title="Expense Tracker API", version="1.0")

# later: restrict origins to your Vercel/Netlify domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(receipts_router, prefix="/api")

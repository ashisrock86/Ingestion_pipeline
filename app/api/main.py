from fastapi import FastAPI
from routes.health import router as health_router
from routes.documents import router as documents_router

app = FastAPI(title="My FastAPI App")
app.state.db = {}  # Placeholder for database connection, if needed

# Include routers
app.include_router(health_router)

app.include_router(documents_router, prefix="/documents")

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}


def main() -> None:
    """Run the FastAPI app directly with Uvicorn."""
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8200, reload=True)

if __name__ == "__main__":
    main()
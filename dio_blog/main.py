from fastapi import FastAPI

from controller.post import router as post_router

app = FastAPI(title="DIO Blog API", version="0.1.0", description="API para gerenciamento de posts do blog da DIO")
app.include_router(post_router)
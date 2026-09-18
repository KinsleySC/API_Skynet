from fastapi import FastAPI

app = FastAPI(title="RecipeShare API")


@app.get("/")
def root():
    return {"message": "RecipeShare API"}

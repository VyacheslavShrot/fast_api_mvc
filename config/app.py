from fastapi import FastAPI

app = FastAPI(
    title="Fast API MVC"
)


@app.get("/app-status")
async def app_status():
    return {
        "status": "success"
    }

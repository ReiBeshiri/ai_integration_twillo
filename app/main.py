from fastapi import FastAPI, Response
from app.api import webhook

#uvicorn app.main:app --reload

app = FastAPI(title="AI WhatsApp Agent")

app.include_router(webhook.router)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)





#authorize the app to run powershell scripts
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser 
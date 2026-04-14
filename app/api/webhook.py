from fastapi import APIRouter, Request
from twilio.rest import Client
import os
from app.services.llm_service import generate_response

router = APIRouter()
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

"""
Webhook endpoint for WhatsApp messages
twillo uses Body=inviomsg&From=+39123 instead of JSON, so we need to use form data instead of JSON
message = data.get("Body") and sender = data.get("From") insted of data = await request.json()
so in postamn, application/x-www-form-urlencoded not application/json

verbose version of the webhook endpoint for WhatsApp messages using Request and form data
this is more flexible and can handle any form data, but it is more verbose and less concise than the FastAPI version
"""
@router.post("/webhook/whatsapp/received")
async def whatsapp_webhook_receive_test(request: Request):
    data = await request.form()
    message = data.get("Body")
    sender = data.get("From")

    print(f"[WHATSAPP] {sender}: {message}")

    result = f"received from {sender}: {message}"
    return {"status": result}

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.form()
    message = data.get("Body")
    sender = str(data.get("From"))

    print(f"[WHATSAPP] {sender}: {message}")

    #response_text = f"Hai scritto: {message}"
    
    ai_response_text = await generate_response(str(message))  # genera la risposta usando il servizio LLM

    client.messages.create(
        from_="whatsapp:+14155238886",  # numero sandbox Twilio 
        body=ai_response_text,
        to=sender
    )

    return {"status": "replied"}

"""
Another version of the webhook endpoint for WhatsApp messages using FastAPI's Form dependency
this is more concise and easier to read, but it maybe not work with all webhook providers that expect form data in a specific format
You need to adjust the parameter names and types to match the expected format of the webhook provider you are using

@router.post("/webhook/whatsapp")
async def whatsapp_webhook_fastapi(Body: str = Form(...), From: str = Form(...)):
    print(f"[WHATSAPP] {From}: {Body}")
    return {"status": f"received from {From}"}
"""
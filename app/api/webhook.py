from fastapi import APIRouter, Request

router = APIRouter()


"""
Webhook endpoint for WhatsApp messages
twillo uses Body=inviomsg&From=+39123 instead of JSON, so we need to use form data instead of JSON
message = data.get("Body") and sender = data.get("From") insted of data = await request.json()
so in postamn, application/x-www-form-urlencoded not application/json
"""
@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.form()
    message = data.get("Body")
    sender = data.get("From")

    print(f"[WHATSAPP] {sender}: {message}")

    result = f"received from {sender}: {message}"

    return {"status": result}
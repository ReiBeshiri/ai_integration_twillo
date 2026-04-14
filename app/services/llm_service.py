from groq import AsyncGroq  # Importiamo la versione Asincrona

client = AsyncGroq(api_key="")

gpt_model = "llama-3.1-8b-instant"
system_prompt = "Sei un assistente utile e conciso."


async def generate_response(message: str) -> str:
    response = await client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    return str(response.choices[0].message.content)
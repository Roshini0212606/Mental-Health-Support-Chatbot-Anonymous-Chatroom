
import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Get key from environment
api_key = os.getenv("XAI_API_KEY")
print(f"API Key loaded from .env: {api_key[:10]}..." if api_key else "API Key NOT found in .env")

if not api_key:
    exit(1)

try:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    response = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, simply reply with 'Connection Successful' if you receive this."}
        ]
    )
    print("Response from Grok:", response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")

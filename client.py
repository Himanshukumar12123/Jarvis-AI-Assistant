from groq import Groq

# Initialize the free Groq client
client = Groq(
    api_key="YOUR_GROQ_API_KEY"
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",  # <-- FIX: Changed to an active, supported model
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like alexa and google cloud."},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)
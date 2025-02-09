from google import genai

client = genai.Client(api_key="AIzaSyAh-GQ7jgx4Ssxta0pEBDrKHR3DN6pvskI")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)
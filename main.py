from google import genai

def main():
    # $env:GEMINI_API_KEY="API_KEY"

    client = genai.Client()  # automatically reads GEMINI_API_KEY

    # flash models are fast, cheap, free-tier
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain what a token is in one short sentence.",
    )

    print(response.text)


if __name__ == "__main__":
    main()

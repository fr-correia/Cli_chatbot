from google import genai

def main():

    client = genai.Client()

    # First call
    r1 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="My name is Francisco. Remember it.",
    )

    print("Answer:", r1.text)

    # Second call
    r2 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="What is my name?",
    )
    print("Answer:", r2.text)

if __name__ == "__main__":
    main()


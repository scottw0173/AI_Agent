import os
from google import genai
from dotenv import load_dotenv
load_dotenv()


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing API key")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model = 'gemini-2.5-flash', contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    prompt_metadata= response.usage_metadata.prompt_token_count
    response_metadata= response.usage_metadata.candidates_token_count
    total_metadata= response.usage_metadata.total_token_count
    if not response.usage_metadata:
        raise RuntimeError("Failed API Request")
    print("=====Response=====")
    print(response.text)
    print(f"Prompt tokens: {prompt_metadata}")
    print(f"Response tokens: {response_metadata}")
    print(f"Total tokens: {total_metadata}")




if __name__ == "__main__":
    main()

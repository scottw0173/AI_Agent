import os
import argparse
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions
from dotenv import load_dotenv
load_dotenv()


def main():
    api_key = os.environ.get("GEMINI_API_KEY") #import API key from local environment
    if not api_key:
        raise RuntimeError("Missing API key")    #raise error if there is no API key
    

    parser = argparse.ArgumentParser(description="What do you want to ask Gemini?")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()     #these 3 lines should give us access to args.user_prompt as a variable
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])] #creates a list for args.user_prompt


    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model = 'gemini-2.5-flash', contents = messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    prompt_metadata= response.usage_metadata.prompt_token_count
    response_metadata= response.usage_metadata.candidates_token_count
    total_metadata= response.usage_metadata.total_token_count
    if not response.usage_metadata:
        raise RuntimeError("Failed API Request")
    if args.verbose:
        print("=====Prompt=====")
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_metadata}")
        print(f"Response tokens: {response_metadata}")
    print("=====Response=====")
    if response.function_calls:
        for call in response.function_calls:
        # Each 'call' is a FunctionCall object
            print(call.name)
            print(call.args)
    else:
        print(response.text)
    print(f"Total tokens: {total_metadata}")




if __name__ == "__main__":
    main()

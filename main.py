import os
import argparse
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions, call_function
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing API key")

    parser = argparse.ArgumentParser(description="What do you want to ask Gemini?")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )

        # Add model candidates to history
        if response.candidates:
            for cand in response.candidates:
                if cand.content:
                    messages.append(cand.content)

        # Done if no tool calls
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        # Run tools
        function_parts = call_function(response.function_calls, verbose=args.verbose)

        # CRITICAL: tool outputs should be role="tool"
        messages.append(types.Content(role="tool", parts=function_parts))

        if args.verbose:
            for p in function_parts:
                fr = p.function_response
                if fr and fr.response:
                    print(f"-> {fr.response}")

    print("Error: max iterations reached and model still requested tools.")
    raise SystemExit(1)

if __name__ == "__main__":
    main()

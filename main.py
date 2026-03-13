import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    #To load .env with key
    load_dotenv()
    #get the api key from .env
    api_key = os.environ.get("GEMINI_API_KEY")
    #if no key show an error
    if api_key == None:
        raise RuntimeError("Missing API KEY")
    #bring the geminai client up
    client = genai.Client(api_key=api_key)


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`  

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        #Get a resonse
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        if response.usage_metadata == None:
            raise RuntimeError("Metadata Issue")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
        if not response.function_calls == None:
            function_responses = []
            for func in response.function_calls:
                function_call_result = call_function(func, args.verbose)
                if not function_call_result.parts:
                    raise Exception("Function_call is empty")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Function_response is None")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function response is None")
                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(response.text)
            break
    else:
        print("Maximum iterations reached without a final response")
        sys.exit(1)



if __name__ == "__main__":
    main()

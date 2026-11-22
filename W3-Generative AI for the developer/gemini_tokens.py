import os
from google import genai

MODEL = "gemini-3.5-flash-lite"


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit(
            "GEMINI_API_KEY was not found.\n"
            "Set it as an environment variable, then run the script again."
        )

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model=MODEL)

    total_input = 0
    total_output = 0
    total_tokens = 0

    print(f"Connected to {MODEL}. Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_text.lower() in {"exit", "quit"}:
            break

        if not user_text:
            continue

        try:
            response = chat.send_message(user_text)
        except Exception as error:
            print(f"\nGemini API error: {error}\n")
            continue

        print(f"\nGemini: {response.text or '(No text returned)'}\n")

        usage = response.usage_metadata
        if usage is None:
            print("Token usage data was not available for this request.\n")
            continue

        input_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        request_total = usage.total_token_count or 0

        total_input += input_tokens
        total_output += output_tokens
        total_tokens += request_total

        print("Tokens for this request")
        print(f"Input:  {input_tokens:,}")
        print(f"Output: {output_tokens:,}")
        print(f"Total:  {request_total:,}")

    print("Session summary")
    print(f"Total input tokens:  {total_input:,}")
    print(f"Total output tokens: {total_output:,}")
    print(f"Total tokens:        {total_tokens:,}")


if __name__ == "__main__":
    main()
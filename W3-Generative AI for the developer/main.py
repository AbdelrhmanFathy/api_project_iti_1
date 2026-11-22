import os
from openai import OpenAI

PRICING = {
    "gpt-4o":       {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":  {"input": 0.15,  "output": 0.60},
    "gpt-4.1":      {"input": 2.00,  "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40,  "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10,  "output": 0.40},
}

def calculate_cost(model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
    
    if model_name not in PRICING:
        print(f"Warning: Pricing for model '{model_name}' not found. Cost = 0.0")
        return 0.0
    
    pricing = PRICING[model_name]
    input_cost = (prompt_tokens / 1000000) * pricing["input"]
    output_cost = (completion_tokens / 1000000) * pricing["output"]
    
    return input_cost + output_cost

def chat_with_cost_analysis(prompt: str, model: str = "gpt-4o-mini"):
        
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Environment variable OPENAI_API_KEY is not set. Please set it first.")
    
    client = OpenAI(api_key=api_key)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant and answer briefly."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        print(f"⏳ Sending request to model: {model} ...\n")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        
        # Extract text and usage
        reply = response.choices[0].message.content
        usage = response.usage
        
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        
        # Calculate cost
        cost = calculate_cost(model, prompt_tokens, completion_tokens)
        
        # Display results
        print("=" * 50)
        print("✅ Assistant reply:")
        print(reply)
        print("=" * 50)
        print("Usage analysis:")
        print(f"Input tokens (Prompt):    {prompt_tokens:,}")
        print(f"Output tokens (Completion): {completion_tokens:,}")
        print(f"Total tokens:                {total_tokens:,}")
        print(f"Request cost:                ${cost:.6f}")
        print("=" * 50)
        
        return {
            "reply": reply,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost
        }
    
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")
        return None


if __name__ == "__main__":
    user_prompt = "Explain the concept of generative AI in two sentences."
    selected_model = "gpt-4o-mini" 
    
    chat_with_cost_analysis(prompt=user_prompt, model=selected_model)
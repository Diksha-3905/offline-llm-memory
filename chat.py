import requests
def ask_llm(prompt):
    # Send your question to the local Ollama model
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=True
    )

    # Print the model's reply as it streams
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if '"response"' in data:
                text = data.split('"response":"')[1].split('"')[0]
                print(text, end="", flush=True)
    print("\n")

# Simple chat loop
print("🤖 Offline LLM Chat (type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break
    ask_llm(user_input)

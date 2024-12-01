from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import os

language = "pl"

# Define the prompt template
if language == "pl":
    template = """
Jesteś moim przyjaznym asystentem. Sprawiasz, że rozmowa jest ciekawa i angażująca.

Oto historia dotychczasowej rozmowy:
{context}

Użytkownik właśnie zadał pytanie:
{question}

Twoja odpowiedź powinna brzmieć:
"""

else:
    template = """
    You are my friendly assistant. You keep the conversation interesting and engaging.
    Here is the conversation history so far:
    {context}
    The user has just asked:
    {question}
    Your response should be:
    """

# Initialize the model
model = OllamaLLM(model="dolphin-llama3")

# Create a PromptTemplate with the defined template
prompt_template = PromptTemplate(template=template, input_variables=["context", "question"])


def handle_conversation(user_input):
    # Full path to the file
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, "context_AI.txt")
    
    # Read existing context from the file
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            old_context = file.read().strip()
    else:
        old_context = ""

    # Format the prompt with context and question
    formatted_prompt = prompt_template.format(context=old_context, question=user_input)
    
    # Get the response from the model
    result = model.invoke(formatted_prompt)
    
    # Print the result
    print("AI:", result)
    print("  ")
    
    # Update the context
    new_context = f"{old_context}\nUser: {user_input}\nAI: {result}"
    with open(file_path, 'w') as file:
        file.write(new_context)


def main():
    print("Welcome! Type your questions below. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        handle_conversation(user_input)


if __name__ == "__main__":
    main()

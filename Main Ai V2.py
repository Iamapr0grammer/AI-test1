from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import os
import json
import vosk
import pyaudio

language = "pl"

# Define the prompt template

if language == "pl":
    template = """
Jesteś moim przyjaznym asystentem. Sprawiasz, że rozmowa jest ciekawa i angażująca.

Oto historia dotychczasowej rozmowy:
{context}

Użytkownik właśnie zadał pytanie:*
{question}

Twoja odpowiedź powinna brzmieć:
"""

else:
    template = """
    You are my friendly assistant. You keep the conversation as short as possible.
    Here is the conversation history so far:
    {context}
    The user has just asked:
    {question}
    Your response should be:
    """

# Initialize the model
model = OllamaLLM(model="dolphin-llama3:latest")

# Create a PromptTemplate with the defined template
prompt_template = PromptTemplate(template=template, input_variables=["context", "question"])


def handle_conversation(user_input):

    # Pełna ścieżka pliku
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, "context AI.txt")
    old_context = ""
    with open(file_path, 'r') as file:
        old_context = file.read().strip()

    # Format the prompt with context and question
    formatted_prompt = prompt_template.format(context=old_context, question=user_input)
    
    # Get the response from the model using invoke
    result = model.invoke(formatted_prompt)
    
    # Print the result
    print("AI:", result)
    print("  ")
    
    # Update the context
    old_context += f"\nUser: {user_input}\nAI: {result}"
    with open(file_path, 'a') as file:
        file.write(old_context)


def listen_for_speech():
    # Absolute path to your Vosk model directory

    if language == "pl":
        model_path = r"C:\pocketsphinx\pl-small"
    else:
        model_path = r"C:\pocketsphinx\en-small\vosk-model-small-en-us-0.15"  # Update this path to your model directory

    # Verify that the path exists
    if not os.path.isdir(model_path):
        raise FileNotFoundError(f"Model directory not found: {model_path}")

    # Initialize Vosk recognizer
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Setup PyAudio for streaming audio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    stream.start_stream()

    print("Listening...")

    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            text = result_dict.get('text', '')
            if text:
                print(f"You: {text}")
                handle_conversation(text)
        else:
            # For partial results
            partial_result = recognizer.PartialResult()
            #print(f"Partial: {json.loads(partial_result).get('partial', '')}")

if __name__ == "__main__":
    listen_for_speech()

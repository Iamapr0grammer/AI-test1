import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties (e.g., voice, rate)
engine.setProperty('rate', 130)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# Load your custom voice model here if applicable
# (This step depends on the format of the model and the TTS library you use)

# Convert text to speech
engine.say("Hello, this is a test of the custom TTS model.")
engine.runAndWait()

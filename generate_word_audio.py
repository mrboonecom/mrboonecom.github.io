import yaml
from gtts import gTTS
import os

# Path to the YAML file in the same directory
yaml_file = "words.yaml"

# Directory to store audio files
audio_dir = "audio"

# Create audio directory if it doesn't exist
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

def load_yaml_file(file_path):
    """Load and parse YAML file from local directory."""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found in the current directory.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def generate_audio(word, audio_dir):
    """Generate audio for a given word using gTTS and save to audio_dir."""
    try:
        # Create gTTS object with American English
        tts = gTTS(text=word, lang="en", tld="us")  # tld="us" ensures American English accent
        # Define output file path
        audio_file = os.path.join(audio_dir, f"{word.lower()}.mp3")
        # Save audio file
        tts.save(audio_file)
        print(f"Generated audio for '{word}' at {audio_file}")
    except Exception as e:
        print(f"Error generating audio for '{word}': {e}")

def main():
    # Load YAML data
    data = load_yaml_file(yaml_file)
    if not data:
        print("Failed to load YAML data. Exiting.")
        return

    # Process each word in the YAML file
    for entry in data:
        word = entry.get("word")
        if word:
            generate_audio(word, audio_dir)
        else:
            print("Invalid entry found in YAML file, skipping.")

if __name__ == "__main__":
    main()

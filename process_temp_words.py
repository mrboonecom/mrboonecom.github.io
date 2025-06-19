import yaml
import os
from gtts import gTTS

# File paths
main_yaml_file = "words.yaml"
temp_yaml_file = "temp_words.yaml"
audio_dir = "audio"

# Create audio directory if it doesn't exist
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

def load_yaml_file(file_path):
    """Load YAML file and return content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or []
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}")
        return []

def save_yaml_file(file_path, data):
    """Save data to YAML file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(data, file, allow_unicode=True)
        print(f"Updated {file_path} successfully.")
    except Exception as e:
        print(f"Error saving YAML file {file_path}: {e}")

def check_duplicates(temp_words, main_words):
    """Identify duplicates and return non-duplicate temp words."""
    main_word_set = {word['word'].lower() for word in main_words}
    non_duplicates = []
    duplicates_found = []

    for word_data in temp_words:
        if word_data['word'].lower() in main_word_set:
            duplicates_found.append(word_data['word'])
        else:
            non_duplicates.append(word_data)

    if duplicates_found:
        print(f"Skipped duplicates: {', '.join(duplicates_found)}")
    else:
        print("No duplicates found in temp_words.yaml.")

    return non_duplicates

def generate_audio(word, audio_dir):
    """Generate audio for a word using gTTS and save to audio_dir."""
    audio_file = os.path.join(audio_dir, f"{word.lower()}.mp3")
    if os.path.exists(audio_file):
        print(f"Audio file for '{word}' already exists, skipping generation.")
        return
    try:
        tts = gTTS(text=word, lang="en", tld="us")  # American English
        tts.save(audio_file)
        print(f"Generated audio for '{word}' at {audio_file}")
    except Exception as e:
        print(f"Error generating audio for '{word}': {e}")

def verify_audio_files(words, audio_dir):
    """Ensure all words in words.yaml have corresponding audio files."""
    missing_audio = []
    for word_data in words:
        word = word_data['word']
        audio_file = os.path.join(audio_dir, f"{word.lower()}.mp3")
        if not os.path.exists(audio_file):
            missing_audio.append(word)
            generate_audio(word, audio_dir)
    if missing_audio:
        print(f"Generated missing audio files for: {', '.join(missing_audio)}")
    else:
        print("All words in words.yaml have corresponding audio files.")

def clear_temp_file():
    """Clear temp_words.yaml after processing."""
    try:
        with open(temp_yaml_file, 'w', encoding='utf-8') as file:
            file.write("")  # Empty the file
        print(f"Cleared {temp_yaml_file} for next batch.")
    except Exception as e:
        print(f"Error clearing {temp_yaml_file}: {e}")

def main():
    # Load main and temp YAML files
    main_words = load_yaml_file(main_yaml_file)
    temp_words = load_yaml_file(temp_yaml_file)

    if not temp_words:
        print(f"No words found in {temp_yaml_file}. Exiting.")
        return

    # Check for duplicates and get non-duplicate words
    non_duplicate_words = check_duplicates(temp_words, main_words)

    if not non_duplicate_words:
        print("No new words to add after duplicate check. Clearing temp_words.yaml.")
        clear_temp_file()
        return

    # Append non-duplicate words to main_words
    updated_main_words = main_words + non_duplicate_words
    save_yaml_file(main_yaml_file, updated_main_words)

    # Generate audio for new words
    for word_data in non_duplicate_words:
        generate_audio(word_data['word'], audio_dir)

    # Verify all words in main database have audio files
    verify_audio_files(updated_main_words, audio_dir)

    # Clear temp_words.yaml for next batch
    clear_temp_file()

if __name__ == "__main__":
    main()

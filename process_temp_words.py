import yaml
import os
from gtts import gTTS
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from tqdm import tqdm
import time

# Initialize Rich console
console = Console()

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
            data = yaml.safe_load(file) or []
        console.print(f"[green]✓ Loaded {file_path} successfully.[/green]")
        return data
    except FileNotFoundError:
        console.print(f"[red]✗ Error: {file_path} not found.[/red]")
        return []
    except yaml.YAMLError as e:
        console.print(f"[red]✗ Error parsing {file_path}: {e}[/red]")
        return []

def save_yaml_file(file_path, data):
    """Save data to YAML file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(data, file, allow_unicode=True)
        console.print(f"[green]✓ Updated {file_path} with {len(data)} entries.[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error saving {file_path}: {e}[/red]")

def remove_yaml_duplicates(words, file_name):
    """Remove duplicates from a YAML word list and return cleaned list."""
    seen = set()
    cleaned_words = []
    duplicates = []
    for word_data in words:
        word_lower = word_data['word'].lower()
        if word_lower in seen:
            duplicates.append(word_data['word'])
        else:
            seen.add(word_lower)
            cleaned_words.append(word_data)
    if duplicates:
        console.print(f"[yellow]⚠ Removed duplicates from {file_name}: {', '.join(duplicates)}[/yellow]")
    return cleaned_words

def check_temp_duplicates(temp_words, main_words):
    """Identify duplicates between temp_words and main_words."""
    main_word_set = {word['word'].lower() for word in main_words}
    non_duplicates = []
    duplicates = []
    for word_data in temp_words:
        if word_data['word'].lower() in main_word_set:
            duplicates.append(word_data['word'])
        else:
            non_duplicates.append(word_data)
    if duplicates:
        console.print(f"[yellow]⚠ Skipped duplicates in {temp_yaml_file}: {', '.join(duplicates)}[/yellow]")
    else:
        console.print(f"[green]✓ No duplicates found in {temp_yaml_file}.[/green]")
    return non_duplicates

def check_audio_duplicates(audio_dir):
    """Check for duplicate audio files and delete extras."""
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
    word_counts = {}
    duplicates = []
    for audio_file in audio_files:
        word = os.path.splitext(audio_file)[0].lower()
        word_counts[word] = word_counts.get(word, 0) + 1
        if word_counts[word] > 1:
            duplicates.append(audio_file)
            try:
                os.remove(os.path.join(audio_dir, audio_file))
                console.print(f"[yellow]⚠ Deleted duplicate audio file: {audio_file}[/yellow]")
            except Exception as e:
                console.print(f"[red]✗ Error deleting {audio_file}: {e}[/red]")
    return len(duplicates) == 0

def generate_audio(word, audio_dir):
    """Generate audio for a word using gTTS and save to audio_dir."""
    audio_file = os.path.join(audio_dir, f"{word.lower()}.mp3")
    if os.path.exists(audio_file):
        return True
    try:
        tts = gTTS(text=word, lang="en", tld="us")  # American English
        tts.save(audio_file)
        return True
    except Exception as e:
        console.print(f"[red]✗ Error generating audio for '{word}': {e}[/red]")
        return False

def verify_audio_files(words, audio_dir):
    """Ensure all words in words.yaml have corresponding audio files."""
    missing_audio = []
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Verifying audio files...", total=len(words))
        for word_data in words:
            word = word_data['word']
            audio_file = os.path.join(audio_dir, f"{word.lower()}.mp3")
            if not os.path.exists(audio_file):
                missing_audio.append(word)
                if generate_audio(word, audio_dir):
                    console.print(f"[green]✓ Generated audio for '{word}' at {audio_file}[/green]")
            progress.advance(task)
    return missing_audio

def clear_temp_file():
    """Clear temp_words.yaml after processing."""
    try:
        with open(temp_yaml_file, 'w', encoding='utf-8') as file:
            file.write("")
        console.print(f"[green]✓ Cleared {temp_yaml_file} for next batch.[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error clearing {temp_yaml_file}: {e}[/red]")

def display_summary(main_words, audio_dir, no_yaml_duplicates, no_audio_duplicates, missing_audio):
    """Display a summary of the process."""
    table = Table(title="[bold blue]Process Summary[/bold blue]", show_header=False, box=None)
    table.add_row("Total words in words.yaml", f"[cyan]{len(main_words)}[/cyan]")
    table.add_row("No duplicates in words.yaml", f"[{'green' if no_yaml_duplicates else 'red'}]✓ {'Yes' if no_yaml_duplicates else 'No'}[/]")
    table.add_row("No duplicates in audio directory", f"[{'green' if no_audio_duplicates else 'red'}]✓ {'Yes' if no_audio_duplicates else 'No'}[/]")
    table.add_row("All words have audio files", f"[{'green' if not missing_audio else 'red'}]✓ {'Yes' if not missing_audio else 'No'}[/]")
    if missing_audio:
        table.add_row("Missing audio files generated", f"[yellow]{', '.join(missing_audio)}[/yellow]")
    console.print(Panel(table, expand=False, border_style="blue"))

def main():
    console.print(Panel("[bold cyan]TOEFL Vocabulary Processor[/bold cyan]", border_style="cyan"))
    console.print(f"[italic]Processing started at {time.strftime('%Y-%m-%d %H:%M:%S')}[/italic]\n")

    # Load main and temp YAML files
    main_words = load_yaml_file(main_yaml_file)
    temp_words = load_yaml_file(temp_yaml_file)

    if not temp_words:
        console.print(f"[red]✗ No words found in {temp_yaml_file}. Exiting.[/red]")
        return

    # Remove duplicates from main_words
    main_words = remove_yaml_duplicates(main_words, main_yaml_file)
    save_yaml_file(main_yaml_file, main_words)

    # Remove duplicates from temp_words
    temp_words = remove_yaml_duplicates(temp_words, temp_yaml_file)

    # Check for duplicates between temp_words and main_words
    non_duplicate_words = check_temp_duplicates(temp_words, main_words)

    if not non_duplicate_words:
        console.print("[yellow]⚠ No new words to add after duplicate check.[/yellow]")
        clear_temp_file()
        # Verify audio files for existing main_words
        missing_audio = verify_audio_files(main_words, audio_dir)
        no_audio_duplicates = check_audio_duplicates(audio_dir)
        display_summary(main_words, audio_dir, True, no_audio_duplicates, missing_audio)
        return

    # Generate audio for new words with progress bar
    console.print("\n[bold cyan]Generating audio files...[/bold cyan]")
    audio_success = []
    for word_data in tqdm(non_duplicate_words, desc="Processing audio", unit="word"):
        if generate_audio(word_data['word'], audio_dir):
            audio_success.append(word_data)

    # Append successful new words to main_words
    main_words.extend(audio_success)
    save_yaml_file(main_yaml_file, main_words)

    # Verify all words have audio files
    missing_audio = verify_audio_files(main_words, audio_dir)

    # Check for audio duplicates
    no_audio_duplicates = check_audio_duplicates(audio_dir)

    # Clear temp_words.yaml
    clear_temp_file()

    # Display summary
    display_summary(main_words, audio_dir, True, no_audio_duplicates, missing_audio)

if __name__ == "__main__":
    main()

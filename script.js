// Load words from YAML
async function loadWords() {
    try {
        const response = await fetch('words.yaml');
        if (!response.ok) throw new Error('Failed to load words.yaml');
        const yamlText = await response.text();
        return jsyaml.load(yamlText);
    } catch (error) {
        console.error('Error loading YAML:', error);
        return [];
    }
}

// Initialize app
async function init() {
    const words = await loadWords();
    if (words.length === 0) {
        document.getElementById('word').textContent = 'Error loading words';
        return;
    }

    let currentIndex = 0;
    const flashcard = document.getElementById('flashcard');
    const wordEl = document.getElementById('word');
    const posEl = document.getElementById('part-of-speech');
    const defEl = document.getElementById('definition');
    const exEl = document.getElementById('example');
    const audioEl = document.getElementById('word-audio');
    let audioTimeout = null;

    // Function to update card content
    function updateCard(index) {
        const wordData = words[index];
        wordEl.textContent = wordData.word;
        posEl.textContent = wordData.part_of_speech;
        defEl.textContent = wordData.definition;
        exEl.textContent = wordData.example;
        audioEl.src = `audio/${wordData.word.toLowerCase()}.mp3`;
        playAudioWithDelay();
    }

    // Play audio with 0.2s delay
    function playAudioWithDelay() {
        if (audioTimeout) clearTimeout(audioTimeout);
        audioTimeout = setTimeout(() => {
            audioEl.play().catch(error => console.error('Audio playback error:', error));
        }, 200);
    }

    // Initial card
    updateCard(currentIndex);

    // Swipe handling with Hammer.js
    const hammer = new Hammer(flashcard);
    hammer.on('swipeleft', () => {
        if (currentIndex < words.length - 1) {
            flashcard.classList.add('swiping-right');
            setTimeout(() => {
                currentIndex++;
                updateCard(currentIndex);
                flashcard.classList.remove('swiping-right');
            }, 300);
        }
    });
    hammer.on('swiperight', () => {
        if (currentIndex > 0) {
            flashcard.classList.add('swiping-left');
            setTimeout(() => {
                currentIndex--;
                updateCard(currentIndex);
                flashcard.classList.remove('swiping-left');
            }, 300);
        }
    });

    // Tap to play audio
    flashcard.addEventListener('click', playAudioWithDelay);
}

init();

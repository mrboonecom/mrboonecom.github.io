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

// Shuffle array using Fisher-Yates algorithm
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Initialize app
async function init() {
    let words = await loadWords();
    if (words.length === 0) {
        document.getElementById('word').textContent = 'Error loading words';
        return;
    }

    // Shuffle words on load
    words = shuffleArray(words);

    let currentIndex = 0;
    const flashcard = document.getElementById('flashcard');
    const wordEl = document.getElementById('word');
    const posEl = document.getElementById('part-of-speech');
    const defEl = document.getElementById('definition');
    const exEl = document.getElementById('example');
    const audioEl = document.getElementById('word-audio');
    let audioTimeout = null;
    let isTransitioning = false;

    // Function to update card content
    function updateCard(index, direction = null) {
        if (isTransitioning) return;
        isTransitioning = true;
        flashcard.classList.add('transitioning');

        if (direction) {
            flashcard.classList.add(`swiping-${direction}`);
        }

        // Wait for the exit animation to complete
        setTimeout(() => {
            // Update content
            const wordData = words[index];
            wordEl.textContent = wordData.word;
            posEl.textContent = wordData.part_of_speech;
            defEl.textContent = wordData.definition;
            exEl.textContent = wordData.example;
            audioEl.src = `audio/${wordData.word.toLowerCase()}.mp3`;

            // Reset card position with a slight delay for smoothness
            flashcard.style.transform = 'translateX(0)';
            flashcard.style.opacity = '1';
            flashcard.classList.remove('swiping-left', 'swiping-right');

            // Play audio after reset
            playAudioWithDelay();

            // Re-enable interactions
            requestAnimationFrame(() => {
                isTransitioning = false;
                flashcard.classList.remove('transitioning');
            });
        }, 400); // Match CSS transition duration
    }

    // Play audio with 0.2s delay
    function playAudioWithDelay() {
        if (audioTimeout) clearTimeout(audioTimeout);
        audioTimeout = setTimeout(() => {
            audioEl.play().catch(error => console.error('Audio playback error:', error));
        }, 200); // 200ms = 0.2 seconds
    }

    // Initial card
    updateCard(currentIndex);

    // Swipe handling with Hammer.js
    const hammer = new Hammer(flashcard);
    hammer.on('swipeleft', () => {
        if (isTransitioning) return;
        currentIndex = (currentIndex + 1) % words.length; // Loop to first card if at end
        updateCard(currentIndex, 'right');
    });
    hammer.on('swiperight', () => {
        if (isTransitioning) return;
        currentIndex = (currentIndex - 1 + words.length) % words.length; // Loop to last card if at start
        updateCard(currentIndex, 'left');
    });

    // Tap to play audio
    flashcard.addEventListener('click', playAudioWithDelay);
}

init();

let currentIndex = 0;
let words = [];
let audio = new Audio();

document.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("words.json");
  words = await response.json();

  showWord();
  addSwipeListeners();
});

function showWord() {
  const { word, pos, thai } = words[currentIndex];
  const card = document.getElementById("flashcard");

  card.innerHTML = `
    <div class="word">${word}</div>
    <div class="pos">${pos}</div>
    <div class="thai">${thai}</div>
  `;

  playAudio();
}

function playAudio() {
  const { word } = words[currentIndex];
  audio.src = `audio/${word}.mp3`;
  audio.play();
}

function addSwipeListeners() {
  let startX;

  document.addEventListener("touchstart", e => {
    startX = e.touches[0].clientX;
  });

  document.addEventListener("touchend", e => {
    const endX = e.changedTouches[0].clientX;
    if (startX - endX > 50) nextWord();     // swipe left
    else if (endX - startX > 50) prevWord(); // swipe right
  });

  document.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") nextWord();
    if (e.key === "ArrowLeft") prevWord();
  });
}

function nextWord() {
  if (currentIndex < words.length - 1) {
    currentIndex++;
    showWord();
  }
}

function prevWord() {
  if (currentIndex > 0) {
    currentIndex--;
    showWord();
  }
}

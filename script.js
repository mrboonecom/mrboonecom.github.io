let currentIndex = 0;
let words = [];
let audio = new Audio();

document.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("words.json");
  words = await response.json();
  showWord();
  addSwipeListeners();
  showOnboarding();
});

function showWord() {
  const word = words[currentIndex];
  const card = document.getElementById("flashcard");
  card.textContent = word;
  playAudio();
}

function playAudio() {
  const word = words[currentIndex];
  audio.src = `audio/${word}.mp3`;
  audio.play();
}

function addSwipeListeners() {
  let startX = 0;

  document.addEventListener("touchstart", e => {
    startX = e.touches[0].clientX;
  });

  document.addEventListener("touchend", e => {
    const endX = e.changedTouches[0].clientX;
    if (startX - endX > 50) nextWord();      // Swipe left
    else if (endX - startX > 50) prevWord(); // Swipe right
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

function showOnboarding() {
  if (!localStorage.getItem("seenOnboarding")) {
    document.getElementById("onboarding").style.display = "flex";
  }
}

function dismissOnboarding() {
  document.getElementById("onboarding").style.display = "none";
  localStorage.setItem("seenOnboarding", "true");
}

let targetNumber = Math.floor(Math.random() * 100) + 1;
let attempts = 0;

function checkGuess() {
    const guessInput = document.getElementById('guess-input');
    const guess = parseInt(guessInput.value);
    const hint = document.getElementById('game-hint');
    const message = document.getElementById('game-message');

    if (isNaN(guess) || guess < 1 || guess > 100) {
        hint.textContent = 'Please enter a number between 1 and 100!';
        return;
    }

    attempts++;

    if (guess === targetNumber) {
        message.textContent = `Congratulations! You guessed it in ${attempts} attempts!`;
        hint.textContent = 'Click below to play again!';
        guessInput.disabled = true;
        setTimeout(resetGame, 3000);
    } else if (guess < targetNumber) {
        hint.textContent = 'Too low! Try a higher number.';
    } else {
        hint.textContent = 'Too high! Try a lower number.';
    }

    guessInput.value = '';
}

function resetGame() {
    targetNumber = Math.floor(Math.random() * 100) + 1;
    attempts = 0;
    document.getElementById('guess-input').disabled = false;
    document.getElementById('game-message').textContent = 'Guess a number between 1 and 100!';
    document.getElementById('game-hint').textContent = '';
}

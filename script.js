// Number Guess Game
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

// Quiz Logic
let currentQuestion = 0;
let answers = {};
let questions = []; // Will be defined in curriculum pages

function loadQuestion() {
    const quizContainer = document.getElementById('quiz-question');
    if (!quizContainer || !questions.length) return;

    const question = questions[currentQuestion];
    const isAnswered = answers[currentQuestion] !== undefined;
    quizContainer.innerHTML = `
        <h3>Question ${currentQuestion + 1}: ${question.question}</h3>
        ${question.options.map((option, index) => `
            <label>
                <input type="radio" name="answer" value="${index}" ${answers[currentQuestion] === index ? 'checked' : ''}>
                ${option}
            </label>
        `).join('')}
    `;

    const prevButton = document.getElementById('prev-question');
    const nextButton = document.getElementById('next-question');
    prevButton.disabled = currentQuestion === 0;
    nextButton.textContent = currentQuestion === questions.length - 1 ? 'Submit Quiz' : 'Next';
    
    const status = document.getElementById('quiz-status');
    const unanswered = questions.length - Object.keys(answers).length;
    status.textContent = `Unanswered questions: ${unanswered}`;
}

function saveAnswer() {
    const selected = document.querySelector('input[name="answer"]:checked');
    if (selected) {
        answers[currentQuestion] = parseInt(selected.value);
    }
}

function prevQuestion() {
    saveAnswer();
    if (currentQuestion > 0) {
        currentQuestion--;
        loadQuestion();
    }
}

function nextQuestion() {
    saveAnswer();
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        loadQuestion();
    } else {
        submitQuiz();
    }
}

function submitQuiz() {
    saveAnswer();
    let score = 0;
    questions.forEach((q, index) => {
        if (answers[index] === q.correct) {
            score++;
        }
    });

    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML = `
        <div class="quiz-result">
            <h3>Congratulations, You Scored ${score} out of ${questions.length}!</h3>
            <p>${score >= 8 ? 'Great job! You’re ready to excel!' : score >= 5 ? 'Good effort! Let’s boost that score together!' : 'Don’t worry, practice makes perfect!'}</p>
            <p>Want to be confident in math? <a href="https://mrboone.com" target="_blank">Study with Mr. Boone!</a></p>
            <button onclick="resetQuiz()">Try Again</button>
        </div>
    `;
}

function resetQuiz() {
    currentQuestion = 0;
    answers = {};
    loadQuestion();
}

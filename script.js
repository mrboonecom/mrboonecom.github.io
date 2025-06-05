document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('bg-video');
    
    // Ensure video autoplays and loops
    video.play().catch(error => {
        console.error('Video autoplay failed:', error);
        // Fallback: Add a play button if autoplay is blocked
        const playButton = document.createElement('button');
        playButton.textContent = 'Play Video';
        playButton.style.position = 'absolute';
        playButton.style.top = '50%';
        playButton.style.left = '50%';
        playButton.style.transform = 'translate(-50%, -50%)';
        playButton.style.padding = '10px 20px';
        playButton.style.fontSize = '1.2rem';
        playButton.style.cursor = 'pointer';
        document.body.appendChild(playButton);
        playButton.addEventListener('click', () => {
            video.play();
            playButton.remove();
        });
    });
});

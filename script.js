// Ensure video plays on page load
document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('background-video');
    video.play().catch(error => {
        console.error('Video playback failed:', error);
    });
});

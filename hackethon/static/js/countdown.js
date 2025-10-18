document.addEventListener('DOMContentLoaded', function() {
    const countdownContainer = document.getElementById('countdown-container');
    const countdownTimer = document.getElementById('countdown-timer');
    const streamContainer = document.getElementById('stream-container');

    // The countdownTime is passed from the Flask template
    const countdownTime = '{{ countdown_time }}';

    if (countdownTime && new Date(countdownTime) > new Date()) {
        streamContainer.style.display = 'none';
        countdownContainer.style.display = 'block';

        const targetDate = new Date(countdownTime).getTime();

        const interval = setInterval(function() {
            const now = new Date().getTime();
            const distance = targetDate - now;

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            countdownTimer.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;

            if (distance < 0) {
                clearInterval(interval);
                countdownContainer.style.display = 'none';
                streamContainer.style.display = 'block';
                // Optionally, refresh the page to load the stream
                window.location.reload();
            }
        }, 1000);
    }
});

document.addEventListener('DOMContentLoaded', function() {

    const container = document.querySelector('.carousel-container');
    const slides = Array.from(container.querySelectorAll('.slide'));
    let currentIndex = 0;
    const intervalTime = 5000;
    let rotationInterval;

    function startRotation() {
        rotationInterval = setInterval(() => {
            slides[currentIndex].classList.remove('active');
            currentIndex = (currentIndex + 1) % slides.length;
            slides[currentIndex].classList.add('active');
        }, intervalTime);
    }

    container.addEventListener('mouseenter', () => clearInterval(rotationInterval));
    container.addEventListener('mouseleave', startRotation);

    startRotation();
})
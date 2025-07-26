// 有点没搞懂逻辑 不想管了有空再看吧
const scrollContainer = document.getElementById('typeScroll');
let isScrolling = false;

scrollContainer.addEventListener('wheel', (e) => {
    const maxScroll = scrollContainer.scrollWidth - scrollContainer.clientWidth;
    const delta = Math.sign(e.deltaY);
    
    const atStart = scrollContainer.scrollLeft === 0;
    const atEnd = scrollContainer.scrollLeft >= maxScroll - 5;
    
    const scrollingRight = delta > 0;
    const scrollingLeft = delta < 0;

    if ((atEnd && scrollingRight) || (atStart && scrollingLeft)) {
        return;
    }

    scrollContainer.scrollLeft += delta * 30;
    e.preventDefault();
    
    if (!isScrolling) {
        isScrolling = true;
        setTimeout(() => isScrolling = false, 100);
    }
});

function updateEdgeIndicator() {
    const maxScroll = scrollContainer.scrollWidth - scrollContainer.clientWidth;
    scrollContainer.style.boxShadow = 
        (scrollContainer.scrollLeft > 0 ? 'inset 15px 0 10px -10px rgba(105, 92, 254, 0.1), ' : '') +
        (scrollContainer.scrollLeft < maxScroll ? 'inset -15px 0 10px -10px rgba(105, 92, 254, 0.1)' : '');
}

scrollContainer.addEventListener('scroll', updateEdgeIndicator);
updateEdgeIndicator();
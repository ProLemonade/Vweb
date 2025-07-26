// Sidebar
const body = document.querySelector('body'),
sidebar = body.querySelector('.sidebar'),
toggle = body.querySelector(".toggle"),
bubbleArrow = document.querySelector('.bubble-arrow'),
menuLinks = document.querySelectorAll('.menu-link a'),
bubbleContents = document.querySelectorAll('.bubble-content');

// 开合
toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
})
// 回家
document.querySelector('.lower').onclick = () => {
    window.location.href = '/';
};
// 小三角位置
function updateArrowPosition() {
    const activeLink = document.querySelector('.menu-link a.active');
        if (activeLink) {
            const sidebarHeight = document.querySelector('.sidebar').offsetHeight;
            const upperHeight = document.querySelector('.upper').offsetHeight;
            const dividerHeight = document.querySelector('.sidebar-divider').offsetHeight;
            const startY = window.innerHeight / 2 - sidebarHeight / 2 + upperHeight + 40 + dividerHeight ;
            const i = Array.from(menuLinks).findIndex(link => link.classList.contains('active'));

            bubbleArrow.style.top = (startY + 55*i + 25) + 'px';
        }
    }
window.addEventListener('resize', updateArrowPosition);


// 激活菜单第一项
menuLinks[0].classList.add('active');
bubbleContents[0].classList.add('active');
setTimeout(updateArrowPosition, 100); 

// 滚动监听第一项
document.addEventListener('DOMContentLoaded', () => {
    const activeContent = document.querySelector('.bubble-content.active');
    if (activeContent) {
        scrollListener(activeContent);
    }
});


// 点击切换菜单项
menuLinks.forEach((link, index) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();

        menuLinks.forEach(l => l.classList.remove('active'));
        bubbleContents.forEach(content => content.classList.remove('active'));

        link.classList.add('active');
        bubbleContents[index].classList.add('active');

        updateArrowPosition();
        
        // 滚动监听预备换新
        const previousActive = document.querySelector('.bubble-content.active');
        if (previousActive && previousActive.scrollHandler) {
            previousActive.removeEventListener('scroll', previousActive.scrollHandler);
        }

        // 滚动监听换新函数
        scrollListener(bubbleContents[index]);
    });
});



// 滚动监听我恨你我恨你我恨你我恨你我恨你我恨你我恨你我恨你我恨你我恨你
function scrollListener(activeContent) {
    const backTopBtn = activeContent.querySelector('.backToTop');
    
    if (activeContent && backTopBtn) {
        const scrollable = activeContent.scrollHeight > activeContent.clientHeight;
        
        if (scrollable) {
            const scrollHandler = function() {
                if (activeContent.scrollTop > 30) {
                    backTopBtn.classList.add('active');
                } else {
                    backTopBtn.classList.remove('active');
                }
            };
            
            // 为确保不受原有监听器干扰 搞不懂但是不加就会错 哈哈
            activeContent.scrollHandler = scrollHandler;
            
            activeContent.addEventListener('scroll', activeContent.scrollHandler);
            
            backTopBtn.onclick = function() {
                activeContent.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            };
        } else {
            backTopBtn.classList.remove('active');
        }
    }
}

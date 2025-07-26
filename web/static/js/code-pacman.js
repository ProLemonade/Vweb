// simu 吃豆人翻页
document.addEventListener('DOMContentLoaded', function() {
    const pac = document.getElementById("pac-button");
    const peas = document.querySelectorAll('.pea');
    const contents = document.querySelectorAll('.simu-content');
    const picture = document.getElementById('pic');
    const peaLabel = document.querySelector('.pea-label');

    contents.forEach(c => c.style.display = 'none');
    picture.style.display = 'block';

    peas.forEach(pea => {
        pea.addEventListener('click', function() {
            const step = this.getAttribute('simu-step'); // 读取目前步骤

            peas.forEach(p => p.classList.remove('active'));
            pea.classList.add('active');

            contents.forEach(c => c.style.display = 'none');
            document.getElementById(step).style.display = 'block';

            peaLabel.textContent = step;
            peaLabel.classList.add("visible");
        });
    });

    pac.addEventListener("click", function() {
        peas.forEach(p => p.classList.remove("active"));
        contents.forEach(c => c.style.display = 'none');
        peaLabel.classList.remove("visible");

        picture.style.display = 'block';
    });
});

// visual 吃豆人切换
const pacman = document.getElementById("pacman-button");
const beans = document.querySelectorAll(".bean");
const imgBoxes = document.querySelectorAll(".img-box");
const beanLabel = document.querySelector(".bean-label");


beans.forEach(bean => {
    bean.addEventListener("click", function() {
        pacman.classList.remove("active");
        beans.forEach(b => b.classList.remove("active"));
        bean.classList.add("active");

        let chosenType = bean.getAttribute("data-type"); // 读取目前种类
        imgBoxes.forEach(box => {
            let boxType = box.querySelector("img").getAttribute("data-type");
            if(boxType.toLowerCase() === chosenType.toLowerCase()) {
                box.style.display = "block";
            } else {
            box.style.display = "none";
            }
        });

        beanLabel.textContent = chosenType;
        beanLabel.classList.add("visible");
    });
});


pacman.addEventListener("click", function() {
    beans.forEach(bean => bean.classList.remove("active"));
    pacman.classList.add("active");
    imgBoxes.forEach(box => box.style.display = "block");
    
    beanLabel.textContent = "";
    beanLabel.classList.remove("visible");
});
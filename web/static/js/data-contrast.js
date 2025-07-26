document.addEventListener('DOMContentLoaded', initPage);

function initPage() {

    document.getElementById('prev-arrow').addEventListener('click', function() {
        navigatePage(-1);
    });
    
    document.getElementById('next-arrow').addEventListener('click', function() {
        navigatePage(1);
    });
}
let currentPage = 0;
function navigatePage(direction) {
    const pages = document.querySelectorAll('.page');
    if (pages.length === 0) return;
    
    let newPage = currentPage + direction;
    
    if (newPage < 0) newPage = pages.length - 1;
    if (newPage >= pages.length) newPage = 0;
    
    if (newPage !== currentPage) {
        showPage(newPage);
    }
}
function showPage(pageIndex) {
    const pages = document.querySelectorAll('.page');
    const dots = document.querySelectorAll('.dot');
    
    currentPage = pageIndex;
    
    pages.forEach((page, index) => {
        page.classList.toggle('active', index === pageIndex);
    });
    
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === pageIndex);
    });
}


document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('#typeSelector .data-type-box');
    const contrastResults = document.querySelector('.data-contrast-results');
    
    if (buttons.length > 0) {
        buttons[0].classList.add('active');
        contrastResults.classList.add('visible');
        const selectedType = buttons[0].innerText;
        generateContrasts(selectedType);
    }
    
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.classList.contains('active')) {
                this.classList.remove('active');

                contrastResults.classList.remove('visible');
            } else {
                buttons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                contrastResults.classList.add('visible');
                
                const selectedType = this.innerText;
                generateContrasts(selectedType);
            }
        });
    });
});
function generateContrasts(excludedType) {
    
    const otherAttributeCombinations = new Map();
    
    DATASET.forEach(point => {
        const selectedAttr = point.attributes.find(attr => attr.type === excludedType);
        
        if (!selectedAttr) return;
        
        const otherAttributes = point.attributes
            .filter(attr => attr.type !== excludedType)
            .sort((a, b) => a.type.localeCompare(b.type));
        
        const combinationKey = otherAttributes.map(attr => `${attr.type}:${attr.value}`).join('|');
        
        if (!otherAttributeCombinations.has(combinationKey)) {
            otherAttributeCombinations.set(combinationKey, {
                conditions: otherAttributes.map(attr => ({ type: attr.type, value: attr.value })),
                points: new Map()
            });
        }
        
        const pointsMap = otherAttributeCombinations.get(combinationKey).points;
        if (!pointsMap.has(selectedAttr.value)) {
            pointsMap.set(selectedAttr.value, []);
        }
        pointsMap.get(selectedAttr.value).push(point);
    });
    
    const contrastGroups = [];
    
    otherAttributeCombinations.forEach((data, key) => {
        if (data.points.size >= 2) {

            const values = Array.from(data.points.entries());
            const contrastGroup = {
                conditions: data.conditions,
                valueGroups: values.map(([value, points]) => ({
                    value,
                    points
                }))
            };
            contrastGroups.push(contrastGroup);
        }
    });
    
    displayContrastGroups(contrastGroups, excludedType);
}
function displayContrastGroups(contrastGroups, excludedType) {
    const container = document.getElementById('contrast-pages');
    const yesResults = document.getElementById('data-yes');
    const noResults = document.getElementById('data-no');
    // 根据对比组数初始化
    container.innerHTML = '';
    currentPage = 0;
    
    if (contrastGroups.length === 0) {
        noResults.style.display = 'flex';
        yesResults.style.display = 'none';

        document.getElementById('pagination-dots').innerHTML = '';
        return;
    }
    
    noResults.style.display = 'none';
    
    initPagination(contrastGroups.length);
    
    contrastGroups.forEach((group, index) => {
        const pageEl = document.createElement('div');
        pageEl.className = `page ${index === 0 ? 'active' : ''}`;  // 编号 选中第一页
        
        // 创建对比组内容
        const groupEl = document.createElement('div');
        groupEl.className = 'contrast-group';
        
        const titleEl = document.createElement('div');
        titleEl.className = 'contrast-title';
        titleEl.textContent = `Group ${index + 1}`;
        groupEl.appendChild(titleEl);
        
        const conditionsEl = document.createElement('div');
        conditionsEl.className = 'contrast-conditions';
        const conditionTexts = group.conditions.map(cond => `${cond.type}: ${cond.value}`);
        conditionsEl.textContent = `Same: ${conditionTexts.join('; ')}`;
        groupEl.appendChild(conditionsEl);
        
        group.valueGroups.forEach(valueGroup => {
            const subgroup = document.createElement('div');
            subgroup.className = 'contrast-subgroup';
            
            const label = document.createElement('div');
            label.className = 'contrast-label';
            label.textContent = `${excludedType}: ${valueGroup.value}`;
            
            const points = document.createElement('div');
            points.className = 'contrast-points';
            points.textContent = valueGroup.points.map(p => p.name).join(', ');
            
            subgroup.appendChild(label);
            subgroup.appendChild(points);
            groupEl.appendChild(subgroup);
        });
        
        pageEl.appendChild(groupEl);
        container.appendChild(pageEl);
    });
}
function initPagination(groupCount) {
    const dotsContainer = document.getElementById('pagination-dots');
    dotsContainer.innerHTML = '';
    
    for (let i = 0; i < groupCount; i++) {
        const dot = document.createElement('span');
        dot.className = `dot ${i === 0 ? 'active' : ''}`; // 编号 选中第一页
        dot.addEventListener('click', () => showPage(i)); // 绑定点击事件
        dotsContainer.appendChild(dot);
    }
    
    // 隐不隐藏都可以 const showArrows = groupCount > 1;
    // document.querySelector('.pagination-arrows').style.display = showArrows ? 'flex' : 'none';
}

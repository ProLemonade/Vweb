function initConditionSelect() {
    const select = document.getElementById('conditionSelect');
    CONDITIONS.forEach(condition => {
        const option = document.createElement('option');
        option.value = condition;
        option.textContent = condition;
        select.appendChild(option);
    });
}

function updateAddButtonState() {
    const addBtn = document.getElementById('addBtn');
    const currentCount = document.querySelectorAll('.card').length;
    addBtn.disabled = currentCount >= 3;
    addBtn.classList.toggle('disabled', currentCount >= 3);
}

function createCloseHandler(card, condition) {
    return function() {
        const option = document.querySelector(
            `#conditionSelect option[value="${condition}"]`
        );
        if (option) option.disabled = false;
        card.remove();
        updateAddButtonState();
    }
}

function addCard() {
    const container = document.getElementById('container');
    const select = document.getElementById('conditionSelect');
    const selectedCondition = select.value;
    
    if (document.querySelectorAll('.card').length >= 3) {
        alert('Cannot add more.');
        return;
    }
    const exists = [...document.querySelectorAll('.card')].some(card => 
        card.dataset.condition === selectedCondition
    );
    if (exists) {
        alert('Already added.');
        return;
    }

    const card = document.createElement('div');
    card.className = 'card';
    card.dataset.condition = selectedCondition;
    card.innerHTML = `
        <div class="close-btn">×</div>
        <h3>${selectedCondition}</h3>
        <div class="analysis-list">
            <div class="analysis-item">
                Data-info 
                <button class="check-btn" onclick="toggleAnalysis(this, 'data-info')">✓</button>
            </div>

            <div class="analysis-item">
                wcross
                <button class="check-btn" onclick="toggleAnalysis(this, 'wcross')">✓</button>
            </div>

            <div class="analysis-item">
                TKE
                <button class="check-btn" onclick="toggleAnalysis(this, 'TKE')">✓</button>
            </div>

            <div class="analysis-item">
                Profile 
                <button class="check-btn" onclick="toggleAnalysis(this, 'profile')">✓</button>
            </div>
        </div>
    `;

    card.querySelector('.close-btn').onclick = 
        createCloseHandler(card, selectedCondition);

        select.querySelector(`option[value="${selectedCondition}"]`).disabled = true;
    
    container.appendChild(card);
    updateAddButtonState();
}

function toggleAnalysis(btn, analysisType) {
    btn.classList.toggle('active');
    
    const card = btn.closest('.card');
    const condition = card.dataset.condition;
    const analysisItem = btn.closest('.analysis-item');
    
    let imageContainer = analysisItem.nextElementSibling;

    // 清空
    if (imageContainer && imageContainer.classList.contains('image-container')) {
        imageContainer.remove();
    } else if (btn.classList.contains('active')) {
        // 重新创建
        imageContainer = document.createElement('div');
        imageContainer.className = 'image-container';
        
        const img = document.createElement('img');
        img.src = `../static/images/${condition}_${analysisType}.png`;
        img.alt = `${condition}_${analysisType}`;
        
        const filename = document.createElement('div');
        filename.className = 'filename';
        filename.textContent = `${condition}_${analysisType}.png`;
        
        imageContainer.appendChild(img);
        imageContainer.appendChild(filename);
        
        analysisItem.after(imageContainer);
    }
}

initConditionSelect();
document.getElementById('addBtn').addEventListener('click', addCard);
updateAddButtonState();
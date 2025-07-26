
// 待读
document.querySelectorAll('#typeFilter .data-type-box').forEach(box => {
    box.addEventListener('click', function() {
        const container = this.closest('.data-type-boxes');
        const typeId = this.getAttribute('type-id');
        
        container.classList.toggle('active');
        this.classList.toggle('active');

        if (container.classList.contains('active')) {
            activeFilters[typeId] = filterOptions[typeId].options[filterOptions[typeId].currentIndex].id;
            updateOptionsDisplay(typeId);
        } else {
            delete activeFilters[typeId];
        }

        filterData();
    });
});

document.querySelectorAll('.option-arrow').forEach(arrow => {
    arrow.addEventListener('click', function(e) {
        e.stopPropagation();
        
        const container = this.closest('.data-type-boxes');
        const typeId = container.querySelector('.data-type-box').getAttribute('type-id');
        const options = filterOptions[typeId];
        const delta = this.classList.contains('prev') ? -1 : 1;

        options.currentIndex = (options.currentIndex + delta + options.options.length) % options.options.length;
        activeFilters[typeId] = options.options[options.currentIndex].id;
        
        updateOptionsDisplay(typeId);
        filterData();
    });
});

function updateOptionsDisplay(typeId) {
    const container = document.querySelector(`.data-type-box[type-id="${typeId}"]`).closest('.data-type-boxes');
    container.querySelector('.option-value').innerHTML = filterOptions[typeId].options[filterOptions[typeId].currentIndex].value;
}

function filterData() {
    const activeTypes = Object.keys(activeFilters);
    const dataItems = document.querySelectorAll('.data-item-result');
    let matchCount = 0;
    
    dataItems.forEach(item => {
        if (activeTypes.length === 0) {
            item.style.display = 'flex';
            matchCount++;
            return;
        }
        
        let match = true;
        activeTypes.forEach(typeId => {
            const selectedValueId = activeFilters[typeId];
            const itemTypeAttr = `data-type${typeId}`;
            
            if (!item.hasAttribute(itemTypeAttr) || item.getAttribute(itemTypeAttr) != selectedValueId) {
                match = false;
            }
        });

        item.style.display = match ? 'flex' : 'none';
        if (match) matchCount++;
    });
    
    document.getElementById('data-no').style.display = matchCount === 0 ? 'flex' : 'none';
    document.getElementById('data-yes').style.display = matchCount === 0 ? 'none' :'flex';
}

filterData();

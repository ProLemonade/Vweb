
// 内容填充
    
document.addEventListener('DOMContentLoaded', () => {
    const codeBoxes = document.querySelectorAll('.img-box');
    const imgBoxMore = document.querySelector('.img-box-more');
    const btnBack = document.querySelector('.btn-back');
    const lanEl = document.getElementById('lan');
    const tagsEl = document.getElementById('tags');
    const codeEditorEl = document.getElementById('code-editor');
    const codeResultEl = document.getElementById('code-result');
    const codeCopyBtn = document.getElementById('code-copy');

    // 代码框
    window.editor = CodeMirror(codeEditorEl, {
        lineNumbers: true,
        mode: "python",
        theme: "default",
        autofocus: true,
        indentUnit: 4,
        readOnly: false,
        viewportMargin: Infinity 
    });

    setTimeout(() => {
        editor.refresh();
        editor.focus();
    }, 100);
    // 点击事件
    codeBoxes.forEach(box => {
        box.addEventListener('click', e => {
            e.stopPropagation(); // 禁止冒泡 不知道干啥的但是不加就不对 哈哈…
            const fileName = box.querySelector('.img-caption')?.textContent;
            const fileData = window.codeFiles.find(f => f.name === fileName);
            
            lanEl.textContent = fileData.language.toUpperCase();
            tagsEl.textContent = fileData.content_tags;
            codeResultEl.innerHTML = `<img src="../static/img/${fileName}.png" alt="Result Image">`;
            
            const modeMap = { python: 'python', julia: 'julia', matlab: 'octave' };
            editor.setValue(fileData.content_code);
            editor.setOption('mode', modeMap[fileData.language] || 'python');
            
            currentLanguage = fileData.language;
            
            imgBoxMore.classList.add('active');
            });
        });
        
        btnBack.addEventListener('click', () => {
            imgBoxMore.classList.remove('active');
        });
    });
    

// 在线编程
let currentLanguage = 'python'; 
    
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function runCode() {
    const currentCode = editor.getValue(); 
    const codeResultEl = document.getElementById('code-result');
    codeResultEl.innerHTML = '<div class="spinner"></div>'; 
        
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `action=run_code&code=${encodeURIComponent(currentCode)}&language=${currentLanguage}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.image) {
            codeResultEl.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="Output Image">`;
        } else {
            codeResultEl.textContent = data.output || data.error;
        }
    })
    .catch(err => {
        console.error(err);
        codeResultEl.textContent = "Something Wrong ……";
    });
}

function copyCode() {
    const code = editor.getValue();
    navigator.clipboard.writeText(code)
        .then(() => {
            codeCopyBtn.classList.add('copied');
            
            setTimeout(() => {
                codeCopyBtn.classList.remove('copied');
            }, 2000);
        })
    }

// 类似
function copyPhase() {
    const code = phEditor.getValue();
    navigator.clipboard.writeText(code)
        .then(() => {
            const phaseCopyBtn = document.querySelector('.phase-copy');
            const phaseCopyIcon = phaseCopyBtn.querySelector('.code-phase-icon');
            
            phaseCopyIcon.classList.replace('fa-clipboard', 'fa-check');

            setTimeout(() => {
                phaseCopyIcon.classList.replace('fa-check', 'fa-clipboard');
            }, 1500);
        })
    }

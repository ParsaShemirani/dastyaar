document.addEventListener('DOMContentLoaded', function() {
    const consoleContainer = document.getElementById('console-container');
    const codeForm = document.getElementById('code-form');
    const codeInput = document.getElementById('codeline');
    
    const dastyaarContainer = document.getElementById('dastyaar-container');
    const dastyaarForm = document.getElementById('dastyaar-form');
    const dastyaarInput = document.getElementById('dastyaar-input');
    
    // Initial setup
    scrollToBottom();
    scrollDastyaarToBottom();
    codeInput.focus();
    
    // Handle form submission
    codeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const codeline = formData.get('codeline').trim();
        
        if (!codeline) return;
        
        fetch('/codeline', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            updateConsoleContent(html);
            codeInput.value = '';
            codeInput.focus();
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    // Handle Dastyaar form submission
    dastyaarForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const message = formData.get('input_message').trim();
        
        if (!message) return;
        
        fetch('/input_message', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            updateDastyaarContent(html);
            dastyaarInput.value = '';
            dastyaarInput.focus();
            scrollDastyaarToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    function updateConsoleContent(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.getElementById('console-container').innerHTML;
        consoleContainer.innerHTML = newContent;
    }
    
    function updateDastyaarContent(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.getElementById('dastyaar-container').innerHTML;
        dastyaarContainer.innerHTML = newContent;
    }
    
    function scrollToBottom() {
        consoleContainer.scrollTop = consoleContainer.scrollHeight;
    }
    
    function scrollDastyaarToBottom() {
        dastyaarContainer.scrollTop = dastyaarContainer.scrollHeight;
    }
});
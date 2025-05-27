document.addEventListener('DOMContentLoaded', function() {
    const consoleContainer = document.getElementById('console-container');
    const codeForm = document.getElementById('code-form');
    const codeInput = document.getElementById('codeline');
    
    // Initial setup
    scrollToBottom();
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
    
    function updateConsoleContent(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.getElementById('console-container').innerHTML;
        consoleContainer.innerHTML = newContent;
    }
    
    function scrollToBottom() {
        consoleContainer.scrollTop = consoleContainer.scrollHeight;
    }
});
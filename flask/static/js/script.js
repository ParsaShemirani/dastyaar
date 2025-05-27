// Scroll to bottom of console on page load
document.addEventListener('DOMContentLoaded', function() {
    const consoleContainer = document.getElementById('console-container');
    consoleContainer.scrollTop = consoleContainer.scrollHeight;
    
    // Focus on input field
    document.getElementById('codeline').focus();
    
    // Handle form submission without page refresh
    const codeForm = document.getElementById('code-form');
    codeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch('/codeline', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Extract just the console content from the response
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newConsoleContent = doc.getElementById('console-container').innerHTML;
            
            // Update just the console content
            document.getElementById('console-container').innerHTML = newConsoleContent;
            
            // Scroll to bottom
            consoleContainer.scrollTop = consoleContainer.scrollHeight;
            
            // Clear and focus the input field
            document.getElementById('codeline').value = '';
            document.getElementById('codeline').focus();
        });
    });
});
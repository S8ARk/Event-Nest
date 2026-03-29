// Theme Switcher Logic
const themeToggle = document.getElementById('themeToggle');
const currentTheme = localStorage.getItem('theme') || 'light';

if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    themeToggle.textContent = '☀️';
}

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    let theme = 'light';
    if (document.body.classList.contains('dark-mode')) {
        theme = 'dark';
        themeToggle.textContent = '☀️';
    } else {
        themeToggle.textContent = '🌙';
    }
    localStorage.setItem('theme', theme);
});

// Global Toast Notification System
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');

    // Handle flask categories mapped to toast CSS classes
    if (type === 'error') type = 'danger';
    if (type === 'message') type = 'info';

    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <span style="cursor:pointer; margin-left: 1rem; font-weight:bold;" onclick="this.parentElement.remove()">&times;</span>
    `;

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Navbar glass-morphism scroll effect
window.addEventListener('scroll', function () {
    const nav = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Prevent Double Click Submission Bugs
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            // Find all submit buttons within this form
            const submitBtns = this.querySelectorAll('button[type="submit"], input[type="submit"]');
            
            // If already processing, stop further events
            if (this.dataset.submitting === "true") {
                e.preventDefault();
                return;
            }
            
            // Mark as submitting
            this.dataset.submitting = "true";
            
            // Disable buttons and show processing state
            submitBtns.forEach(btn => {
                btn.dataset.originalText = btn.value || btn.innerHTML;
                btn.disabled = true;
                if (btn.tagName.toLowerCase() === 'input') {
                    btn.value = "Processing...";
                } else {
                    btn.innerHTML = "Processing...";
                }
                btn.style.opacity = '0.7';
                btn.style.cursor = 'not-allowed';
            });
        });
    });
});

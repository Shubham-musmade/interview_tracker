// Modern JavaScript Enhancements for Job Application Tracker

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeAnimations();
    initializeInteractions();
    initializeFormEnhancements();
    initializeSearchAndFilters();
    initializeNotifications();
    initializeThemeSystem();
});

// Animation System
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.card, .stats-card, .main-container').forEach(el => {
        observer.observe(el);
    });

    // Stagger animations for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// Interactive Enhancements
function initializeInteractions() {
    // Enhanced button interactions
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Card hover effects
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Enhanced dropdown interactions
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const menu = this.nextElementSibling;
            if (menu) {
                menu.style.transform = 'translateY(-10px)';
                menu.style.opacity = '0';
                
                setTimeout(() => {
                    menu.style.transform = 'translateY(0)';
                    menu.style.opacity = '1';
                }, 50);
            }
        });
    });
}

// Form Enhancements
function initializeFormEnhancements() {
    // Floating labels effect
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        // Add focus/blur effects
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
            
            // Add ripple effect
            const ripple = document.createElement('div');
            ripple.className = 'input-ripple';
            this.parentElement.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
        });

        // Real-time validation feedback
        input.addEventListener('input', function() {
            validateField(this);
        });
    });

    // Enhanced file upload
    document.querySelectorAll('input[type="file"]').forEach(fileInput => {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            if (fileName) {
                showFileUploadFeedback(this, fileName);
            }
        });
    });

    // Form submission loading states
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
                
                // Add loading spinner
                const spinner = document.createElement('span');
                spinner.className = 'spinner-border spinner-border-sm me-2';
                spinner.setAttribute('role', 'status');
                submitBtn.insertBefore(spinner, submitBtn.firstChild);
            }
        });
    });
}

// Search and Filter System
function initializeSearchAndFilters() {
    // Enhanced search functionality
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase();
            
            // Add loading state
            this.classList.add('searching');
            
            searchTimeout = setTimeout(() => {
                performSearch(query, this);
                this.classList.remove('searching');
            }, 300);
        });
    });

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const filterValue = this.dataset.filter;
            applyFilter(filterValue);
            
            // Update active state
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Sort functionality
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const sortBy = this.dataset.sort;
            const sortOrder = this.classList.contains('asc') ? 'desc' : 'asc';
            
            applySorting(sortBy, sortOrder);
            
            // Update sort indicators
            this.classList.toggle('asc');
            this.classList.toggle('desc');
        });
    });
}

// Notification System
function initializeNotifications() {
    // Auto-hide alerts with progress bar
    document.querySelectorAll('.alert').forEach(alert => {
        if (alert.classList.contains('alert-dismissible')) {
            addProgressBar(alert);
            
            setTimeout(() => {
                fadeOutAlert(alert);
            }, 5000);
        }
    });

    // Toast notifications
    window.showToast = function(message, type = 'info', duration = 3000) {
        const toast = createToast(message, type);
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };
}

// Theme System
function initializeThemeSystem() {
    // Theme toggle functionality (if needed)
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            toggleTheme();
        });
    }

    // Respect system theme preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
        // User prefers light mode - we're using dark theme, so add override
        document.documentElement.setAttribute('data-theme-override', 'dark');
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (e.matches) {
            document.documentElement.removeAttribute('data-theme-override');
        }
    });
}

// Utility Functions
function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    const isRequired = field.hasAttribute('required');
    
    let isValid = true;
    let message = '';

    // Basic validation
    if (isRequired && !value) {
        isValid = false;
        message = 'This field is required';
    } else if (fieldType === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        message = 'Please enter a valid email address';
    } else if (fieldType === 'tel' && value && !isValidPhone(value)) {
        isValid = false;
        message = 'Please enter a valid phone number';
    }

    // Update field state
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }

    // Show/hide feedback
    const feedback = field.parentElement.querySelector('.invalid-feedback') || 
                    field.parentElement.querySelector('.valid-feedback');
    if (feedback) {
        feedback.textContent = message;
    }

    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

function showFileUploadFeedback(input, fileName) {
    let feedback = input.parentElement.querySelector('.file-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'file-feedback text-success mt-2';
        input.parentElement.appendChild(feedback);
    }
    
    feedback.innerHTML = `<i class="bi bi-check-circle me-1"></i> ${fileName}`;
    feedback.style.opacity = '0';
    feedback.style.transform = 'translateY(-10px)';
    
    setTimeout(() => {
        feedback.style.opacity = '1';
        feedback.style.transform = 'translateY(0)';
    }, 100);
}

function performSearch(query, input) {
    const searchTargets = document.querySelectorAll('.searchable');
    
    searchTargets.forEach(target => {
        const text = target.textContent.toLowerCase();
        const matches = text.includes(query);
        
        if (matches || query === '') {
            target.style.display = '';
            target.classList.remove('filtered-out');
        } else {
            target.style.display = 'none';
            target.classList.add('filtered-out');
        }
    });

    // Update search results count
    const visibleItems = document.querySelectorAll('.searchable:not(.filtered-out)').length;
    updateSearchResultsCount(visibleItems);
}

function applyFilter(filterValue) {
    const filterTargets = document.querySelectorAll('.filterable');
    
    filterTargets.forEach(target => {
        const targetFilter = target.dataset.filter;
        const matches = filterValue === 'all' || targetFilter === filterValue;
        
        if (matches) {
            target.style.display = '';
            target.classList.remove('filtered-out');
        } else {
            target.style.display = 'none';
            target.classList.add('filtered-out');
        }
    });
}

function applySorting(sortBy, sortOrder) {
    const sortContainer = document.querySelector('.sortable-container');
    if (!sortContainer) return;
    
    const items = Array.from(sortContainer.children);
    
    items.sort((a, b) => {
        const aValue = a.dataset[sortBy] || a.textContent;
        const bValue = b.dataset[sortBy] || b.textContent;
        
        const comparison = aValue.localeCompare(bValue, undefined, { numeric: true });
        return sortOrder === 'asc' ? comparison : -comparison;
    });
    
    items.forEach(item => sortContainer.appendChild(item));
}

function addProgressBar(alert) {
    const progressBar = document.createElement('div');
    progressBar.className = 'alert-progress';
    progressBar.style.cssText = `
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
        background: currentColor;
        opacity: 0.3;
        animation: progress 5s linear;
        width: 100%;
    `;
    
    alert.style.position = 'relative';
    alert.appendChild(progressBar);
    
    // Add CSS animation
    if (!document.querySelector('#progress-animation')) {
        const style = document.createElement('style');
        style.id = 'progress-animation';
        style.textContent = `
            @keyframes progress {
                from { width: 100%; }
                to { width: 0%; }
            }
        `;
        document.head.appendChild(style);
    }
}

function fadeOutAlert(alert) {
    alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-20px)';
    
    setTimeout(() => {
        alert.remove();
    }, 300);
}

function createToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="bi bi-${getToastIcon(type)} me-2"></i>
            <span>${message}</span>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="bi bi-x"></i>
        </button>
    `;
    
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 300px;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        background: var(--surface-secondary);
        border-left: 4px solid var(--accent-${type === 'error' ? 'danger' : type});
        color: var(--text-primary);
    `;
    
    return toast;
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || icons.info;
}

function updateSearchResultsCount(count) {
    const counter = document.querySelector('.search-results-count');
    if (counter) {
        counter.textContent = `${count} result${count !== 1 ? 's' : ''}`;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals/dropdowns
    if (e.key === 'Escape') {
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

// Add additional CSS for enhancements
const enhancementStyles = document.createElement('style');
enhancementStyles.textContent = `
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .input-focused {
        transform: scale(1.02);
    }
    
    .input-ripple {
        position: absolute;
        top: 50%;
        left: 10px;
        width: 20px;
        height: 20px;
        background: rgba(88, 166, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple {
        0% {
            transform: translate(-50%, -50%) scale(0);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -50%) scale(4);
            opacity: 0;
        }
    }
    
    .searching {
        position: relative;
    }
    
    .searching::after {
        content: '';
        position: absolute;
        right: 10px;
        top: 50%;
        width: 16px;
        height: 16px;
        border: 2px solid var(--accent-primary);
        border-top: 2px solid transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        transform: translateY(-50%);
    }
    
    @keyframes spin {
        0% { transform: translateY(-50%) rotate(0deg); }
        100% { transform: translateY(-50%) rotate(360deg); }
    }
    
    .toast-notification.show {
        transform: translateX(0);
    }
    
    .toast-close {
        background: none;
        border: none;
        color: var(--text-secondary);
        font-size: 1.2rem;
        padding: 0;
        margin-left: auto;
        cursor: pointer;
    }
    
    .toast-content {
        display: flex;
        align-items: center;
        flex: 1;
    }
`;
document.head.appendChild(enhancementStyles);
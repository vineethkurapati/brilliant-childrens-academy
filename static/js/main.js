// Main JavaScript for Brilliant Childrens Academy

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize photo gallery animations
    initializePhotoGallery();
    
    // Initialize form validations
    initializeFormValidation();
    
    // Initialize file upload features
    initializeFileUpload();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

// Photo Gallery Animations
function initializePhotoGallery() {
    const photoItems = document.querySelectorAll('.photo-item');
    
    photoItems.forEach((item, index) => {
        // Add random animation delays
        const delay = Math.random() * 2;
        item.style.animationDelay = delay + 's';
        
        // Add click event for photo cards
        const photoCard = item.querySelector('.photo-card');
        if (photoCard) {
            photoCard.addEventListener('click', function() {
                this.classList.add('pulse');
                setTimeout(() => {
                    this.classList.remove('pulse');
                }, 1000);
            });
        }
    });
}

// Form Validation
function initializeFormValidation() {
    // Bootstrap form validation
    var forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            checkPasswordStrength(this);
        });
    });
}

// Password Strength Checker
function checkPasswordStrength(input) {
    const password = input.value;
    const strengthIndicator = input.parentNode.querySelector('.password-strength');
    
    if (!strengthIndicator) return;
    
    let strength = 0;
    let feedback = '';
    
    // Check password criteria
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    // Set feedback based on strength
    switch(strength) {
        case 0:
        case 1:
            feedback = 'Very Weak';
            strengthIndicator.className = 'password-strength text-danger';
            break;
        case 2:
            feedback = 'Weak';
            strengthIndicator.className = 'password-strength text-warning';
            break;
        case 3:
            feedback = 'Fair';
            strengthIndicator.className = 'password-strength text-info';
            break;
        case 4:
            feedback = 'Good';
            strengthIndicator.className = 'password-strength text-primary';
            break;
        case 5:
            feedback = 'Strong';
            strengthIndicator.className = 'password-strength text-success';
            break;
    }
    
    strengthIndicator.textContent = feedback;
}

// File Upload Features
function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            handleFileSelection(e);
        });
        
        // Add drag and drop support
        const dropZone = input.closest('.card-body');
        if (dropZone) {
            setupDragAndDrop(dropZone, input);
        }
    });
}

// Handle File Selection
function handleFileSelection(event) {
    const files = event.target.files;
    const fileInfo = event.target.parentNode.querySelector('.file-info');
    
    if (files.length > 0) {
        const file = files[0];
        const fileSize = formatFileSize(file.size);
        const fileName = file.name;
        
        if (fileInfo) {
            fileInfo.innerHTML = `
                <div class="selected-file-info mt-2 p-2 bg-light rounded">
                    <i class="fas fa-file me-2"></i>
                    <strong>${fileName}</strong>
                    <span class="text-muted ms-2">(${fileSize})</span>
                </div>
            `;
        }
        
        // Validate file size (500MB limit)
        if (file.size > 500 * 1024 * 1024) {
            showAlert('File size exceeds 500MB limit', 'danger');
            event.target.value = '';
            if (fileInfo) fileInfo.innerHTML = '';
        }
    }
}

// Setup Drag and Drop
function setupDragAndDrop(dropZone, fileInput) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    dropZone.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        fileInput.files = files;
        handleFileSelection({ target: fileInput });
    }, false);
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    e.currentTarget.classList.add('border-primary', 'bg-light');
}

function unhighlight(e) {
    e.currentTarget.classList.remove('border-primary', 'bg-light');
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// Smooth scrolling for anchor links
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Loading state management
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading me-2"></span>Loading...';
    button.disabled = true;
    
    return function hideLoading() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Form submission with loading state
function submitFormWithLoading(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    const hideLoading = showLoading(submitButton);
    
    // Simulate processing time
    setTimeout(() => {
        hideLoading();
    }, 2000);
}

// Initialize search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const searchableItems = document.querySelectorAll('.searchable-item');
            
            searchableItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Export functions for global use
window.schoolApp = {
    showAlert,
    smoothScroll,
    showLoading,
    submitFormWithLoading,
    formatFileSize
};
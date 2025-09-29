// Login Page JavaScript Functionality

// Global variables
let currentTab = 'login';

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    // Set default tab
    switchTab('login');
    
    // Add event listeners
    addEventListeners();
    
    // Initialize form validation
    initializeValidation();
}

function addEventListeners() {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.textContent.toLowerCase();
            switchTab(tabName);
        });
    });
    
    // Form submission
    const loginForm = document.querySelector('.login-form');
    const registerForm = document.querySelector('.register-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Real-time validation
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

function switchTab(tabName) {
    // Update tab buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.toLowerCase() === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update form content
    const forms = document.querySelectorAll('.form-content');
    forms.forEach(form => {
        form.classList.remove('active');
    });
    
    const targetForm = document.getElementById(tabName + '-form');
    if (targetForm) {
        targetForm.classList.add('active');
    }
    
    currentTab = tabName;
    
    // Clear forms when switching
    clearForms();
}

function handleLogin(event) {
    event.preventDefault();
    
    // Prevent multiple submissions
    const submitBtn = event.target.querySelector('.submit-btn');
    if (submitBtn.disabled) {
        return;
    }
    
    const formData = new FormData(event.target);
    const email = formData.get('email');
    const password = formData.get('password');
    const rememberMe = formData.get('remember-me');
    
    // Validate form
    if (!validateLoginForm(email, password)) {
        return;
    }
    
    // Disable submit button to prevent multiple submissions
    submitBtn.disabled = true;
    submitBtn.textContent = 'Memproses...';
    
    // Record start time for minimum loading duration
    const startTime = Date.now();
    const minLoadingTime = 1000; // 1 second minimum
    
    // Show loading with existing animation
    showLoadingWithAnimation();
    
    // Make API call to login endpoint
    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
            remember_me: rememberMe
        })
    })
    .then(response => response.json())
    .then(data => {
        // Calculate elapsed time
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, minLoadingTime - elapsedTime);
        
        // Wait for minimum loading time + remaining time
        setTimeout(() => {
            hideLoading();
            
            if (data.success) {
                // Store login state
                if (rememberMe) {
                    localStorage.setItem('rememberMe', 'true');
                    localStorage.setItem('userEmail', email);
                    localStorage.setItem('userName', data.user.name);
                }
                
                // Show success notification only once
                showNotification(data.message, 'success');
                
                // Redirect to main page seamlessly
                setTimeout(() => {
                    // Use replace to avoid back button issues
                    window.location.replace('/main');
                }, 1000);
            } else {
                showNotification(data.message, 'error');
                // Re-enable submit button on error
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<span>Masuk</span>';
            }
        }, remainingTime);
    })
    .catch(error => {
        // Calculate elapsed time for error case too
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, minLoadingTime - elapsedTime);
        
        setTimeout(() => {
            hideLoading();
            console.error('Login error:', error);
            showNotification('Terjadi kesalahan saat login. Silakan coba lagi.', 'error');
            // Re-enable submit button on error
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>Masuk</span>';
        }, remainingTime);
    });
}

function handleRegister(event) {
    event.preventDefault();
    
    // Prevent multiple submissions
    const submitBtn = event.target.querySelector('.submit-btn');
    if (submitBtn.disabled) {
        return;
    }
    
    const formData = new FormData(event.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    // Validate form
    if (!validateRegisterForm(name, email, password, confirmPassword)) {
        return;
    }
    
    // Disable submit button to prevent multiple submissions
    submitBtn.disabled = true;
    submitBtn.textContent = 'Memproses...';
    
    // Record start time for minimum loading duration
    const startTime = Date.now();
    const minLoadingTime = 1000; // 1 second minimum
    
    // Show loading with existing animation
    showLoadingWithAnimation();
    
    // Make API call to register endpoint
    fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password,
            confirm_password: confirmPassword
        })
    })
    .then(response => response.json())
    .then(data => {
        // Calculate elapsed time
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, minLoadingTime - elapsedTime);
        
        // Wait for minimum loading time + remaining time
        setTimeout(() => {
            hideLoading();
            
            if (data.success) {
                showNotification(data.message, 'success');
                
                // Switch to login tab
                setTimeout(() => {
                    switchTab('login');
                    // Pre-fill email
                    document.getElementById('login-email').value = email;
                }, 1500);
            } else {
                showNotification(data.message, 'error');
                // Re-enable submit button on error
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<span>Daftar</span>';
            }
        }, remainingTime);
    })
    .catch(error => {
        // Calculate elapsed time for error case too
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, minLoadingTime - elapsedTime);
        
        setTimeout(() => {
            hideLoading();
            console.error('Register error:', error);
            showNotification('Terjadi kesalahan saat registrasi. Silakan coba lagi.', 'error');
            // Re-enable submit button on error
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>Daftar</span>';
        }, remainingTime);
    });
}

function validateLoginForm(email, password) {
    let isValid = true;
    
    // Clear previous errors
    clearFormErrors('login');
    
    // Validate email
    if (!email) {
        showFieldError('login-email', 'Email harus diisi');
        isValid = false;
    } else if (!isValidEmail(email)) {
        showFieldError('login-email', 'Format email tidak valid');
        isValid = false;
    }
    
    // Validate password
    if (!password) {
        showFieldError('login-password', 'Password harus diisi');
        isValid = false;
    } else if (password.length < 6) {
        showFieldError('login-password', 'Password minimal 6 karakter');
        isValid = false;
    }
    
    return isValid;
}

function validateRegisterForm(name, email, password, confirmPassword) {
    let isValid = true;
    
    // Clear previous errors
    clearFormErrors('register');
    
    // Validate name
    if (!name) {
        showFieldError('register-name', 'Nama lengkap harus diisi');
        isValid = false;
    } else if (name.length < 2) {
        showFieldError('register-name', 'Nama minimal 2 karakter');
        isValid = false;
    }
    
    // Validate email
    if (!email) {
        showFieldError('register-email', 'Email harus diisi');
        isValid = false;
    } else if (!isValidEmail(email)) {
        showFieldError('register-email', 'Format email tidak valid');
        isValid = false;
    }
    
    // Validate password
    if (!password) {
        showFieldError('register-password', 'Password harus diisi');
        isValid = false;
    } else if (password.length < 6) {
        showFieldError('register-password', 'Password minimal 6 karakter');
        isValid = false;
    } else if (!isStrongPassword(password)) {
        showFieldError('register-password', 'Password harus mengandung huruf dan angka');
        isValid = false;
    }
    
    // Validate confirm password
    if (!confirmPassword) {
        showFieldError('register-confirm-password', 'Konfirmasi password harus diisi');
        isValid = false;
    } else if (password !== confirmPassword) {
        showFieldError('register-confirm-password', 'Password tidak sama');
        isValid = false;
    }
    
    return isValid;
}

function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    const fieldId = field.id;
    
    // Clear previous error
    clearFieldError(event);
    
    // Validate based on field type
    if (fieldId.includes('email')) {
        if (value && !isValidEmail(value)) {
            showFieldError(fieldId, 'Format email tidak valid');
        }
    } else if (fieldId.includes('password')) {
        if (value && value.length < 6) {
            showFieldError(fieldId, 'Password minimal 6 karakter');
        }
    } else if (fieldId.includes('name')) {
        if (value && value.length < 2) {
            showFieldError(fieldId, 'Nama minimal 2 karakter');
        }
    }
}

function clearFieldError(event) {
    const field = event.target;
    const fieldId = field.id;
    
    // Remove error styling
    field.style.borderColor = '';
    field.style.backgroundColor = '';
    
    // Remove error message
    const errorMsg = document.getElementById(fieldId + '-error');
    if (errorMsg) {
        errorMsg.remove();
    }
}

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    // Add error styling
    field.style.borderColor = '#e74c3c';
    field.style.backgroundColor = '#fdf2f2';
    
    // Remove existing error message
    const existingError = document.getElementById(fieldId + '-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.id = fieldId + '-error';
    errorDiv.className = 'field-error';
    errorDiv.style.color = '#e74c3c';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFormErrors(formType) {
    const form = document.querySelector('.' + formType + '-form');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.style.borderColor = '';
        input.style.backgroundColor = '';
    });
    
    const errorMessages = form.querySelectorAll('.field-error');
    errorMessages.forEach(error => error.remove());
}

function clearForms() {
    // Clear all form inputs
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        if (input.type !== 'checkbox') {
            input.value = '';
        } else {
            input.checked = false;
        }
    });
    
    // Clear all errors
    const errorMessages = document.querySelectorAll('.field-error');
    errorMessages.forEach(error => error.remove());
    
    // Reset field styles
    const styledInputs = document.querySelectorAll('input[style*="border-color"]');
    styledInputs.forEach(input => {
        input.style.borderColor = '';
        input.style.backgroundColor = '';
    });
}

function initializeValidation() {
    // Add CSS for error styling
    const style = document.createElement('style');
    style.textContent = `
        .field-error {
            color: #e74c3c;
            font-size: 0.8rem;
            margin-top: 0.25rem;
            display: block;
        }
        
        input.error {
            border-color: #e74c3c !important;
            background-color: #fdf2f2 !important;
        }
    `;
    document.head.appendChild(style);
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isStrongPassword(password) {
    // At least one letter and one number
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    return hasLetter && hasNumber;
}

function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; font-size: 1.2rem; cursor: pointer; margin-left: 1rem; color: #6c757d;">&times;</button>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('show');
    }
}

function showLoadingWithAnimation() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        // Update loading content to use existing animation
        overlay.innerHTML = `
            <div class="loading-content">
                <video autoplay loop muted class="loading-video">
                    <source src="/static/Loading animation blue.webm" type="video/webm">
                </video>
                <p>Memproses login...</p>
            </div>
        `;
        overlay.classList.add('show');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('show');
        // Reset to original content
        overlay.innerHTML = `
            <div class="loading-spinner"></div>
            <p>Memproses...</p>
        `;
    }
}

// Check if user is already logged in
function checkLoginStatus() {
    const rememberMe = localStorage.getItem('rememberMe');
    const userEmail = localStorage.getItem('userEmail');
    
    if (rememberMe === 'true' && userEmail) {
        // Pre-fill email in login form
        const emailField = document.getElementById('login-email');
        if (emailField) {
            emailField.value = userEmail;
        }
        
        // Check remember me checkbox
        const rememberCheckbox = document.getElementById('remember-me');
        if (rememberCheckbox) {
            rememberCheckbox.checked = true;
        }
    }
}

// Initialize login status check
document.addEventListener('DOMContentLoaded', checkLoginStatus);

// Handle forgot password
function handleForgotPassword() {
    const email = document.getElementById('login-email').value;
    
    if (!email) {
        showNotification('Silakan masukkan email terlebih dahulu', 'warning');
        return;
    }
    
    if (!isValidEmail(email)) {
        showNotification('Format email tidak valid', 'error');
        return;
    }
    
    showLoading();
    
    // Simulate password reset
    setTimeout(() => {
        hideLoading();
        showNotification('Link reset password telah dikirim ke email Anda', 'success');
    }, 2000);
}

// Add forgot password event listener
document.addEventListener('DOMContentLoaded', function() {
    const forgotPasswordLink = document.querySelector('.forgot-password');
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(e) {
            e.preventDefault();
            handleForgotPassword();
        });
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Alt + L for login tab
    if (e.altKey && e.key === 'l') {
        e.preventDefault();
        switchTab('login');
    }
    
    // Alt + R for register tab
    if (e.altKey && e.key === 'r') {
        e.preventDefault();
        switchTab('register');
    }
    
    // Enter key in forms
    if (e.key === 'Enter') {
        const activeForm = document.querySelector('.form-content.active form');
        if (activeForm) {
            activeForm.dispatchEvent(new Event('submit'));
        }
    }
});

// Form auto-save (for better UX)
function autoSaveForm() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                sessionStorage.setItem('form_' + form.className, JSON.stringify(data));
            });
        });
    });
}

// Restore form data
function restoreFormData() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const savedData = sessionStorage.getItem('form_' + form.className);
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input && input.type !== 'checkbox') {
                        input.value = data[key];
                    } else if (input && input.type === 'checkbox') {
                        input.checked = data[key] === 'on';
                    }
                });
            } catch (e) {
                console.log('Error restoring form data:', e);
            }
        }
    });
}

// Initialize auto-save and restore
document.addEventListener('DOMContentLoaded', function() {
    autoSaveForm();
    restoreFormData();
});

// Clear form data on successful submission
function clearFormData() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        sessionStorage.removeItem('form_' + form.className);
    });
}

// Export functions for global access
window.switchTab = switchTab;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.showNotification = showNotification;

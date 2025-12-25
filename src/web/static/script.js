// ===== BOOTSTRAP INTEGRATION =====

// Initialize Bootstrap functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            
            // Add visual feedback to the button
            const icon = sidebarToggle.querySelector('i');
            if (icon) {
                if (document.body.classList.contains('sb-sidenav-toggled')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
    
    // Set Dashboard as active by default (without background color)
    const dashboardLink = document.querySelector('.sb-sidenav .nav-link[onclick*="showContent(\'home\')"]');
    if (dashboardLink) {
        dashboardLink.classList.add('active');
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        const sidebar = document.getElementById('layoutSidenav_nav');
        const sidebarToggle = document.getElementById('sidebarToggle');
        
        if (window.innerWidth <= 991.98 && 
            document.body.classList.contains('sb-sidenav-toggled') &&
            !sidebar.contains(e.target) && 
            !sidebarToggle.contains(e.target)) {
            document.body.classList.remove('sb-sidenav-toggled');
            
            // Reset button icon
            const icon = sidebarToggle.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });
});

// Sidebar dropdown toggle function
function toggleSidebarDropdown(targetId, triggerElement) {
    const target = document.getElementById(targetId);
    
    if (target && triggerElement) {
        const isExpanded = triggerElement.getAttribute('aria-expanded') === 'true';
        
        // Close all other dropdowns first
        const allDropdowns = document.querySelectorAll('.sb-sidenav .collapse');
        const allTriggers = document.querySelectorAll('.sb-sidenav .nav-link[aria-controls]');
        
        allDropdowns.forEach(dropdown => {
            if (dropdown.id !== targetId) {
                dropdown.classList.remove('show');
            }
        });
        
        allTriggers.forEach(trigger => {
            if (trigger !== triggerElement) {
                trigger.setAttribute('aria-expanded', 'false');
                trigger.classList.add('collapsed');
            }
        });
        
        // Toggle current dropdown with smooth animation
        if (isExpanded) {
            target.classList.remove('show');
            triggerElement.setAttribute('aria-expanded', 'false');
            triggerElement.classList.add('collapsed');
        } else {
            target.classList.add('show');
            triggerElement.setAttribute('aria-expanded', 'true');
            triggerElement.classList.remove('collapsed');
        }
    }
}

// Update active menu state
function updateActiveMenu(activeElement) {
    // Remove active class from all nav links
    const allNavLinks = document.querySelectorAll('.sb-sidenav .nav-link');
    allNavLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to clicked element
    if (activeElement) {
        activeElement.classList.add('active');
    }
}

// Theme Management System
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.themeIcon = document.getElementById('themeIcon');
        this.init();
    }

    init() {
        // Apply saved theme
        this.applyTheme(this.currentTheme);
        
        // Update icon
        this.updateIcon();
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        this.updateIcon();
        this.saveTheme();
        
        // Show notification
        if (window.notificationSystem) {
            const themeName = this.currentTheme === 'dark' ? 'Dark' : 'Light';
            window.notificationSystem.show(
                `Switched to ${themeName} mode`,
                'success',
                'Theme Changed'
            );
        }
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
    }

    updateIcon() {
        if (this.themeIcon) {
            this.themeIcon.textContent = this.currentTheme === 'dark' ? '☀️' : '🌙';
        }
    }

    saveTheme() {
        localStorage.setItem('theme', this.currentTheme);
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();

// Global function for theme toggle
function toggleTheme() {
    themeManager.toggleTheme();
}

// Modern Notification System
class NotificationSystem {
    constructor() {
        this.container = document.getElementById('notificationContainer');
        this.notifications = new Map();
    }

    show(message, type = 'info', title = '', duration = 2000) {
        const id = Date.now() + Math.random();
        const notification = this.createNotification(id, message, type, title);
        
        this.container.appendChild(notification);
        this.notifications.set(id, notification);

        // Auto remove after duration
        setTimeout(() => {
            this.remove(id);
        }, duration);

        return id;
    }

    createNotification(id, message, type, title) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.dataset.id = id;

        // Get appropriate icon and title based on type
        const iconMap = {
            success: '✓',
            error: '✕',
            info: 'ℹ',
            warning: '⚠'
        };

        const titleMap = {
            success: title || 'Success',
            error: title || 'Error',
            info: title || 'Information',
            warning: title || 'Warning'
        };

        notification.innerHTML = `
            <div class="notification-icon">${iconMap[type] || 'ℹ'}</div>
            <div class="notification-content">
                <div class="notification-title">${titleMap[type]}</div>
                <div class="notification-message">${message}</div>
                <div class="notification-time">now</div>
            </div>
            <button class="notification-close" onclick="notificationSystem.remove(${id})">×</button>
            <div class="notification-progress">
                <div class="notification-progress-bar"></div>
            </div>
        `;

        return notification;
    }

    remove(id) {
        const notification = this.notifications.get(id);
        if (notification) {
            notification.classList.add('slide-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
                this.notifications.delete(id);
            }, 300);
        }
    }

    success(message, title = '') {
        return this.show(message, 'success', title);
    }

    error(message, title = '') {
        return this.show(message, 'error', title);
    }

    info(message, title = '') {
        return this.show(message, 'info', title);
    }

    warning(message, title = '') {
        return this.show(message, 'warning', title);
    }
}

// Initialize notification system
const notificationSystem = new NotificationSystem();

// Global state to store table data for each view
let viewStates = {
    keuangan: {
        tableHtml: '',
        hasData: false,
        filters: {
            startDate: '',
            endDate: '',
            sortColumn: '',
            sortOrder: 'ASC',
            filterColumn: '',
            filterValue: ''
        }
    },
    pasien: {
        tableHtml: '',
        hasData: false,
        filters: {
            startDate: '',
            endDate: '',
            sortColumn: '',
            sortOrder: 'ASC',
            filterColumn: '',
            filterValue: ''
        }
    },
    'selisih-tarif': {
        tableHtml: '',
        hasData: false,
        filters: {
            startDate: '',
            endDate: '',
            sortColumn: '',
            sortOrder: 'ASC',
            filterColumn: '',
            filterValue: ''
        }
    },
    'los': {
        tableHtml: '',
        hasData: false,
        filters: {
            startDate: '',
            endDate: '',
            sortColumn: '',
            sortOrder: 'ASC',
            filterColumn: '',
            filterValue: ''
        }
    },
    'inacbg': {
        tableHtml: '',
        hasData: false,
        filters: {
            startDate: '',
            endDate: '',
            sortColumn: '',
            sortOrder: 'ASC',
            filterColumn: '',
            filterValue: ''
        }
    },
    'ventilator': {
        tableHtml: '',
        hasData: false,
        filters: {
            startDate: '',
            endDate: '',
            sortColumn: '',
            sortOrder: 'ASC',
            filterColumn: '',
            filterValue: ''
        }
    }
};

// Function to show content based on button clicked
function showContent(content) {
    // Get all content sections
    const contentSections = ['home', 'keuangan', 'pasien', 'selisih-tarif', 'los', 'inacbg', 'ventilator', 'file-upload', 'admin'];
    
    // Hide all sections and remove active class
    contentSections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.remove('active');
            section.style.display = 'none';
        }
    });
    
    // Show the selected content
    const selectedContent = document.getElementById(content);
    if (!selectedContent) return;
    
    selectedContent.style.display = 'block';
    selectedContent.classList.add('active');
    
    // Update active menu item
    updateActiveMenu(content);
    
    // Handle special content loading
    if (content === 'home') {
        if (typeof loadDashboardView === 'function') {
            loadDashboardView();
        }
    } else if (content === 'keuangan') {
        loadDataView('keuangan');
    } else if (content === 'pasien') {
        loadDataView('pasien');
    } else if (content === 'selisih-tarif') {
        loadDataView('selisih-tarif');
    } else if (content === 'los') {
        loadDataView('los');
    } else if (content === 'inacbg') {
        loadDataView('inacbg');
    } else if (content === 'ventilator') {
        loadDataView('ventilator');
    } else if (content === 'file-upload') {
        loadFileUploadView();
    } else if (content === 'admin') {
        loadAdminView();
    }
}

// Function to show file upload content
function showFileUpload() {
    showContent('file-upload');
}

// Function to load file upload view
function loadFileUploadView() {
    const content = document.getElementById('file-upload');
    if (!content) return;
    
    content.innerHTML = `
        <div class="upload-container">
            <!-- Upload Header -->
            <div class="upload-header">
                <h2>Upload Data File</h2>
                <p>Upload .txt, .xlsx, or .xls files to process and analyze data</p>
            </div>
            
            <!-- Upload Form Card -->
            <div class="upload-card">
                <form id="uploadForm" onsubmit="handleFormSubmit(event)" enctype="multipart/form-data">
                    <div class="file-upload-section">
                        <div class="file-input-wrapper">
                            <input type="file" id="fileInput" name="file" accept=".txt,.xlsx,.xls" onchange="handleFileUpload(event)" required>
                            <label for="fileInput" class="file-input-label">
                                <i class="fas fa-cloud-upload-alt file-input-icon"></i>
                                <span>Choose file or drag and drop</span>
                            </label>
                        </div>
                        <div id="fileInfo" class="file-info">No file selected.</div>
                    </div>
                    
                    <div class="upload-actions">
                        <button type="submit" id="uploadBtn" class="upload-btn" disabled>
                            <i class="fas fa-upload"></i>
                            <span>Process File</span>
                        </button>
                    </div>
                </form>
            </div>
            
            <!-- Upload Instructions -->
            <div class="upload-instructions">
                <h3><i class="fas fa-info-circle"></i> Upload Instructions</h3>
                <div class="instructions-list">
                    <div class="instruction-item">
                        <i class="fas fa-check-circle"></i>
                        <div>
                            <strong>Supported Formats:</strong> .txt, .xlsx, .xls
                        </div>
                    </div>
                    <div class="instruction-item">
                        <i class="fas fa-check-circle"></i>
                        <div>
                            <strong>File Requirements:</strong> Ensure your file contains valid data columns
                        </div>
                    </div>
                    <div class="instruction-item">
                        <i class="fas fa-check-circle"></i>
                        <div>
                            <strong>Processing:</strong> Files will be processed and data will be accumulated if multiple files are uploaded
                        </div>
                    </div>
                    <div class="instruction-item">
                        <i class="fas fa-check-circle"></i>
                        <div>
                            <strong>Data Management:</strong> Uploaded data can be viewed in Financial, Patient, and Analytics sections
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Data Management Info -->
            <div class="data-management-card">
                <div class="data-management-header">
                    <i class="fas fa-database"></i>
                    <span>Data Management</span>
                </div>
                <div class="data-management-body">
                    <div class="data-status">
                        <span class="status-indicator" id="statusIndicator"></span>
                        <span id="dataStatusText">Checking data status...</span>
                    </div>
                    <div id="dataStats" class="data-stats" style="display: none;">
                        <div id="uploadStats"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Initialize data management info
    updateDataManagementInfo();
}

// Function to load admin view
function loadAdminView() {
    const content = document.getElementById('admin');
    if (!content) return;
    
    content.innerHTML = `
        <div class="admin-container">
            <!-- Admin Header -->
            <div class="admin-header">
                <h2><i class="fas fa-users-cog"></i> User Management</h2>
                <p>Manage users, roles, and permissions</p>
            </div>
            
            <!-- Admin Actions -->
            <div class="admin-actions">
                <button class="btn-create-user" onclick="showCreateUserModal()">
                    <i class="fas fa-user-plus"></i>
                    <span>Create New User</span>
                </button>
                <button class="btn-refresh-users" onclick="refreshUsersList()">
                    <i class="fas fa-sync-alt"></i>
                    <span>Refresh</span>
                </button>
            </div>
            
            <!-- Users Table -->
            <div class="admin-table-card">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Full Name</th>
                                <th>Role</th>
                                <th>Status</th>
                                <th>Last Login</th>
                                <th>Created At</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="usersTableBody">
                            <tr>
                                <td colspan="8" class="text-center text-muted">
                                    <i class="fas fa-spinner fa-spin"></i> Loading users...
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
    
    // Initialize admin functionality
    if (typeof initializeAdmin === 'function') {
        initializeAdmin();
    }
}

// Function to update active menu item
function updateActiveMenu(content) {
    // Remove active class from all menu items
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    
    // Remove active from nav group toggles
    const navGroupToggles = document.querySelectorAll('.nav-group-toggle');
    navGroupToggles.forEach(toggle => toggle.classList.remove('active'));
    
    // Close all nav groups
    const navGroupContents = document.querySelectorAll('.nav-group-content');
    navGroupContents.forEach(groupContent => groupContent.classList.remove('show'));
    
    // Reset all arrows
    const arrows = document.querySelectorAll('.nav-arrow');
    arrows.forEach(arrow => arrow.style.transform = 'rotate(0deg)');
    
    // Add active class to the clicked menu item based on content
    if (content === 'home') {
        const homeItem = document.querySelector('.nav-item[onclick*="home"]');
        if (homeItem) homeItem.classList.add('active');
    } else if (content === 'keuangan' || content === 'pasien' || content === 'file-upload') {
        // Find Financial Data nav group (first nav-group)
        const navGroups = document.querySelectorAll('.nav-group');
        if (navGroups.length > 0) {
            const financialGroup = navGroups[0];
            const toggle = financialGroup.querySelector('.nav-group-toggle');
            const groupContent = financialGroup.querySelector('.nav-group-content');
            if (toggle && groupContent) {
                toggle.classList.add('active');
                groupContent.classList.add('show');
                // Update arrow rotation
                const arrow = toggle.querySelector('.nav-arrow');
                if (arrow) arrow.style.transform = 'rotate(180deg)';
            }
            
            // Highlight specific subitem
            let selector = '';
            if (content === 'keuangan') {
                selector = '.nav-subitem[onclick*="keuangan"]';
            } else if (content === 'pasien') {
                selector = '.nav-subitem[onclick*="pasien"]';
            } else if (content === 'file-upload') {
                selector = '.nav-subitem[onclick*="showFileUpload"]';
            }
            
            const subItem = financialGroup.querySelector(selector);
            if (subItem) subItem.classList.add('active');
        }
    } else if (content === 'selisih-tarif' || content === 'los' || content === 'inacbg' || content === 'ventilator') {
        // Find Analytics nav group (second nav-group)
        const navGroups = document.querySelectorAll('.nav-group');
        if (navGroups.length > 1) {
            const analyticsGroup = navGroups[1];
            const toggle = analyticsGroup.querySelector('.nav-group-toggle');
            const groupContent = analyticsGroup.querySelector('.nav-group-content');
            if (toggle && groupContent) {
                toggle.classList.add('active');
                groupContent.classList.add('show');
                // Update arrow rotation
                const arrow = toggle.querySelector('.nav-arrow');
                if (arrow) arrow.style.transform = 'rotate(180deg)';
            }
            
            // Highlight specific subitem
            let selector = '';
            if (content === 'selisih-tarif') {
                selector = '.nav-subitem[onclick*="selisih-tarif"]';
            } else if (content === 'los') {
                selector = '.nav-subitem[onclick*="los"]';
            } else if (content === 'inacbg') {
                selector = '.nav-subitem[onclick*="inacbg"]';
            } else if (content === 'ventilator') {
                selector = '.nav-subitem[onclick*="ventilator"]';
            }
            
            const subItem = analyticsGroup.querySelector(selector);
            if (subItem) subItem.classList.add('active');
        }
    } else if (content === 'admin') {
        const adminItem = document.querySelector('.nav-item[onclick*="admin"]');
        if (adminItem) adminItem.classList.add('active');
    }
}

// Make entire submenu-row clickable, not just the text
document.addEventListener('DOMContentLoaded', () => {
    const submenuItems = document.querySelectorAll('.submenu-item');
    submenuItems.forEach((li) => {
        li.addEventListener('click', (event) => {
            // If anchor itself was clicked, let default handler run
            if ((event.target && event.target.closest('a'))) return;
            const anchor = li.querySelector('a');
            if (anchor) anchor.click();
        });
    });
});

// Function to toggle the dropdown visibility on click
function toggleDropdown(id) {
    var dropdown = document.getElementById(id);
    var parentMenuItem = dropdown.closest('.nav-item');
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
        parentMenuItem.classList.remove("active");
    } else {
        dropdown.style.display = "block";
        parentMenuItem.classList.add("active");
    }
}

// Function to handle file upload
function handleFileUpload(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const fileInfo = document.getElementById('fileInfo');
    const uploadBtn = document.getElementById('uploadBtn');
    
    if (file) {
        const fileName = file.name;
        const fileExtension = fileName.split('.').pop().toLowerCase();
        
        // Check if the file extension is supported
        const allowedExtensions = ['txt', 'xlsx', 'xls'];
        if (!allowedExtensions.includes(fileExtension)) {
            fileInfo.innerHTML = `<span style="color: red;">❌ File tidak didukung. Gunakan .txt, .xlsx, atau .xls</span>`;
            uploadBtn.disabled = true;
            return;
        }
        // File is supported
        fileInfo.textContent = `Selected file: ${fileName}`;
        fileInfo.style.color = '#28a745'; // Green color for valid file
        uploadBtn.disabled = false;
    } else {
        fileInfo.textContent = 'No file selected.';
        fileInfo.style.color = '#555';
        uploadBtn.disabled = true;
    }
}

// Function to handle form submission and preserve data
function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const uploadBtn = document.getElementById('uploadBtn');
    
    // Show loading state
    uploadBtn.textContent = 'Processing...';
    uploadBtn.disabled = true;
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(html => {
        // Parse the HTML response to extract table data
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Check if there's success message or table data in the response
        const successMessage = doc.querySelector('.alert-success');
        const tableContainer = doc.querySelector('.table-container');
        const errorMessage = doc.querySelector('.alert-danger');
        
        if (successMessage) {
            // Success message found - upload was successful
            console.log('Upload successful - success message found');
        } else if (tableContainer && tableContainer.innerHTML.trim() !== '' && !tableContainer.innerHTML.includes('Data Belum Tersedia')) {
            // Table data found - upload was successful
            console.log('Upload successful - table data found');
        } else {
            // No success indicators found
            console.log('Upload failed - no success indicators found');
        }
        
        if (successMessage || (tableContainer && tableContainer.innerHTML.trim() !== '' && !tableContainer.innerHTML.includes('Data Belum Tersedia'))) {
            // Extract table HTML if available
            const tableHtml = tableContainer ? tableContainer.innerHTML : '';
            
            // Update all view states with the uploaded data
            updateViewState('keuangan', { 
                tableHtml: tableHtml, 
                hasData: true,
                filters: { ...viewStates.keuangan.filters }
            });
            
            updateViewState('pasien', { 
                tableHtml: tableHtml, 
                hasData: true,
                filters: { ...viewStates.pasien.filters }
            });
            
            updateViewState('selisih-tarif', { 
                tableHtml: tableHtml, 
                hasData: true,
                filters: { ...viewStates['selisih-tarif'].filters }
            });
            
            updateViewState('los', { 
                tableHtml: tableHtml, 
                hasData: true,
                filters: { ...viewStates['los'].filters }
            });
            
            updateViewState('inacbg', { 
                tableHtml: tableHtml, 
                hasData: true,
                filters: { ...viewStates['inacbg'].filters }
            });
            
            updateViewState('ventilator', { 
                tableHtml: tableHtml, 
                hasData: true,
                filters: { ...viewStates['ventilator'].filters }
            });
            
            // Update data management info
            updateDataManagementInfo();
            
            // Extract import stats from response if available
            const importStatsElement = doc.querySelector('[data-import-stats]');
            if (importStatsElement) {
                try {
                    const importStats = JSON.parse(importStatsElement.getAttribute('data-import-stats'));
                    updateDataStatusAfterUpload({summary: importStats});
                } catch (e) {
                    console.log('Could not parse import stats');
                }
            }
            
            // Show success message
            if (successMessage) {
                notificationSystem.success('File uploaded and processed successfully!', 'Success');
            } else {
                notificationSystem.success('File uploaded and accumulated successfully!', 'Success');
            }
            
        } else if (errorMessage) {
            // Show error message
            notificationSystem.error(errorMessage.textContent.trim(), 'Error');
        } else {
            notificationSystem.warning('No data found in file.', 'No Data');
        }
        
        // Reset form
        event.target.reset();
        document.getElementById('fileInfo').textContent = 'No file selected.';
        document.getElementById('fileInfo').style.color = '#555';
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        notificationSystem.error('Upload failed. Please try again.', 'Error');
    })
    .finally(() => {
        // Restore button state
        uploadBtn.textContent = 'Process File';
        uploadBtn.disabled = true;
    });
}

// Generic function to load data view (keuangan, pasien, selisih-tarif, or los)
function loadDataView(viewType) {
    const content = document.getElementById(viewType);
    let title, description, prefix;
    
    if (viewType === 'keuangan') {
        title = 'Financial';
        description = 'financial with profit and loss calculation';
        prefix = '';
    } else if (viewType === 'pasien') {
        title = 'Patient';
        description = 'patient with complete medical information';
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        title = 'Rate Difference';
        description = 'rate difference between charged rates and standard rates';
        prefix = 'selisih';
    } else if (viewType === 'los') {
        title = 'LOS (Length of Stay)';
        description = 'patient length of stay with various parameters';
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        title = 'INACBG';
        description = 'data grouped by INACBG with aggregate statistics';
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        title = 'Ventilator';
        description = 'ventilator usage with detailed information';
        prefix = 'ventilator';
    }
    
    const state = viewStates[viewType];
    
    // Format date for display
    const formatDateForDisplay = (dateStr) => {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
    };
    
    const dateRangeDisplay = state.filters.startDate && state.filters.endDate 
        ? `${formatDateForDisplay(state.filters.startDate)} - ${formatDateForDisplay(state.filters.endDate)}`
        : 'Date, 2023 - Nov 17, 2023';
    
    // Set content dengan struktur baru mengikuti desain !Important
    content.innerHTML = `
        <div class="table-card">
            <!-- Table Header -->
            <div class="table-header">
                <h2>Analisis ${title}</h2>
                <p>Menampilkan analisis data ${description}</p>
            </div>
            
            <!-- Filter Container -->
            <div class="filter-container">
                <div class="filter-row">
                    <!-- Date Range -->
                    <div class="filter-field">
                        <label class="filter-label">Date Range</label>
                        <div class="date-range-wrapper" onclick="openDatePicker('${prefix}', '${viewType}')">
                            <div class="date-range-content">
                                <svg class="filter-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                                <span id="${prefix}DateRange" class="date-range-text">${dateRangeDisplay}</span>
                            </div>
                            <svg class="filter-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                            </svg>
                            <input type="date" id="${prefix}StartDate" class="hidden-date-input" value="${state.filters.startDate || ''}" style="display: none;">
                            <input type="date" id="${prefix}EndDate" class="hidden-date-input" value="${state.filters.endDate || ''}" style="display: none;">
                        </div>
                    </div>
                    
                    <!-- Sort By -->
                    <div class="filter-field">
                        <label class="filter-label">Sort By</label>
                        <div class="filter-input-wrapper">
                            <select id="${prefix}SortColumn" class="filter-select">
                                <option value="">Select Column</option>
                            </select>
                            <div class="filter-select-icon">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"></path>
                                </svg>
                            </div>
                            <input type="hidden" id="${prefix}SortOrder" value="${state.filters.sortOrder || 'ASC'}">
                        </div>
                    </div>
                    
                    <!-- Select Column -->
                    <div class="filter-field">
                        <label class="filter-label">Select Column</label>
                        <div class="filter-input-wrapper">
                            <select id="${prefix}FilterColumn" class="filter-select">
                                <option value="">Select Column</option>
                            </select>
                            <div class="filter-select-icon">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Search Value -->
                    <div class="filter-field">
                        <label class="filter-label">Search Value</label>
                        <div class="filter-input-wrapper">
                            <input type="text" id="${prefix}FilterValue" class="filter-input" placeholder="Search Value" value="${state.filters.filterValue || ''}">
                            <div class="filter-input-icon">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Action Buttons -->
                <div class="filter-buttons">
                    <button id="${prefix}ApplyAllFilters" class="filter-btn filter-btn-primary">
                        <svg class="btn-icon-small" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                        SEARCH
                    </button>
                    <button id="${prefix}ClearAllFilters" class="filter-btn filter-btn-secondary" title="Click: Clear filters & show all data | Double-click: Clear filters only">
                        <svg class="btn-icon-small" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                        </svg>
                        CLEAR
                    </button>
                </div>
            </div>
            
            <!-- Table Container -->
            <div class="table-container">
                ${state.hasData ? state.tableHtml : `
                <div class="no-data-container">
                    <h3>No Data Available</h3>
                    <p>Please select a date range first to display data.</p>
                    <div class="upload-instructions">
                        <h4>How to Display Data:</h4>
                        <ol>
                            <li>Upload .txt, .xlsx, or .xls file using the upload form</li>
                            <li>Select the desired date range</li>
                            <li>Click the "SEARCH" button</li>
                            <li>Data will appear according to the selected date range</li>
                        </ol>
                    </div>
                </div>
                `}
            </div>
        </div>
    `;
    
    // Load filter columns
    loadFilterColumns(viewType);
    loadSortingColumns(viewType);
    
    // Restore selected values for dropdowns
    if (state.filters.sortColumn) {
        setTimeout(() => {
            const sortSelect = document.getElementById(`${prefix}SortColumn`);
            if (sortSelect) {
                sortSelect.value = state.filters.sortColumn;
            }
        }, 100);
    }
    
    if (state.filters.filterColumn) {
        setTimeout(() => {
            const filterSelect = document.getElementById(`${prefix}FilterColumn`);
            if (filterSelect) {
                filterSelect.value = state.filters.filterColumn;
            }
        }, 100);
    }
    
    // Attach event listeners
    document.getElementById(`${prefix}ApplyAllFilters`).addEventListener('click', () => applyAllFilters(viewType));
    
    // Add both click and double-click listeners for clear button
    const clearBtn = document.getElementById(`${prefix}ClearAllFilters`);
    clearBtn.addEventListener('click', () => clearAllFilters(viewType));
    clearBtn.addEventListener('dblclick', () => clearFiltersOnly(viewType));
    
    // Add click listener to sort icon
    setTimeout(() => {
        const sortColumnSelect = document.getElementById(`${prefix}SortColumn`);
        if (sortColumnSelect) {
            const sortIcon = sortColumnSelect.parentElement.querySelector('.filter-select-icon');
            if (sortIcon) {
                sortIcon.classList.add('clickable');
                sortIcon.title = 'Click to toggle sort order';
                sortIcon.addEventListener('click', (e) => {
                    e.stopPropagation();
                    applySortFromIcon(viewType);
                });
            }
        }
    }, 100);
    
    // Initialize date range picker
    initializeDateRangePicker(viewType, prefix);
}

// Function to open date picker
function openDatePicker(prefix, viewType) {
    const startDateInput = document.getElementById(`${prefix}StartDate`);
    const endDateInput = document.getElementById(`${prefix}EndDate`);
    
    if (!startDateInput || !endDateInput) return;
    
    // If no start date, open start date picker first
    if (!startDateInput.value) {
        startDateInput.showPicker();
    } else if (!endDateInput.value) {
        // If start date exists but no end date, open end date picker
        endDateInput.showPicker();
    } else {
        // If both dates exist, allow user to change start date
        startDateInput.showPicker();
    }
}

// Function to initialize date range picker
function initializeDateRangePicker(viewType, prefix) {
    const dateRangeText = document.getElementById(`${prefix}DateRange`);
    const startDateInput = document.getElementById(`${prefix}StartDate`);
    const endDateInput = document.getElementById(`${prefix}EndDate`);
    
    if (!dateRangeText || !startDateInput || !endDateInput) return;
    
    // Format date for display
    const formatDateForDisplay = (dateStr) => {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
    };
    
    // Update display when dates change
    const updateDateRangeDisplay = () => {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        
        if (startDate && endDate) {
            dateRangeText.textContent = `${formatDateForDisplay(startDate)} - ${formatDateForDisplay(endDate)}`;
        } else if (startDate) {
            dateRangeText.textContent = `${formatDateForDisplay(startDate)} - ...`;
        } else if (endDate) {
            dateRangeText.textContent = `... - ${formatDateForDisplay(endDate)}`;
        } else {
            dateRangeText.textContent = 'Date, 2023 - Nov 17, 2023';
        }
    };
    
    // Handle start date change
    startDateInput.addEventListener('change', () => {
        updateDateRangeDisplay();
        // If end date is before start date, clear end date
        if (endDateInput.value && endDateInput.value < startDateInput.value) {
            endDateInput.value = '';
        }
        // Auto-open end date picker if start date is set
        if (startDateInput.value && !endDateInput.value) {
            setTimeout(() => endDateInput.showPicker(), 100);
        }
    });
    
    // Handle end date change
    endDateInput.addEventListener('change', () => {
        updateDateRangeDisplay();
    });
    
    // Initialize display
    updateDateRangeDisplay();
}

// Function to apply sort when sort icon is clicked
function applySortFromIcon(viewType) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    const sortColumn = document.getElementById(`${prefix}SortColumn`);
    if (!sortColumn || !sortColumn.value) {
        notificationSystem.warning('Please select a field to sort first', 'Required');
        return;
    }
    
    // Toggle sort order
    const sortOrderInput = document.getElementById(`${prefix}SortOrder`);
    const currentOrder = sortOrderInput ? sortOrderInput.value : 'ASC';
    const newOrder = currentOrder === 'ASC' ? 'DESC' : 'ASC';
    
    if (sortOrderInput) {
        sortOrderInput.value = newOrder;
    }
    
    // Apply the sort
    applySortFromButton(viewType, newOrder);
}

// Function to apply sort from button click
function applySortFromButton(viewType, sortOrder) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    const sortColumn = document.getElementById(`${prefix}SortColumn`);
    if (!sortColumn || !sortColumn.value) {
        notificationSystem.warning('Please select a field to sort first', 'Required');
        return;
    }
    
    // Update hidden sort order input
    const sortOrderInput = document.getElementById(`${prefix}SortOrder`);
    if (sortOrderInput) {
        sortOrderInput.value = sortOrder;
    }
    
    // Get current filter values
    const startDate = getInputValueWithFallback(prefix, 'StartDate');
    const endDate = getInputValueWithFallback(prefix, 'EndDate');
    const filterColumn = getInputValueWithFallback(prefix, 'FilterColumn');
    const filterValue = getInputValueWithFallback(prefix, 'FilterValue');
    
    // Update filters state
    updateFiltersState(viewType, { 
        sortColumn: sortColumn.value, 
        sortOrder: sortOrder,
        startDate: startDate,
        endDate: endDate,
        filterColumn: filterColumn,
        filterValue: filterValue
    });
    
    // Show loading state
    const tableContainer = document.querySelector(`#${viewType} .table-container`);
    if (tableContainer) {
        showTableSkeleton(tableContainer);
    }
    
    // Build query parameters
    const params = new URLSearchParams();
    params.append('sort_column', sortColumn.value);
    params.append('sort_order', sortOrder);
    
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    if (filterColumn && filterValue) {
        params.append('filter_column', filterColumn);
        params.append('filter_value', filterValue);
    }
    
    // Determine endpoint
    let endpoint = `/${viewType}/filter`;
    if (filterColumn && filterValue) {
        endpoint = `/${viewType}/specific-filter`;
    }
    
    // Make API call
    fetch(`${endpoint}?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                notificationSystem.error('Error: ' + data.error, 'Error');
                return;
            }
            
            // Update the table with sorted data
            if (tableContainer && data.table_html) {
                tableContainer.style.opacity = '0';
                setTimeout(() => {
                    tableContainer.innerHTML = data.table_html;
                    tableContainer.style.transition = 'opacity 0.3s ease';
                    tableContainer.style.opacity = '1';
                }, 200);
                
                // Update state
                updateViewState(viewType, { tableHtml: data.table_html, hasData: true });
                
                notificationSystem.success(`Data sorted by ${sortColumn.value} (${sortOrder})`, 'Success');
            }
        })
        .catch(error => {
            console.error(`Error applying ${viewType} sort:`, error);
            notificationSystem.error('Sorting failed. Please try again.', 'Error');
        });
}

// Generic function to load available columns for sorting
function loadSortingColumns(viewType) {
    const endpoint = `/${viewType}/columns`;
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            const sortColumnSelect = document.getElementById(`${prefix}SortColumn`);
            
            // Clear existing options except the first one
            sortColumnSelect.innerHTML = '<option value="">Select Column</option>';
            
            // Add column options
            if (data.columns && data.columns.length > 0) {
                data.columns.forEach(column => {
                    const option = document.createElement('option');
                    option.value = column;
                    option.textContent = column;
                    sortColumnSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error(`Error loading ${viewType} sorting columns:`, error);
        });
}

// Generic function to load available columns for filtering
function loadFilterColumns(viewType) {
    const endpoint = `/${viewType}/columns`;
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            const filterColumnSelect = document.getElementById(`${prefix}FilterColumn`);
            
            // Clear existing options except the first one
            filterColumnSelect.innerHTML = '<option value="">Select Column</option>';
            
            // Add column options
            if (data.columns && data.columns.length > 0) {
                data.columns.forEach(column => {
                    const option = document.createElement('option');
                    option.value = column;
                    option.textContent = column;
                    filterColumnSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error(`Error loading ${viewType} filter columns:`, error);
        });
}

// Function to update view state
function updateViewState(viewType, updates) {
    viewStates[viewType] = { ...viewStates[viewType], ...updates };
}

// Function to update filters state
function updateFiltersState(viewType, filterUpdates) {
    viewStates[viewType].filters = { ...viewStates[viewType].filters, ...filterUpdates };
}

// Helper to read input/select values with ID-casing fallbacks
function getInputValueWithFallback(prefix, baseName) {
    const candidates = [];
    candidates.push(`${prefix}${baseName}`);
    candidates.push(`${prefix}${baseName[0].toLowerCase()}${baseName.slice(1)}`);
    candidates.push(`${prefix.toLowerCase()}${baseName}`);
    candidates.push(`${prefix.toLowerCase()}${baseName[0].toLowerCase()}${baseName.slice(1)}`);

    for (let id of candidates) {
        const el = document.getElementById(id);
        if (el) return el.value;
    }

    return '';
}

function setInputValueWithFallback(prefix, baseName, value) {
    const candidates = [];
    candidates.push(`${prefix}${baseName}`);
    candidates.push(`${prefix}${baseName[0].toLowerCase()}${baseName.slice(1)}`);
    candidates.push(`${prefix.toLowerCase()}${baseName}`);
    candidates.push(`${prefix.toLowerCase()}${baseName[0].toLowerCase()}${baseName.slice(1)}`);

    for (let id of candidates) {
        const el = document.getElementById(id);
        if (el) {
            el.value = value;
            return true;
        }
    }

    return false;
}

// Generic function to apply sorting
function applySorting(viewType) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    const sortColumn = getInputValueWithFallback(prefix, 'SortColumn');
    const sortOrder = getInputValueWithFallback(prefix, 'SortOrder');
    
    if (!sortColumn) {
        notificationSystem.warning('Please select a column to sort', 'Required');
        return;
    }
    
    // Update filters state
    updateFiltersState(viewType, { sortColumn, sortOrder });
    
    // Show loading state (guard in case ApplySort button not present)
    const applySortBtn = document.getElementById(`${prefix}ApplySort`);
    let originalText = '';
    if (applySortBtn) {
        originalText = applySortBtn.textContent;
        applySortBtn.textContent = 'Sorting...';
        applySortBtn.disabled = true;
    }
    
    // Make API call to get sorted data
    fetch(`/${viewType}/sort?column=${encodeURIComponent(sortColumn)}&order=${encodeURIComponent(sortOrder)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                notificationSystem.error('Error: ' + data.error, 'Error');
                return;
            }
            
            // Update the table with sorted data
            const tableContainer = document.querySelector(`#${viewType} .table-container`);
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
                // Update state
                updateViewState(viewType, { tableHtml: data.table_html, hasData: true });
            }
        })
        .catch(error => {
            console.error(`Error applying ${viewType} sorting:`, error);
            notificationSystem.error('Sorting failed. Please try again.', 'Error');
        })
        .finally(() => {
            // Restore button state if it existed
            if (applySortBtn) {
                applySortBtn.textContent = originalText;
                applySortBtn.disabled = false;
            }
        });
}

// Generic function to apply all filters (flexible - handles 1, 2, or 3 features)
function applyAllFilters(viewType) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    const startDate = getInputValueWithFallback(prefix, 'StartDate');
    const endDate = getInputValueWithFallback(prefix, 'EndDate');
    const sortColumn = getInputValueWithFallback(prefix, 'SortColumn');
    const sortOrder = getInputValueWithFallback(prefix, 'SortOrder');
    const filterColumn = getInputValueWithFallback(prefix, 'FilterColumn');
    const filterValue = getInputValueWithFallback(prefix, 'FilterValue');
    
    // Check if at least one filter is applied (date range, specific filter, OR sorting)
    if (!startDate && !endDate && !filterColumn && !filterValue && !sortColumn) {
        notificationSystem.warning('Please select at least one filter criteria (date range, specific filter, or sort)', 'Required');
        return;
    }
    
    // Update filters state
    updateFiltersState(viewType, { startDate, endDate, sortColumn, sortOrder, filterColumn, filterValue });
    
    // Show loading state with skeleton
    const tableContainer = document.querySelector(`#${viewType} .table-container`);
    if (tableContainer) {
        showTableSkeleton(tableContainer);
    }
    
    // Show loading state
    const applyFilterBtn = document.getElementById(`${prefix}ApplyAllFilters`);
    if (!applyFilterBtn) {
        console.error(`Button ${prefix}ApplyAllFilters not found`);
        return;
    }
    
    // Store original button content
    const originalContent = applyFilterBtn.innerHTML;
    const originalDisabled = applyFilterBtn.disabled;
    
    // Update button to show loading state
    applyFilterBtn.innerHTML = '<svg class="btn-icon-small" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg> Searching...';
    applyFilterBtn.disabled = true;
    applyFilterBtn.style.opacity = '0.7';
    
    // Build query parameters for all available filters
    const params = new URLSearchParams();
    
    // Add date filters if provided
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    // Add sorting if provided
    if (sortColumn) params.append('sort_column', sortColumn);
    if (sortOrder) params.append('sort_order', sortOrder);
    
    // Add specific filter if provided
    if (filterColumn && filterValue) {
        params.append('filter_column', filterColumn);
        params.append('filter_value', filterValue);
    }
    
    // Determine which API endpoint to use based on filters
    let endpoint = `/${viewType}/filter`;
    
    // If specific filter is applied, use specific-filter endpoint
    if (filterColumn && filterValue) {
        endpoint = `/${viewType}/specific-filter`;
    }
    
    // Make API call to get filtered data
    fetch(`${endpoint}?${params.toString()}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                notificationSystem.error('Error: ' + data.error, 'Error');
                // Show error in table container
                const tableContainer = document.querySelector(`#${viewType} .table-container`);
                if (tableContainer) {
                    tableContainer.innerHTML = `
                        <div class="no-data-container">
                            <h3>Error</h3>
                            <p>${data.error}</p>
                        </div>
                    `;
                }
                return;
            }
            
            // Update the table with filtered data
            const tableContainer = document.querySelector(`#${viewType} .table-container`);
            if (tableContainer && data.table_html) {
                // Remove skeleton and show content
                tableContainer.innerHTML = data.table_html;
                tableContainer.style.opacity = '1';
                
                // Update state
                updateViewState(viewType, { tableHtml: data.table_html, hasData: true });
                
                // Show success message with applied filters info
                let appliedFilters = [];
                if (startDate || endDate) appliedFilters.push('Date Range');
                if (sortColumn) appliedFilters.push('Sorting');
                if (filterColumn && filterValue) appliedFilters.push('Specific Filter');
                
                notificationSystem.success(`Data filtered successfully! Applied: ${appliedFilters.join(', ')}`, 'Success');
            } else if (tableContainer && !data.table_html) {
                // No data returned
                tableContainer.innerHTML = `
                    <div class="no-data-container">
                        <h3>No Data Found</h3>
                        <p>No data matches your search criteria. Please try different filters.</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error(`Error applying ${viewType} filters:`, error);
            notificationSystem.error('Search failed. Please try again.', 'Error');
            
            // Show error message in table container
            const tableContainer = document.querySelector(`#${viewType} .table-container`);
            if (tableContainer) {
                tableContainer.innerHTML = `
                    <div class="no-data-container">
                        <h3>Error Loading Data</h3>
                        <p>An error occurred while searching. Please try again.</p>
                    </div>
                `;
            }
        })
        .finally(() => {
            // Always restore button state, even on error
            if (applyFilterBtn) {
                applyFilterBtn.innerHTML = originalContent;
                applyFilterBtn.disabled = originalDisabled;
                applyFilterBtn.style.opacity = '1';
            }
        });
}

// Generic function to clear all filters and show all data
function clearAllFilters(viewType) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    // Clear all inputs (use fallback setter)
    setInputValueWithFallback(prefix, 'StartDate', '');
    setInputValueWithFallback(prefix, 'EndDate', '');
    setInputValueWithFallback(prefix, 'SortColumn', '');
    setInputValueWithFallback(prefix, 'SortOrder', 'ASC');
    setInputValueWithFallback(prefix, 'FilterColumn', '');
    setInputValueWithFallback(prefix, 'FilterValue', '');
    
    // Clear date range display
    const dateRangeInput = document.getElementById(`${prefix}DateRange`);
    if (dateRangeInput) {
        dateRangeInput.value = 'Date, 2023 - Nov 17, 2023';
    }
    
    // Update filters state
    updateFiltersState(viewType, { 
        startDate: '', 
        endDate: '', 
        sortColumn: '', 
        sortOrder: 'ASC', 
        filterColumn: '', 
        filterValue: '' 
    });
    
    // Show loading state
    const clearFilterBtn = document.getElementById(`${prefix}ClearAllFilters`);
    if (!clearFilterBtn) {
        console.error(`Button ${prefix}ClearAllFilters not found`);
        return;
    }
    
    // Store original button content
    const originalContent = clearFilterBtn.innerHTML;
    const originalDisabled = clearFilterBtn.disabled;
    
    // Update button to show loading state
    clearFilterBtn.innerHTML = '<svg class="btn-icon-small" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg> Loading...';
    clearFilterBtn.disabled = true;
    
    // Make API call to get all data (no filters)
    fetch(`/${viewType}/filter`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                notificationSystem.error('Error: ' + data.error, 'Error');
                return;
            }
            
            // Update the table with all data
            const tableContainer = document.querySelector(`#${viewType} .table-container`);
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
                // Update state
                updateViewState(viewType, { tableHtml: data.table_html, hasData: true });
                notificationSystem.success('All filters cleared! Showing all data.', 'Success');
            }
        })
        .catch(error => {
            console.error(`Error clearing ${viewType} filters:`, error);
            notificationSystem.error('Clear failed. Please try again.', 'Error');
        })
        .finally(() => {
            // Restore button state
            if (clearFilterBtn) {
                clearFilterBtn.innerHTML = originalContent;
                clearFilterBtn.disabled = originalDisabled;
            }
        });
}

// Generic function to clear filters only (without reloading data)
function clearFiltersOnly(viewType) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    // Clear all inputs (use fallback setter)
    setInputValueWithFallback(prefix, 'StartDate', '');
    setInputValueWithFallback(prefix, 'EndDate', '');
    setInputValueWithFallback(prefix, 'SortColumn', '');
    setInputValueWithFallback(prefix, 'SortOrder', 'ASC');
    setInputValueWithFallback(prefix, 'FilterColumn', '');
    setInputValueWithFallback(prefix, 'FilterValue', '');
    
    // Clear date range display
    const dateRangeText = document.getElementById(`${prefix}DateRange`);
    if (dateRangeText) {
        dateRangeText.textContent = 'Date, 2023 - Nov 17, 2023';
    }
    
    // Update filters state
    updateFiltersState(viewType, { 
        startDate: '', 
        endDate: '', 
        sortColumn: '', 
        sortOrder: 'ASC', 
        filterColumn: '', 
        filterValue: '' 
    });
    
    // Show notification
    notificationSystem.info('Filters cleared! Use Search button to apply new filters.', 'Info');
}

// Generic function to apply specific filter
function applySpecificFilter(viewType) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    const filterColumn = getInputValueWithFallback(prefix, 'FilterColumn');
    const filterValue = getInputValueWithFallback(prefix, 'FilterValue');
    const sortColumn = getInputValueWithFallback(prefix, 'SortColumn');
    const sortOrder = getInputValueWithFallback(prefix, 'SortOrder');
    const startDate = getInputValueWithFallback(prefix, 'StartDate');
    const endDate = getInputValueWithFallback(prefix, 'EndDate');
    
    if (!filterColumn || !filterValue) {
        notificationSystem.warning('Please select column and enter search value', 'Required');
        return;
    }
    
    // Update filters state
    updateFiltersState(viewType, { filterColumn, filterValue, sortColumn, sortOrder, startDate, endDate });
    
    // Show loading state
    const applyFilterBtn = document.getElementById(`${prefix}ApplySpecificFilter`);
    const originalText = applyFilterBtn.textContent;
    applyFilterBtn.textContent = 'Mencari...';
    applyFilterBtn.disabled = true;
    
    // Build query parameters
    const params = new URLSearchParams();
    params.append('filter_column', filterColumn);
    params.append('filter_value', filterValue);
    if (sortColumn) params.append('sort_column', sortColumn);
    if (sortOrder) params.append('sort_order', sortOrder);
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    // Make API call to get filtered data
    fetch(`/${viewType}/specific-filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                notificationSystem.error('Error: ' + data.error, 'Error');
                return;
            }
            
            // Update the table with filtered data
            const tableContainer = document.querySelector(`#${viewType} .table-container`);
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
                // Update state
                updateViewState(viewType, { tableHtml: data.table_html, hasData: true });
            }
        })
        .catch(error => {
            console.error(`Error applying ${viewType} specific filter:`, error);
            notificationSystem.error('Search failed. Please try again.', 'Error');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Generic function to clear specific filter
function clearSpecificFilter(viewType) {
    let prefix;
    
    if (viewType === 'keuangan') {
        prefix = '';
    } else if (viewType === 'pasien') {
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        prefix = 'selisih';
    } else if (viewType === 'los') {
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        prefix = 'ventilator';
    }
    
    // Clear filter inputs
    document.getElementById(`${prefix}FilterColumn`).value = '';
    document.getElementById(`${prefix}FilterValue`).value = '';
    
    // Update filters state
    updateFiltersState(viewType, { filterColumn: '', filterValue: '' });
    
    // Reload original data without specific filter
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    const startDate = document.getElementById(`${prefix}StartDate`).value;
    const endDate = document.getElementById(`${prefix}EndDate`).value;
    
    // Show loading state
    const clearFilterBtn = document.getElementById(`${prefix}ClearSpecificFilter`);
    const originalText = clearFilterBtn.textContent;
    clearFilterBtn.textContent = 'Clearing...';
    clearFilterBtn.disabled = true;
    
    // Build query parameters for other filters only
    const params = new URLSearchParams();
    if (sortColumn) params.append('sort_column', sortColumn);
    if (sortOrder) params.append('sort_order', sortOrder);
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    // Make API call to get original data
    fetch(`/${viewType}/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                notificationSystem.error('Error: ' + data.error, 'Error');
                return;
            }
            
            // Update the table with original data
            const tableContainer = document.querySelector(`#${viewType} .table-container`);
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
                // Update state
                updateViewState(viewType, { tableHtml: data.table_html, hasData: true });
            }
        })
        .catch(error => {
            console.error(`Error clearing ${viewType} specific filter:`, error);
            notificationSystem.error('Clear failed. Please try again.', 'Error');
        })
        .finally(() => {
            // Restore button state
            clearFilterBtn.textContent = originalText;
            clearFilterBtn.disabled = false;
        });
}

// Test function for notifications (can be called from browser console)
function testNotifications() {
    notificationSystem.success('File processed!', 'Success');
    setTimeout(() => notificationSystem.error('Upload failed.', 'Error'), 500);
    setTimeout(() => notificationSystem.warning('Please select column to sort', 'Required'), 1000);
    setTimeout(() => notificationSystem.info('Data available in menu', 'Info'), 1500);
}



// Update processing summary display
function updateProcessingSummary(summary) {
    const processingContainer = document.querySelector('.processing-info-container');
    if (!processingContainer) return;
    
    // Update the summary content
    const summaryElement = processingContainer.querySelector('.processing-summary');
    if (summaryElement) {
        summaryElement.innerHTML = `
            <p><strong>Total Data Rows:</strong> ${summary.total_rows}</p>
            <p><strong>Price Adjustments Applied:</strong> ${summary.pricing_adjustments_applied}</p>
            <div class="inacbg-breakdown">
                <h4>Breakdown INACBG:</h4>
                <ul>
                    <li>Digit 4 = '0' (79%): ${summary.inacbg_0_count} rows</li>
                    <li>Digit 4 = 'I/II/III' (73%): ${summary.inacbg_i_ii_iii_count} rows</li>
                    <li>Others (100%): ${summary.inacbg_other_count} rows</li>
                </ul>
            </div>
            <div class="processing-note">
                <p><strong>Note:</strong> Displayed data has been processed with price adjustments based on INACBG 4th digit.</p>
            </div>
        `;
    }
}


// Function to update data management information
function updateDataManagementInfo() {
    fetch('/processing-info')
        .then(response => response.json())
        .then(data => {
            const dataStatusText = document.getElementById('dataStatusText');
            const dataStats = document.getElementById('dataStats');
            const uploadStats = document.getElementById('uploadStats');
            
            const statusIndicator = document.querySelector('.status-indicator');
            if (data.has_data) {
                dataStatusText.textContent = 'Data available';
                if (statusIndicator) {
                    statusIndicator.style.background = '#28a745'; // Success color
                }
                
                // Show detailed stats with rows_success and rows_failed from upload_logs
                let statsHtml = '';
                if (data.rows_success > 0) {
                    statsHtml += `<div style="color: #28a745;"><strong>Rows Uploaded:</strong> ${data.rows_success}</div>`;
                }
                if (data.rows_failed > 0) {
                    statsHtml += `<div style="color: #dc3545;"><strong>Rows Duplicated:</strong> ${data.rows_failed}</div>`;
                }
                if (data.total_rows > 0) {
                    statsHtml += `<div><strong>Total rows:</strong> ${data.total_rows}</div>`;
                }
                if (data.upload_count > 0) {
                    statsHtml += `<div><strong>Files uploaded:</strong> ${data.upload_count}</div>`;
                }
                
                uploadStats.innerHTML = statsHtml;
                dataStats.style.display = 'block';
            } else {
                dataStatusText.textContent = 'No data uploaded';
                if (statusIndicator) {
                    statusIndicator.style.background = '#6c757d'; // Default color
                }
                dataStats.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data info:', error);
        });
}

// Function to update data status after upload
function updateDataStatusAfterUpload(uploadResult) {
    const dataStatusText = document.getElementById('dataStatusText');
    const dataStats = document.getElementById('dataStats');
    const uploadStats = document.getElementById('uploadStats');
    
    if (uploadResult) {
        const rowsSuccess = uploadResult.rows_success || 0;
        const rowsFailed = uploadResult.rows_failed || 0;
        const totalRows = uploadResult.total_rows || (rowsSuccess + rowsFailed);
        
        // Determine status text based on results
        const statusIndicator = document.querySelector('.status-indicator');
        if (rowsSuccess > 0 && rowsFailed > 0) {
            dataStatusText.textContent = 'Data processed (partial)';
            if (statusIndicator) {
                statusIndicator.style.background = '#ffc107'; // Warning color
            }
        } else if (rowsSuccess > 0) {
            dataStatusText.textContent = 'Data uploaded successfully';
            if (statusIndicator) {
                statusIndicator.style.background = '#28a745'; // Success color
            }
        } else if (rowsFailed > 0) {
            dataStatusText.textContent = 'Upload failed (duplicates)';
            if (statusIndicator) {
                statusIndicator.style.background = '#dc3545'; // Error color
            }
        } else {
            dataStatusText.textContent = 'No data uploaded';
            if (statusIndicator) {
                statusIndicator.style.background = '#6c757d'; // Default color
            }
        }
        
        // Show detailed stats with clear row failed/success information
        let statsHtml = '';
        if (totalRows > 0) {
            statsHtml += `<div><strong>Total rows:</strong> ${totalRows}</div>`;
        }
        if (rowsSuccess > 0) {
            statsHtml += `<div style="color: #28a745;"><strong>Rows Success:</strong> ${rowsSuccess}</div>`;
        }
        if (rowsFailed > 0) {
            statsHtml += `<div style="color: #dc3545;"><strong>Rows Failed:</strong> ${rowsFailed}</div>`;
        }
        
        uploadStats.innerHTML = statsHtml;
        dataStats.style.display = 'block';
    } else {
        dataStatusText.textContent = 'No data uploaded';
        dataStats.style.display = 'none';
    }
}

// Function to show skeleton loader for table
function showTableSkeleton(container) {
    const skeletonHtml = `
        <div class="skeleton-card" style="padding: 2rem;">
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text" style="width: 60%;"></div>
            <div style="margin-top: 1.5rem;">
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text" style="width: 80%;"></div>
            </div>
        </div>
    `;
    container.innerHTML = skeletonHtml;
    container.style.opacity = '1';
}

// Add ripple effect to buttons
function addRippleEffect(button) {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
}

// Initialize ripple effects on all buttons
function initializeRippleEffects() {
    const buttons = document.querySelectorAll('.primary-btn, .secondary-btn, .search-btn, .submit-btn');
    buttons.forEach(btn => addRippleEffect(btn));
}

// Initialize the page with Home content as default
document.addEventListener('DOMContentLoaded', function() {
    // Show Home content by default
    showContent('home');
    
    // Initialize upload button as disabled
    const uploadBtn = document.getElementById('uploadBtn');
    if (uploadBtn) {
        uploadBtn.disabled = true;
    }
    
    // Initialize data management info
    updateDataManagementInfo();
    
    // Add animation to feature cards
    animateFeatureCards();
    
    // Initialize sidebar functionality
    initializeSidebar();
    
    // Initialize ripple effects
    initializeRippleEffects();
    
    // Add ripple effect styles
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .primary-btn,
        .secondary-btn,
        .search-btn,
        .submit-btn {
            position: relative;
            overflow: hidden;
        }
    `;
    document.head.appendChild(style);
    
    // Test notifications on page load (remove this line in production)
    // setTimeout(() => testNotifications(), 1000);
});

// Function to animate feature cards on scroll
function animateFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1
    });
    
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// ===== SIDEBAR FUNCTIONALITY =====

// Initialize sidebar functionality
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const mainContentWrapper = document.querySelector('.main-content-wrapper');
    
    if (!sidebar || !mainContentWrapper) return;
    
    // Load saved sidebar state
    const savedWidth = localStorage.getItem('sidebarWidth');
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    
    // Set default width if not saved (16rem = 256px)
    const defaultWidth = '256px';
    
    if (isCollapsed) {
        sidebar.classList.add('collapsed');
        if (sidebarToggle) sidebarToggle.classList.add('active');
        sidebar.style.width = '60px';
        sidebar.style.minWidth = '60px';
        sidebar.style.maxWidth = '60px';
        mainContentWrapper.style.marginLeft = '60px';
        mainContentWrapper.style.width = 'calc(100% - 60px)';
    } else if (savedWidth) {
        sidebar.style.width = savedWidth + 'px';
        mainContentWrapper.style.marginLeft = savedWidth + 'px';
        mainContentWrapper.style.width = `calc(100% - ${savedWidth}px)`;
    } else {
        // Use default width from CSS (16rem = 256px)
        sidebar.style.width = defaultWidth;
        mainContentWrapper.style.marginLeft = defaultWidth;
        mainContentWrapper.style.width = 'calc(100% - 256px)';
    }
    
    // Ensure transition is set
    mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
    
    // Initialize resize functionality
    initializeSidebarResize();
    
    // Initialize responsive behavior
    initializeResponsiveSidebar();
    
    // Ensure main content is properly adjusted on load
    ensureMainContentSync();
}

// Initialize sidebar resize functionality
function initializeSidebarResize() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    let isResizing = false;
    let startX, startWidth;
    let animationFrameId = null;
    
    // Throttle function for smooth resize
    function throttle(func, delay) {
        let timeoutId;
        let lastExecTime = 0;
        return function (...args) {
            const currentTime = Date.now();
            
            if (currentTime - lastExecTime > delay) {
                func.apply(this, args);
                lastExecTime = currentTime;
            } else {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    func.apply(this, args);
                    lastExecTime = Date.now();
                }, delay - (currentTime - lastExecTime));
            }
        };
    }
    
    // Smooth resize function
    function smoothResize(newWidth) {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }
        
        animationFrameId = requestAnimationFrame(() => {
            // Update sidebar width and positioning
            sidebar.style.width = newWidth + 'px';
            sidebar.style.minWidth = newWidth + 'px';
            sidebar.style.maxWidth = newWidth + 'px';
            sidebar.style.position = 'fixed';
            sidebar.style.left = '0';
            sidebar.style.top = '0';
            sidebar.style.zIndex = '1001';
            
            // Update main content wrapper to match sidebar width
            const mainContentWrapper = document.querySelector('.main-content-wrapper');
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = newWidth + 'px';
                mainContentWrapper.style.width = `calc(100% - ${newWidth}px)`;
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';
            }
            
            // Update all dashboard elements to ensure they fit properly
            const contentSections = document.querySelectorAll('.content-section');
            const headerSections = document.querySelectorAll('.header-section');
            const homeContainers = document.querySelectorAll('.home-container');
            const featuresGrids = document.querySelectorAll('.features-grid');
            const featureCards = document.querySelectorAll('.feature-card');
            
            // Apply responsive styles to all dashboard elements
            [...contentSections, ...headerSections, ...homeContainers, ...featuresGrids].forEach(element => {
                if (element) {
                    element.style.width = '100%';
                    element.style.boxSizing = 'border-box';
                    element.style.overflowX = 'hidden';
                }
            });
            
            featureCards.forEach(card => {
                if (card) {
                    card.style.width = '100%';
                    card.style.boxSizing = 'border-box';
                }
            });
            
            // Force reflow to ensure changes are applied
            mainContent.offsetHeight;
        });
    }
    
    // Mouse events for resize
    sidebar.addEventListener('mousedown', (e) => {
        if (e.target === sidebar || e.target.classList.contains('sidebar')) {
            const rect = sidebar.getBoundingClientRect();
            const handleWidth = 4;
            
            if (rect.right - e.clientX <= handleWidth) {
                isResizing = true;
                startX = e.clientX;
                startWidth = sidebar.offsetWidth;
                
                sidebar.classList.add('resizing');
                document.body.style.cursor = 'col-resize';
                document.body.style.userSelect = 'none';
                
                e.preventDefault();
            }
        }
    });
    
    // Throttled mousemove handler
    const throttledMouseMove = throttle((e) => {
        if (isResizing) {
            const newWidth = startWidth + (e.clientX - startX);
            const minWidth = 200;
            const maxWidth = 400;
            
            if (newWidth >= minWidth && newWidth <= maxWidth) {
                smoothResize(newWidth);
            }
        }
    }, 16); // ~60fps
    
    document.addEventListener('mousemove', throttledMouseMove);
    
    document.addEventListener('mouseup', () => {
        if (isResizing) {
            isResizing = false;
            sidebar.classList.remove('resizing');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
            
            // Get final width and ensure main content wrapper is properly adjusted
            const finalWidth = sidebar.offsetWidth;
            const mainContentWrapper = document.querySelector('.main-content-wrapper');
            
            // Force update main content wrapper to match final sidebar width
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = finalWidth + 'px';
                mainContentWrapper.style.width = `calc(100% - ${finalWidth}px)`;
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';
            }
            
            // Save final width to localStorage
            localStorage.setItem('sidebarWidth', finalWidth);
            
            // Cancel any pending animation frame
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
            
            // Force reflow to ensure all changes are applied
            mainContent.offsetHeight;
        }
    });
}

// Ensure main content is synchronized with sidebar width
function ensureMainContentSync() {
    const sidebar = document.getElementById('sidebar');
    const mainContentWrapper = document.querySelector('.main-content-wrapper');
    
    if (sidebar && mainContentWrapper) {
        const sidebarWidth = sidebar.offsetWidth;
        
        // Ensure sidebar positioning
        sidebar.style.position = 'fixed';
        sidebar.style.left = '0';
        sidebar.style.top = '0';
        sidebar.style.zIndex = '1001';
        
        // Ensure main content wrapper matches sidebar width and prevents overlap
        mainContentWrapper.style.marginLeft = sidebarWidth + 'px';
        mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
        
        // Ensure all dashboard elements are properly sized
        const contentSections = document.querySelectorAll('.content-section');
        const headerSections = document.querySelectorAll('.header-section');
        const homeContainers = document.querySelectorAll('.home-container');
        const featuresGrids = document.querySelectorAll('.features-grid');
        const featureCards = document.querySelectorAll('.feature-card');
        
        // Apply responsive styles to all dashboard elements
        [...contentSections, ...headerSections, ...homeContainers, ...featuresGrids].forEach(element => {
            if (element) {
                element.style.width = '100%';
                element.style.boxSizing = 'border-box';
                element.style.overflowX = 'hidden';
            }
        });
        
        featureCards.forEach(card => {
            if (card) {
                card.style.width = '100%';
                card.style.boxSizing = 'border-box';
            }
        });
        
        // Force reflow
        mainContent.offsetHeight;
    }
}

// Initialize responsive sidebar behavior
function initializeResponsiveSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    
    // Check if mobile view
    function checkMobileView() {
        return window.innerWidth <= 768;
    }
    
    // Handle window resize
    window.addEventListener('resize', () => {
        const isMobile = checkMobileView();
        
        if (isMobile) {
            // Mobile view
            sidebar.classList.remove('collapsed');
            if (sidebarToggle) sidebarToggle.style.display = 'flex';
            sidebar.style.width = '256px';
            sidebar.style.minWidth = '256px';
            sidebar.style.maxWidth = '256px';
            
            // Use CSS class instead of inline transform
            if (!sidebar.classList.contains('open')) {
                sidebar.style.removeProperty('transform');
            }
            
            // Update main content wrapper margin
            const mainContentWrapper = document.querySelector('.main-content-wrapper');
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = '0';
                mainContentWrapper.style.width = '100%';
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';
            }
        } else {
            // Desktop view
            if (sidebarToggle) sidebarToggle.style.display = 'none';
            sidebar.classList.remove('open');
            if (sidebarOverlay) sidebarOverlay.classList.remove('active');
            // Remove inline transform to let CSS handle it
            sidebar.style.removeProperty('transform');
            sidebar.style.minWidth = '';
            sidebar.style.maxWidth = '';
            
            // Restore saved state
            const savedWidth = localStorage.getItem('sidebarWidth');
            const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
            const mainContentWrapper = document.querySelector('.main-content-wrapper');
            
            if (isCollapsed) {
                sidebar.classList.add('collapsed');
                sidebar.style.width = '60px';
                if (mainContentWrapper) {
                    mainContentWrapper.style.marginLeft = '60px';
                    mainContentWrapper.style.width = 'calc(100% - 60px)';
                    mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';
                }
            } else if (savedWidth) {
                sidebar.style.width = savedWidth + 'px';
                if (mainContentWrapper) {
                    mainContentWrapper.style.marginLeft = savedWidth + 'px';
                    mainContentWrapper.style.width = `calc(100% - ${savedWidth}px)`;
                    mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';
                }
            } else {
                sidebar.style.width = '256px';
                if (mainContentWrapper) {
                    mainContentWrapper.style.marginLeft = '256px';
                    mainContentWrapper.style.width = 'calc(100% - 256px)';
                    mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';
                }
            }
            
            // Force desktop margin
            if (mainContentWrapper) {
                const sidebarWidth = sidebar.style.width || '256px';
                mainContentWrapper.style.marginLeft = sidebarWidth;
                mainContentWrapper.style.width = `calc(100% - ${sidebarWidth})`;
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';
            }
        }
    });
    
    // Add overlay click event
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }
    
    // Initial check
    const isMobile = checkMobileView();
    if (isMobile) {
        if (sidebarToggle) sidebarToggle.style.display = 'flex';
        sidebar.style.width = '280px';
        sidebar.style.minWidth = '280px';
        sidebar.style.maxWidth = '280px';
        // Remove inline transform to let CSS handle it
        sidebar.style.removeProperty('transform');
        
        // Update main content wrapper margin
        const mainContentWrapper = document.querySelector('.main-content-wrapper');
        if (mainContentWrapper) {
            mainContentWrapper.style.marginLeft = '0';
            mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
        }
    } else {
        if (sidebarToggle) sidebarToggle.style.display = 'none';
        // Remove inline transform to let CSS handle it
        sidebar.style.removeProperty('transform');
        
        // Restore saved state or use default
        const savedWidth = localStorage.getItem('sidebarWidth');
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        const mainContentWrapper = document.querySelector('.main-content-wrapper');
        
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
            sidebar.style.width = '60px';
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = '60px';
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
            }
        } else if (savedWidth) {
            sidebar.style.width = savedWidth + 'px';
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = savedWidth + 'px';
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
            }
        } else {
            sidebar.style.width = '280px';
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = '256px';
                mainContentWrapper.style.width = 'calc(100% - 256px)';
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
            }
        }
        
        // Force desktop margin
        if (mainContentWrapper) {
            const sidebarWidth = sidebar.style.width || '256px';
            mainContentWrapper.style.marginLeft = sidebarWidth;
            mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
        }
    }
}

// Toggle sidebar (mobile/desktop)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const toggleIcon = document.getElementById('toggleIcon');
    const menuToggleBtn = document.getElementById('menuToggleBtn');
    
    if (!sidebar) return;
    
    // Check if mobile view (using 1024px breakpoint to match CSS)
    if (window.innerWidth <= 1024) {
        // Mobile toggle
        const isOpen = sidebar.classList.contains('open');
        
        if (isOpen) {
            // Close sidebar - use CSS class instead of inline style
            sidebar.classList.remove('open');
            if (sidebarOverlay) sidebarOverlay.classList.remove('active');
            // Remove any inline transform to let CSS handle it
            sidebar.style.removeProperty('transform');
            
            // Update icon
            if (toggleIcon) {
                toggleIcon.classList.remove('fa-times');
                toggleIcon.classList.add('fa-bars');
            }
        } else {
            // Open sidebar - use CSS class instead of inline style
            sidebar.classList.add('open');
            if (sidebarOverlay) sidebarOverlay.classList.add('active');
            // Remove any inline transform to let CSS handle it
            sidebar.style.removeProperty('transform');
            
            // Update icon
            if (toggleIcon) {
                toggleIcon.classList.remove('fa-bars');
                toggleIcon.classList.add('fa-times');
            }
        }
    } else {
        // Desktop collapse/expand
        const sidebarToggle = document.querySelector('.sidebar-toggle');
        const isCollapsed = sidebar.classList.contains('collapsed');
        const mainContent = document.querySelector('.main-content');
        
        const mainContentWrapper = document.querySelector('.main-content-wrapper');
        
        if (isCollapsed) {
            // Expand sidebar
            sidebar.classList.remove('collapsed');
            if (sidebarToggle) sidebarToggle.classList.remove('active');
            
            const savedWidth = localStorage.getItem('sidebarWidth') || '256';
            sidebar.style.width = savedWidth + 'px';
            sidebar.style.minWidth = '';
            sidebar.style.maxWidth = '';
            sidebar.style.removeProperty('transform');
            
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = savedWidth + 'px';
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
            }
            
            if (toggleIcon) {
                toggleIcon.classList.remove('fa-arrow-right');
                toggleIcon.classList.add('fa-bars');
            }
            
            localStorage.setItem('sidebarCollapsed', 'false');
        } else {
            // Collapse sidebar
            sidebar.classList.add('collapsed');
            if (sidebarToggle) sidebarToggle.classList.add('active');
            
            sidebar.style.width = '60px';
            sidebar.style.minWidth = '60px';
            sidebar.style.maxWidth = '60px';
            sidebar.style.removeProperty('transform');
            
            if (mainContentWrapper) {
                mainContentWrapper.style.marginLeft = '60px';
                mainContentWrapper.style.transition = 'margin-left 0.3s ease-in-out';
            }
            
            if (toggleIcon) {
                toggleIcon.classList.remove('fa-bars');
                toggleIcon.classList.add('fa-arrow-right');
            }
            
            localStorage.setItem('sidebarCollapsed', 'true');
        }
    }
}

// Close sidebar (mobile)
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (!sidebar) return;
    
    sidebar.classList.remove('open');
    if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    // Remove inline transform to let CSS handle it
    sidebar.style.removeProperty('transform');
    
    // Reset icon
    if (toggleIcon) {
        toggleIcon.classList.remove('fa-times');
        toggleIcon.classList.add('fa-bars');
    }
}

// Logout function
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success notification
                notificationSystem.success('Logout successful!', 'Success');
                
                // Redirect to login page after a short delay
                setTimeout(() => {
                    window.location.href = '/login';
                }, 1000);
            } else {
                notificationSystem.error('Logout failed: ' + data.message, 'Error');
            }
        })
        .catch(error => {
            console.error('Logout error:', error);
            notificationSystem.error('Logout error occurred', 'Error');
        });
    }
}

// ===== AUTO LOGOUT ON INACTIVITY =====
(function setupAutoLogout() {
	// 20 minutes in milliseconds
	const INACTIVITY_LIMIT_MS = 20 * 60 * 1000;
	let inactivityTimerId = null;
	let lastActivityTs = Date.now();

	function performAutoLogout() {
		// Avoid duplicate triggers
		if (inactivityTimerId) {
			clearTimeout(inactivityTimerId);
			inactivityTimerId = null;
		}
		// Silent logout without confirmation
		fetch('/auth/logout', { method: 'POST', headers: { 'Content-Type': 'application/json' } })
			.finally(() => {
				window.location.replace('/login');
			});
	}

	function resetInactivityTimer() {
		lastActivityTs = Date.now();
		if (inactivityTimerId) clearTimeout(inactivityTimerId);
		inactivityTimerId = setTimeout(performAutoLogout, INACTIVITY_LIMIT_MS);
	}

	function activityListener() {
		resetInactivityTimer();
	}

	// Start after DOM ready
	document.addEventListener('DOMContentLoaded', () => {
		// Bind common activity events
		['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart', 'touchmove', 'click'].forEach(evt => {
			window.addEventListener(evt, activityListener, { passive: true });
		});

		// Reset timer on visibility change (e.g., user returns to the tab)
		document.addEventListener('visibilitychange', () => {
			if (!document.hidden) resetInactivityTimer();
		});

		resetInactivityTimer();
	});
})();
    
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
    const contentSections = ['home', 'keuangan', 'pasien', 'selisih-tarif', 'los', 'inacbg', 'ventilator', 'file-upload'];
    
    // Add fade out animation to all visible sections
    contentSections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section.style.display !== 'none') {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            setTimeout(() => {
                section.style.display = 'none';
            }, 300);
        }
    });
    
    // Show the selected content with fade in animation
    setTimeout(() => {
        const selectedContent = document.getElementById(content);
        selectedContent.style.display = 'block';
        selectedContent.style.opacity = '0';
        selectedContent.style.transform = 'translateY(20px)';
        
        // Trigger reflow
        selectedContent.offsetHeight;
        
        // Add fade in animation
        selectedContent.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        selectedContent.style.opacity = '1';
        selectedContent.style.transform = 'translateY(0)';
    }, 300);
    
    // Update active menu item
    updateActiveMenu(content);
    
    // Handle special content loading
    if (content === 'keuangan') {
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
    }
}

// Function to show file upload content
function showFileUpload() {
    showContent('file-upload');
}

// Function to update active menu item
function updateActiveMenu(content) {
    // Remove active class from all menu items
    const menuItems = document.querySelectorAll('.nav-link');
    menuItems.forEach(item => item.classList.remove('active'));
    const subItems = document.querySelectorAll('.submenu-link');
    subItems.forEach(item => item.classList.remove('active'));
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    
    // Add active class to the clicked menu item
    if (content === 'home') {
        document.querySelector('.nav-link[onclick*="home"]').classList.add('active');
    } else if (content === 'keuangan' || content === 'pasien' || content === 'file-upload') {
        const eclaimItem = document.querySelector('.nav-item.has-submenu');
        if (eclaimItem) {
            eclaimItem.classList.add('active');
            eclaimItem.querySelector('.nav-link').classList.add('active');
        }
    } else if (content === 'selisih-tarif' || content === 'los' || content === 'inacbg' || content === 'ventilator') {
        const analyticsItem = document.querySelectorAll('.nav-item.has-submenu')[1];
        if (analyticsItem) {
            analyticsItem.classList.add('active');
            analyticsItem.querySelector('.nav-link').classList.add('active');
        }
    }

    // Highlight the active submenu item
    const submenuSelectorMap = {
        'keuangan': "#eclaim-dropdown .submenu-link[onclick*='keuangan']",
        'pasien': "#eclaim-dropdown .submenu-link[onclick*='pasien']",
        'file-upload': "#eclaim-dropdown .submenu-link[onclick*='showFileUpload']",
        'selisih-tarif': "#analytics-dropdown .submenu-link[onclick*='selisih-tarif']",
        'los': "#analytics-dropdown .submenu-link[onclick*='los']",
        'inacbg': "#analytics-dropdown .submenu-link[onclick*='inacbg']",
        'ventilator': "#analytics-dropdown .submenu-link[onclick*='ventilator']"
    };
    const activeSubItem = document.querySelector(submenuSelectorMap[content]);
    if (activeSubItem) {
        activeSubItem.classList.add('active');
        const parentLi = activeSubItem.closest('.submenu-item');
        if (parentLi) parentLi.classList.add('active');
        // Ensure the parent submenu is expanded
        const parentSubmenu = activeSubItem.closest('.submenu');
        if (parentSubmenu) {
            parentSubmenu.style.display = 'block';
            const parentMenuItem = parentSubmenu.closest('.nav-item');
            if (parentMenuItem) parentMenuItem.classList.add('active');
        }
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
        
        // Check if the file extension is .txt
        if (fileExtension === 'txt') {
            fileInfo.textContent = `Selected file: ${fileName}`;
            fileInfo.style.color = '#28a745'; // Green color for valid file
            uploadBtn.disabled = false;
        } else {
            fileInfo.textContent = 'Please select a .txt file only.';
            fileInfo.style.color = '#dc3545'; // Red color for invalid file
            uploadBtn.disabled = true;
        }
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
        
        // Check if there's table data in the response
        const tableContainer = doc.querySelector('.table-container');
        if (tableContainer && tableContainer.innerHTML.trim() !== '') {
            // Extract table HTML and update all view states
            const tableHtml = tableContainer.innerHTML;
            
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
            
            // Show success message
            notificationSystem.success('File uploaded and accumulated successfully!', 'Success');
            
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
        title = 'Keuangan';
        description = 'keuangan dengan perhitungan laba rugi';
        prefix = '';
    } else if (viewType === 'pasien') {
        title = 'Pasien';
        description = 'pasien dengan informasi medis lengkap';
        prefix = 'pasien';
    } else if (viewType === 'selisih-tarif') {
        title = 'Selisih Tarif';
        description = 'selisih tarif antara tarif yang dikenakan dan tarif standar';
        prefix = 'selisih';
    } else if (viewType === 'los') {
        title = 'LOS (Length of Stay)';
        description = 'lama rawat inap pasien dengan berbagai parameter';
        prefix = 'los';
    } else if (viewType === 'inacbg') {
        title = 'INACBG';
        description = 'data yang dikelompokkan berdasarkan INACBG dengan statistik agregat';
        prefix = 'inacbg';
    } else if (viewType === 'ventilator') {
        title = 'Ventilator';
        description = 'penggunaan ventilator dengan informasi detail';
        prefix = 'ventilator';
    }
    
    const state = viewStates[viewType];
    
    // Set content dengan urutan filter yang baru - data tidak langsung muncul
    content.innerHTML = `
        <h2>Analisis ${title}</h2>
        <p>Menampilkan analisis data ${description}</p>
        <p class="data-notice"><strong>⚠️ Data hanya akan muncul setelah Anda memilih rentang waktu!</strong></p>
        
        <!-- Search Controls Layout - Top Row (6 controls) -->
        <div class="search-controls-container">
            <div class="search-controls-top-row">
                <!-- Black Controls (2) -->
                <div class="search-control black-control">
                    <label for="${prefix}StartDate">Tanggal Mulai</label>
                    <input type="date" id="${prefix}StartDate" class="search-input" value="${state.filters.startDate}">
                </div>
                <div class="search-control black-control">
                    <label for="${prefix}EndDate">Tanggal Akhir</label>
                    <input type="date" id="${prefix}EndDate" class="search-input" value="${state.filters.endDate}">
                </div>
                
                <!-- Red Controls (2) -->
                <div class="search-control red-control">
                    <label for="${prefix}SortColumn">Sort By</label>
                    <select id="${prefix}SortColumn" class="search-select">
                        <option value="">Pilih Kolom</option>
                    </select>
                </div>
                <div class="search-control red-control">
                    <label for="${prefix}SortOrder">Order</label>
                    <select id="${prefix}SortOrder" class="search-select">
                        <option value="ASC" ${state.filters.sortOrder === 'ASC' ? 'selected' : ''}>ASC</option>
                        <option value="DESC" ${state.filters.sortOrder === 'DESC' ? 'selected' : ''}>DESC</option>
                    </select>
                </div>
                
                <!-- Green Controls (2) -->
                <div class="search-control green-control">
                    <label for="${prefix}FilterColumn">Pilih Kolom</label>
                    <select id="${prefix}FilterColumn" class="search-select">
                        <option value="">Pilih Kolom</option>
                    </select>
                </div>
                <div class="search-control green-control">
                    <label for="${prefix}FilterValue">Nilai yang Dicari</label>
                    <input type="text" id="${prefix}FilterValue" class="search-input" placeholder="Masukkan nilai" value="${state.filters.filterValue}">
                </div>
            </div>
            
            <!-- Bottom Row (2 main action buttons) -->
            <div class="search-controls-bottom-row">
                <div class="search-control light-blue-control">
                    <button id="${prefix}ApplyAllFilters" class="search-btn primary-btn">
                        <img src="/static/Search_Logo-removebg-preview.png" alt="Search" class="btn-icon">
                        <span>Search</span>
                    </button>
                </div>
                <div class="search-control light-blue-control">
                    <button id="${prefix}ClearAllFilters" class="search-btn secondary-btn">
                        <img src="/static/Clear_Logo-removebg-preview.png" alt="Clear" class="btn-icon">
                        <span>Clear</span>
                    </button>
                </div>
            </div>
        </div>
        
        <div class="table-container">
            ${state.hasData ? state.tableHtml : `
            <div class="no-data-container">
                <h3>Data Belum Tersedia</h3>
                <p>Silakan pilih rentang waktu terlebih dahulu untuk menampilkan data.</p>
                <div class="upload-instructions">
                    <h4>Cara Menampilkan Data:</h4>
                    <ol>
                        <li>Upload file .txt menggunakan form di sebelah kiri</li>
                        <li>Pilih rentang waktu yang diinginkan</li>
                        <li>Klik tombol "Filter Data"</li>
                        <li>Data akan muncul sesuai rentang waktu yang dipilih</li>
                    </ol>
                </div>
            </div>
            `}
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
            sortColumnSelect.innerHTML = '<option value="">Pilih Kolom</option>';
            
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
            filterColumnSelect.innerHTML = '<option value="">Pilih Kolom</option>';
            
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
    
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    
    if (!sortColumn) {
        notificationSystem.warning('Please select a column to sort', 'Required');
        return;
    }
    
    // Update filters state
    updateFiltersState(viewType, { sortColumn, sortOrder });
    
    // Show loading state
    const applySortBtn = document.getElementById(`${prefix}ApplySort`);
    const originalText = applySortBtn.textContent;
    applySortBtn.textContent = 'Sorting...';
    applySortBtn.disabled = true;
    
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
            // Restore button state
            applySortBtn.textContent = originalText;
            applySortBtn.disabled = false;
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
    
    const startDate = document.getElementById(`${prefix}StartDate`).value;
    const endDate = document.getElementById(`${prefix}EndDate`).value;
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    const filterColumn = document.getElementById(`${prefix}FilterColumn`).value;
    const filterValue = document.getElementById(`${prefix}FilterValue`).value;
    
    // Check if at least one filter is applied
    if (!startDate && !endDate && !filterColumn && !filterValue) {
        notificationSystem.warning('Please select at least one filter criteria', 'Required');
        return;
    }
    
    // Update filters state
    updateFiltersState(viewType, { startDate, endDate, sortColumn, sortOrder, filterColumn, filterValue });
    
    // Show loading state
    const applyFilterBtn = document.getElementById(`${prefix}ApplyAllFilters`);
    const originalText = applyFilterBtn.querySelector('span').textContent;
    applyFilterBtn.querySelector('span').textContent = 'Searching...';
    applyFilterBtn.disabled = true;
    
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
                
                // Show success message with applied filters info
                let appliedFilters = [];
                if (startDate || endDate) appliedFilters.push('Date Range');
                if (sortColumn) appliedFilters.push('Sorting');
                if (filterColumn && filterValue) appliedFilters.push('Specific Filter');
                
                notificationSystem.success(`Data filtered successfully! Applied: ${appliedFilters.join(', ')}`, 'Success');
            }
        })
        .catch(error => {
            console.error(`Error applying ${viewType} filters:`, error);
            notificationSystem.error('Search failed. Please try again.', 'Error');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.querySelector('span').textContent = originalText;
            applyFilterBtn.disabled = false;
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
    
    // Clear all inputs
    document.getElementById(`${prefix}StartDate`).value = '';
    document.getElementById(`${prefix}EndDate`).value = '';
    document.getElementById(`${prefix}SortColumn`).value = '';
    document.getElementById(`${prefix}SortOrder`).value = 'ASC';
    document.getElementById(`${prefix}FilterColumn`).value = '';
    document.getElementById(`${prefix}FilterValue`).value = '';
    
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
    const originalText = clearFilterBtn.querySelector('span').textContent;
    clearFilterBtn.querySelector('span').textContent = 'Loading...';
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
            clearFilterBtn.querySelector('span').textContent = originalText;
            clearFilterBtn.disabled = false;
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
    
    // Clear all inputs
    document.getElementById(`${prefix}StartDate`).value = '';
    document.getElementById(`${prefix}EndDate`).value = '';
    document.getElementById(`${prefix}SortColumn`).value = '';
    document.getElementById(`${prefix}SortOrder`).value = 'ASC';
    document.getElementById(`${prefix}FilterColumn`).value = '';
    document.getElementById(`${prefix}FilterValue`).value = '';
    
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
    
    const filterColumn = document.getElementById(`${prefix}FilterColumn`).value;
    const filterValue = document.getElementById(`${prefix}FilterValue`).value;
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    const startDate = document.getElementById(`${prefix}StartDate`).value;
    const endDate = document.getElementById(`${prefix}EndDate`).value;
    
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
            <p><strong>Total Baris Data:</strong> ${summary.total_rows}</p>
            <p><strong>Penyesuaian Harga Diterapkan:</strong> ${summary.pricing_adjustments_applied}</p>
            <div class="inacbg-breakdown">
                <h4>Breakdown INACBG:</h4>
                <ul>
                    <li>Digit 4 = '0' (79%): ${summary.inacbg_0_count} baris</li>
                    <li>Digit 4 = 'I/II/III' (73%): ${summary.inacbg_i_ii_iii_count} baris</li>
                    <li>Lainnya (100%): ${summary.inacbg_other_count} baris</li>
                </ul>
            </div>
            <div class="processing-note">
                <p><strong>Catatan:</strong> Data yang ditampilkan telah diproses dengan penyesuaian harga berdasarkan digit ke-4 INACBG.</p>
            </div>
        `;
    }
}


// Function to update data management information
function updateDataManagementInfo() {
    fetch('/accumulation-info')
        .then(response => response.json())
        .then(data => {
            const dataInfo = document.getElementById('dataInfo');
            const clearBtn = document.getElementById('clearAllDataBtn');
            
            if (data.has_data) {
                dataInfo.innerHTML = `
                    <div class="data-status">
                        <div class="status-indicator active"></div>
                        <span>${data.upload_count} files uploaded</span>
                    </div>
                    <div class="data-status">
                        <div class="status-indicator active"></div>
                        <span>${data.accumulated_rows} total rows</span>
                    </div>
                `;
                clearBtn.disabled = false;
            } else {
                dataInfo.innerHTML = `
                    <div class="data-status">
                        <div class="status-indicator"></div>
                        <span>No data uploaded</span>
                    </div>
                `;
                clearBtn.disabled = true;
            }
        })
        .catch(error => {
            console.error('Error fetching accumulation info:', error);
        });
}

// Function to clear all accumulated data
function clearAllData() {
    if (!confirm('Are you sure you want to clear all accumulated data? This action cannot be undone.')) {
        return;
    }
    
    const clearBtn = document.getElementById('clearAllDataBtn');
    const originalText = clearBtn.querySelector('span').textContent;
    
    // Show loading state
    clearBtn.querySelector('span').textContent = 'Clearing...';
    clearBtn.disabled = true;
    
    fetch('/clear-all-data', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Clear all view states
        Object.keys(viewStates).forEach(viewType => {
            updateViewState(viewType, {
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
            });
        });
        
        // Update data management info
        updateDataManagementInfo();
        
        // Show success message
        notificationSystem.success('All data cleared successfully!', 'Success');
        
        // Return to home view
        showContent('home');
    })
    .catch(error => {
        console.error('Error clearing data:', error);
        notificationSystem.error('Failed to clear data. Please try again.', 'Error');
    })
    .finally(() => {
        // Restore button state
        clearBtn.querySelector('span').textContent = originalText;
        clearBtn.disabled = false;
    });
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
    const mainContent = document.querySelector('.main-content');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    
    // Load saved sidebar state
    const savedWidth = localStorage.getItem('sidebarWidth');
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    
    if (savedWidth && !isCollapsed) {
        sidebar.style.width = savedWidth + 'px';
        mainContent.style.marginLeft = savedWidth + 'px';
    }
    
    if (isCollapsed) {
        sidebar.classList.add('collapsed');
        sidebarToggle.classList.add('active');
        mainContent.style.marginLeft = '60px';
    }
    
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
            
            // Update main content to match sidebar width and prevent overlap
            mainContent.style.marginLeft = newWidth + 'px';
            mainContent.style.width = `calc(100% - ${newWidth}px)`;
            mainContent.style.backgroundColor = 'var(--gray-50)';
            mainContent.style.position = 'relative';
            mainContent.style.zIndex = '1';
            mainContent.style.left = '0';
            mainContent.style.top = '0';
            
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
            
            // Get final width and ensure main content is properly adjusted
            const finalWidth = sidebar.offsetWidth;
            
            // Force update main content to match final sidebar width
            mainContent.style.marginLeft = finalWidth + 'px';
            mainContent.style.width = `calc(100% - ${finalWidth}px)`;
            mainContent.style.backgroundColor = 'var(--gray-50)';
            
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
    const mainContent = document.querySelector('.main-content');
    
    if (sidebar && mainContent) {
        const sidebarWidth = sidebar.offsetWidth;
        
        // Ensure sidebar positioning
        sidebar.style.position = 'fixed';
        sidebar.style.left = '0';
        sidebar.style.top = '0';
        sidebar.style.zIndex = '1001';
        
        // Ensure main content matches sidebar width and prevents overlap
        mainContent.style.marginLeft = sidebarWidth + 'px';
        mainContent.style.width = `calc(100% - ${sidebarWidth}px)`;
        mainContent.style.backgroundColor = 'var(--gray-50)';
        mainContent.style.position = 'relative';
        mainContent.style.zIndex = '1';
        mainContent.style.left = '0';
        mainContent.style.top = '0';
        
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
            sidebarToggle.style.display = 'flex';
            sidebar.style.width = '280px';
            sidebar.style.minWidth = '280px';
            sidebar.style.maxWidth = '280px';
            
            if (!sidebar.classList.contains('open')) {
                sidebar.style.transform = 'translateX(-100%)';
            }
            
            // Update main content margin
            const mainContent = document.querySelector('.main-content');
            if (mainContent) {
                mainContent.style.marginLeft = '0';
                mainContent.style.width = '100%';
            }
        } else {
            // Desktop view
            sidebarToggle.style.display = 'none';
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('active');
            sidebar.style.transform = '';
            sidebar.style.minWidth = '';
            sidebar.style.maxWidth = '';
            
            // Restore saved state
            const savedWidth = localStorage.getItem('sidebarWidth');
            const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
            const mainContent = document.querySelector('.main-content');
            
            if (isCollapsed) {
                sidebar.classList.add('collapsed');
                sidebar.style.width = '60px';
                if (mainContent) {
                    mainContent.style.marginLeft = '60px';
                    mainContent.style.width = 'calc(100% - 60px)';
                }
            } else if (savedWidth) {
                sidebar.style.width = savedWidth + 'px';
                if (mainContent) {
                    mainContent.style.marginLeft = savedWidth + 'px';
                    mainContent.style.width = `calc(100% - ${savedWidth}px)`;
                }
            } else {
                sidebar.style.width = '280px';
                if (mainContent) {
                    mainContent.style.marginLeft = '280px';
                    mainContent.style.width = 'calc(100% - 280px)';
                }
            }
            
            // Force desktop margin
            if (mainContent) {
                const sidebarWidth = sidebar.style.width || '280px';
                mainContent.style.marginLeft = sidebarWidth;
                mainContent.style.width = `calc(100% - ${sidebarWidth})`;
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
        sidebarToggle.style.display = 'flex';
        sidebar.style.width = '280px';
        sidebar.style.minWidth = '280px';
        sidebar.style.maxWidth = '280px';
        sidebar.style.transform = 'translateX(-100%)';
        
        // Update main content margin
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.style.marginLeft = '0';
            mainContent.style.width = '100%';
        }
    } else {
        sidebarToggle.style.display = 'none';
        sidebar.style.transform = '';
        
        // Restore saved state or use default
        const savedWidth = localStorage.getItem('sidebarWidth');
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        const mainContent = document.querySelector('.main-content');
        
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
            sidebar.style.width = '60px';
            if (mainContent) {
                mainContent.style.marginLeft = '60px';
                mainContent.style.width = 'calc(100% - 60px)';
            }
        } else if (savedWidth) {
            sidebar.style.width = savedWidth + 'px';
            if (mainContent) {
                mainContent.style.marginLeft = savedWidth + 'px';
                mainContent.style.width = `calc(100% - ${savedWidth}px)`;
            }
        } else {
            sidebar.style.width = '280px';
            if (mainContent) {
                mainContent.style.marginLeft = '280px';
                mainContent.style.width = 'calc(100% - 280px)';
            }
        }
        
        // Force desktop margin
        if (mainContent) {
            const sidebarWidth = sidebar.style.width || '280px';
            mainContent.style.marginLeft = sidebarWidth;
            mainContent.style.width = `calc(100% - ${sidebarWidth})`;
        }
    }
}

// Toggle sidebar (mobile)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (window.innerWidth <= 768) {
        // Mobile toggle
        sidebar.classList.toggle('open');
        sidebarOverlay.classList.toggle('active');
        
        if (sidebar.classList.contains('open')) {
            toggleIcon.textContent = '✕';
            sidebar.style.transform = 'translateX(0)';
        } else {
            toggleIcon.textContent = '☰';
            sidebar.style.transform = 'translateX(-100%)';
        }
    } else {
        // Desktop collapse/expand
        sidebar.classList.toggle('collapsed');
        sidebarToggle.classList.toggle('active');
        
        const mainContent = document.querySelector('.main-content');
        
        if (sidebar.classList.contains('collapsed')) {
            sidebar.style.width = '60px';
            sidebar.style.minWidth = '60px';
            sidebar.style.maxWidth = '60px';
            if (mainContent) mainContent.style.marginLeft = '60px';
            toggleIcon.textContent = '→';
            localStorage.setItem('sidebarCollapsed', 'true');
        } else {
            const savedWidth = localStorage.getItem('sidebarWidth') || '280';
            sidebar.style.width = savedWidth + 'px';
            sidebar.style.minWidth = '';
            sidebar.style.maxWidth = '';
            if (mainContent) mainContent.style.marginLeft = savedWidth + 'px';
            toggleIcon.textContent = '☰';
            localStorage.setItem('sidebarCollapsed', 'false');
        }
    }
}

// Close sidebar (mobile)
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const toggleIcon = document.getElementById('toggleIcon');
    
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
    sidebar.style.transform = 'translateX(-100%)';
    toggleIcon.textContent = '☰';
}

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
    const contentSections = ['home', 'keuangan', 'pasien', 'selisih-tarif', 'los', 'inacbg', 'ventilator'];
    
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

// Function to update active menu item
function updateActiveMenu(content) {
    // Remove active class from all menu items
    const menuItems = document.querySelectorAll('.menu-item > a');
    menuItems.forEach(item => item.classList.remove('active'));
    const subItems = document.querySelectorAll('.submenu-item, .submenu-item a');
    subItems.forEach(item => item.classList.remove('active'));
    
    // Add active class to the clicked menu item
    if (content === 'home') {
        document.querySelector('.menu-item > a[onclick*="home"]').classList.add('active');
    } else if (content === 'keuangan' || content === 'pasien') {
        document.querySelector('.menu-item > a[onclick*="analytics-dropdown"]').classList.add('active');
    } else if (content === 'selisih-tarif' || content === 'los' || content === 'inacbg' || content === 'ventilator') {
        document.querySelector('.menu-item > a[onclick*="analisa-dropdown"]').classList.add('active');
    }

    // Highlight the active submenu item
    const submenuSelectorMap = {
        'keuangan': "#analytics-dropdown .submenu-item a[onclick*='keuangan']",
        'pasien': "#analytics-dropdown .submenu-item a[onclick*='pasien']",
        'selisih-tarif': "#analisa-dropdown .submenu-item a[onclick*='selisih-tarif']",
        'los': "#analisa-dropdown .submenu-item a[onclick*='los']",
        'inacbg': "#analisa-dropdown .submenu-item a[onclick*='inacbg']",
        'ventilator': "#analisa-dropdown .submenu-item a[onclick*='ventilator']"
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
            const parentMenuItem = parentSubmenu.closest('.menu-item');
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
    var parentMenuItem = dropdown.closest('.menu-item');
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
            
            // Show success message
            notificationSystem.success('File uploaded successfully!', 'Success');
            
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
        
        <!-- Date Range Filter Controls (Paling Atas) -->
        <div class="date-filter-controls">
            <div class="filter-group">
                <label for="${prefix}StartDate">Tanggal Mulai:</label>
                <input type="date" id="${prefix}StartDate" class="date-input" value="${state.filters.startDate}">
            </div>
            <div class="filter-group">
                <label for="${prefix}EndDate">Tanggal Akhir:</label>
                <input type="date" id="${prefix}EndDate" class="date-input" value="${state.filters.endDate}">
            </div>
            <button id="${prefix}ApplyDateFilter" class="filter-btn">Filter Data</button>
            <button id="${prefix}ClearDateFilter" class="clear-btn">Clear Filter</button>
        </div>
        
        <!-- Sorting Controls (Tengah) -->
        <div class="sorting-controls">
            <div class="sort-group">
                <label for="${prefix}SortColumn">Sort By:</label>
                <select id="${prefix}SortColumn" class="sort-select">
                    <option value="">Pilih Kolom</option>
                </select>
            </div>
            <div class="sort-group">
                <label for="${prefix}SortOrder">Order:</label>
                <select id="${prefix}SortOrder" class="sort-select">
                    <option value="ASC" ${state.filters.sortOrder === 'ASC' ? 'selected' : ''}>ASC</option>
                    <option value="DESC" ${state.filters.sortOrder === 'DESC' ? 'selected' : ''}>DESC</option>
                </select>
            </div>
            <button id="${prefix}ApplySort" class="sort-btn">Apply Sort</button>
        </div>
        
        <!-- Specific Data Filter Controls (Paling Bawah) -->
        <div class="specific-filter-controls">
            <div class="filter-group">
                <label for="${prefix}FilterColumn">Pilih Kolom:</label>
                <select id="${prefix}FilterColumn" class="filter-select">
                    <option value="">Pilih Kolom</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="${prefix}FilterValue">Nilai yang Dicari:</label>
                <input type="text" id="${prefix}FilterValue" class="filter-input" placeholder="Masukkan nilai yang dicari" value="${state.filters.filterValue}">
            </div>
            <button id="${prefix}ApplySpecificFilter" class="specific-filter-btn">Cari</button>
            <button id="${prefix}ClearSpecificFilter" class="clear-specific-btn">Clear</button>
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
    document.getElementById(`${prefix}ApplySort`).addEventListener('click', () => applySorting(viewType));
    document.getElementById(`${prefix}ApplyDateFilter`).addEventListener('click', () => applyDateFilter(viewType));
    document.getElementById(`${prefix}ClearDateFilter`).addEventListener('click', () => clearDateFilter(viewType));
    document.getElementById(`${prefix}ApplySpecificFilter`).addEventListener('click', () => applySpecificFilter(viewType));
    document.getElementById(`${prefix}ClearSpecificFilter`).addEventListener('click', () => clearSpecificFilter(viewType));
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

// Generic function to apply date filter
function applyDateFilter(viewType) {
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
    
    if (!startDate && !endDate) {
        notificationSystem.warning('Please select at least one date', 'Required');
        return;
    }
    
    // Update filters state
    updateFiltersState(viewType, { startDate, endDate, sortColumn, sortOrder });
    
    // Show loading state
    const applyFilterBtn = document.getElementById(`${prefix}ApplyDateFilter`);
    const originalText = applyFilterBtn.textContent;
    applyFilterBtn.textContent = 'Filtering...';
    applyFilterBtn.disabled = true;
    
    // Build query parameters
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    if (sortColumn) params.append('sort_column', sortColumn);
    if (sortOrder) params.append('sort_order', sortOrder);
    
    // Make API call to get filtered data
    fetch(`/${viewType}/filter?${params.toString()}`)
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
            console.error(`Error applying ${viewType} date filter:`, error);
            notificationSystem.error('Filtering failed. Please try again.', 'Error');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Generic function to clear date filter
function clearDateFilter(viewType) {
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
    
    // Clear date inputs
    document.getElementById(`${prefix}StartDate`).value = '';
    document.getElementById(`${prefix}EndDate`).value = '';
    
    // Update filters state
    updateFiltersState(viewType, { startDate: '', endDate: '' });
    
    // Reload original data without filters
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    
    // Show loading state
    const clearFilterBtn = document.getElementById(`${prefix}ClearDateFilter`);
    const originalText = clearFilterBtn.textContent;
    clearFilterBtn.textContent = 'Clearing...';
    clearFilterBtn.disabled = true;
    
    // Build query parameters for sorting only
    const params = new URLSearchParams();
    if (sortColumn) params.append('sort_column', sortColumn);
    if (sortOrder) params.append('sort_order', sortOrder);
    
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
            console.error(`Error clearing ${viewType} date filter:`, error);
            notificationSystem.error('Clear failed. Please try again.', 'Error');
        })
        .finally(() => {
            // Restore button state
            clearFilterBtn.textContent = originalText;
            clearFilterBtn.disabled = false;
        });
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


// Initialize the page with Home content as default
document.addEventListener('DOMContentLoaded', function() {
    // Show Home content by default
    showContent('home');
    
    // Initialize upload button as disabled
    const uploadBtn = document.getElementById('uploadBtn');
    if (uploadBtn) {
        uploadBtn.disabled = true;
    }
    
    
    // Add animation to feature cards
    animateFeatureCards();
    
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

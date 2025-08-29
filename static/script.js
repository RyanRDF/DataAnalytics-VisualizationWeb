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
    }
};

// Function to show content based on button clicked
function showContent(content) {
    // Hide all content first
    document.getElementById('home').style.display = 'none';
    document.getElementById('keuangan').style.display = 'none';
    document.getElementById('pasien').style.display = 'none';
    
    // Show the selected content
    document.getElementById(content).style.display = 'block';
    
    // Update active menu item
    updateActiveMenu(content);
    
    // Handle special content loading
    if (content === 'keuangan') {
        loadDataView('keuangan');
    } else if (content === 'pasien') {
        loadDataView('pasien');
    }
}

// Function to update active menu item
function updateActiveMenu(content) {
    // Remove active class from all menu items
    const menuItems = document.querySelectorAll('.menu-item > a');
    menuItems.forEach(item => item.classList.remove('active'));
    
    // Add active class to the clicked menu item
    if (content === 'home') {
        document.querySelector('.menu-item > a[onclick*="home"]').classList.add('active');
    } else if (content === 'keuangan' || content === 'pasien') {
        document.querySelector('.menu-item > a[onclick*="analytics-dropdown"]').classList.add('active');
    }
}

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
            // Extract table HTML and update both view states
            const tableHtml = tableContainer.innerHTML;
            
            // Update both keuangan and pasien states with the uploaded data
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
            
            // Show success message
            alert('File berhasil diproses! Data tersedia di menu Keuangan dan Pasien.');
        } else {
            alert('File berhasil diupload tetapi tidak ada data yang dapat ditampilkan.');
        }
        
        // Reset form
        event.target.reset();
        document.getElementById('fileInfo').textContent = 'No file selected.';
        document.getElementById('fileInfo').style.color = '#555';
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        alert('Terjadi kesalahan saat mengupload file.');
    })
    .finally(() => {
        // Restore button state
        uploadBtn.textContent = 'Process File';
        uploadBtn.disabled = true;
    });
}

// Generic function to load data view (keuangan or pasien)
function loadDataView(viewType) {
    const content = document.getElementById(viewType);
    const isKeuangan = viewType === 'keuangan';
    const prefix = isKeuangan ? '' : 'pasien';
    const state = viewStates[viewType];
    
    // Set content dengan urutan filter yang baru - data tidak langsung muncul
    content.innerHTML = `
        <h2>Analisis ${isKeuangan ? 'Keuangan' : 'Pasien'}</h2>
        <p>Menampilkan analisis data ${isKeuangan ? 'keuangan dengan perhitungan laba rugi' : 'pasien dengan informasi medis lengkap'}</p>
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
    const prefix = viewType === 'keuangan' ? '' : 'pasien';
    
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
    const prefix = viewType === 'keuangan' ? '' : 'pasien';
    
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
    const prefix = viewType === 'keuangan' ? '' : 'pasien';
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    
    if (!sortColumn) {
        alert('Silakan pilih kolom untuk sorting');
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
                alert('Error: ' + data.error);
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
            alert('Terjadi kesalahan saat melakukan sorting');
        })
        .finally(() => {
            // Restore button state
            applySortBtn.textContent = originalText;
            applySortBtn.disabled = false;
        });
}

// Generic function to apply date filter
function applyDateFilter(viewType) {
    const prefix = viewType === 'keuangan' ? '' : 'pasien';
    const startDate = document.getElementById(`${prefix}StartDate`).value;
    const endDate = document.getElementById(`${prefix}EndDate`).value;
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    
    if (!startDate && !endDate) {
        alert('Silakan pilih minimal satu tanggal untuk filtering');
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
                alert('Error: ' + data.error);
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
            alert('Terjadi kesalahan saat melakukan filtering');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Generic function to clear date filter
function clearDateFilter(viewType) {
    const prefix = viewType === 'keuangan' ? '' : 'pasien';
    
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
                alert('Error: ' + data.error);
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
            alert('Terjadi kesalahan saat membersihkan filter');
        })
        .finally(() => {
            // Restore button state
            clearFilterBtn.textContent = originalText;
            clearFilterBtn.disabled = false;
        });
}

// Generic function to apply specific filter
function applySpecificFilter(viewType) {
    const prefix = viewType === 'keuangan' ? '' : 'pasien';
    const filterColumn = document.getElementById(`${prefix}FilterColumn`).value;
    const filterValue = document.getElementById(`${prefix}FilterValue`).value;
    const sortColumn = document.getElementById(`${prefix}SortColumn`).value;
    const sortOrder = document.getElementById(`${prefix}SortOrder`).value;
    const startDate = document.getElementById(`${prefix}StartDate`).value;
    const endDate = document.getElementById(`${prefix}EndDate`).value;
    
    if (!filterColumn || !filterValue) {
        alert('Silakan pilih kolom dan masukkan nilai yang dicari');
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
                alert('Error: ' + data.error);
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
            alert('Terjadi kesalahan saat melakukan pencarian');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Generic function to clear specific filter
function clearSpecificFilter(viewType) {
    const prefix = viewType === 'keuangan' ? '' : 'pasien';
    
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
                alert('Error: ' + data.error);
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
            alert('Terjadi kesalahan saat membersihkan filter');
        })
        .finally(() => {
            // Restore button state
            clearFilterBtn.textContent = originalText;
            clearFilterBtn.disabled = false;
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
});


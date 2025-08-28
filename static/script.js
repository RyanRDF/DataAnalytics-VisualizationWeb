// Function to show content based on button clicked
function showContent(content) {
    // Hide all content first
    document.getElementById('home').style.display = 'none';
    document.getElementById('keuangan').style.display = 'none';
    document.getElementById('pasien').style.display = 'none';
    document.getElementById('dokter').style.display = 'none';
    document.getElementById('charts').style.display = 'none';
    document.getElementById('graphs').style.display = 'none';
    document.getElementById('reports').style.display = 'none';
    
    // Show the selected content
    document.getElementById(content).style.display = 'block';
    
    // Update active menu item
    updateActiveMenu(content);
    
    // Handle special content loading
    if (content === 'keuangan') {
        loadKeuanganData();
    } else if (content === 'pasien') {
        loadPasienData();
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
    } else if (content === 'keuangan' || content === 'pasien' || content === 'dokter') {
        document.querySelector('.menu-item > a[onclick*="analytics-dropdown"]').classList.add('active');
    } else if (content === 'charts' || content === 'graphs' || content === 'reports') {
        document.querySelector('.menu-item > a[onclick*="visualize-dropdown"]').classList.add('active');
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

// Function to load keuangan data via AJAX
function loadKeuanganData() {
    const keuanganContent = document.getElementById('keuangan');
    
    // Set content dengan urutan filter yang baru - data tidak langsung muncul
    keuanganContent.innerHTML = `
        <h2>Analisis Keuangan</h2>
        <p>Menampilkan analisis data keuangan dengan perhitungan laba rugi</p>
        <p class="data-notice"><strong>⚠️ Data hanya akan muncul setelah Anda memilih rentang waktu!</strong></p>
        
        <!-- Date Range Filter Controls (Paling Atas) -->
        <div class="date-filter-controls">
            <div class="filter-group">
                <label for="startDate">Tanggal Mulai:</label>
                <input type="date" id="startDate" class="date-input">
            </div>
            <div class="filter-group">
                <label for="endDate">Tanggal Akhir:</label>
                <input type="date" id="endDate" class="date-input">
            </div>
            <button id="applyDateFilter" class="filter-btn">Filter Data</button>
            <button id="clearDateFilter" class="clear-btn">Clear Filter</button>
        </div>
        
        <!-- Sorting Controls (Tengah) -->
        <div class="sorting-controls">
            <div class="sort-group">
                <label for="sortColumn">Sort By:</label>
                <select id="sortColumn" class="sort-select">
                    <option value="">Pilih Kolom</option>
                </select>
            </div>
            <div class="sort-group">
                <label for="sortOrder">Order:</label>
                <select id="sortOrder" class="sort-select">
                    <option value="ASC">ASC</option>
                    <option value="DESC">DESC</option>
                </select>
            </div>
            <button id="applySort" class="sort-btn">Apply Sort</button>
        </div>
        
        <!-- Specific Data Filter Controls (Paling Bawah) -->
        <div class="specific-filter-controls">
            <div class="filter-group">
                <label for="filterColumn">Pilih Kolom:</label>
                <select id="filterColumn" class="filter-select">
                    <option value="">Pilih Kolom</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="filterValue">Nilai yang Dicari:</label>
                <input type="text" id="filterValue" class="filter-input" placeholder="Masukkan nilai yang dicari">
            </div>
            <button id="applySpecificFilter" class="specific-filter-btn">Cari</button>
            <button id="clearSpecificFilter" class="clear-specific-btn">Clear</button>
        </div>
        
        <div class="table-container">
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
        </div>
    `;
    
    // Load filter columns
    loadFilterColumns();
    loadSortingColumns();
    
    // Attach event listeners
    document.getElementById('applySort').addEventListener('click', applySorting);
    document.getElementById('applyDateFilter').addEventListener('click', applyDateFilter);
    document.getElementById('clearDateFilter').addEventListener('click', clearDateFilter);
    document.getElementById('applySpecificFilter').addEventListener('click', applySpecificFilter);
    document.getElementById('clearSpecificFilter').addEventListener('click', clearSpecificFilter);
}

// Function to load available columns for sorting
function loadSortingColumns() {
    fetch('/keuangan/columns')
        .then(response => response.json())
        .then(data => {
            const sortColumnSelect = document.getElementById('sortColumn');
            
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
            console.error('Error loading sorting columns:', error);
        });
}

// Function to load available columns for filtering
function loadFilterColumns() {
    fetch('/keuangan/columns')
        .then(response => response.json())
        .then(data => {
            const filterColumnSelect = document.getElementById('filterColumn');
            
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
            console.error('Error loading filter columns:', error);
        });
}

// Function to apply sorting
function applySorting() {
    const sortColumn = document.getElementById('sortColumn').value;
    const sortOrder = document.getElementById('sortOrder').value;
    
    if (!sortColumn) {
        alert('Silakan pilih kolom untuk sorting');
        return;
    }
    
    // Show loading state
    const applySortBtn = document.getElementById('applySort');
    const originalText = applySortBtn.textContent;
    applySortBtn.textContent = 'Sorting...';
    applySortBtn.disabled = true;
    
    // Make API call to get sorted data
    fetch(`/keuangan/sort?column=${encodeURIComponent(sortColumn)}&order=${encodeURIComponent(sortOrder)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with sorted data
            const tableContainer = document.querySelector('#keuangan .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error applying sorting:', error);
            alert('Terjadi kesalahan saat melakukan sorting');
        })
        .finally(() => {
            // Restore button state
            applySortBtn.textContent = originalText;
            applySortBtn.disabled = false;
        });
}

// Function to apply date filter
function applyDateFilter() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const sortColumn = document.getElementById('sortColumn').value;
    const sortOrder = document.getElementById('sortOrder').value;
    
    if (!startDate && !endDate) {
        alert('Silakan pilih minimal satu tanggal untuk filtering');
        return;
    }
    
    // Show loading state
    const applyFilterBtn = document.getElementById('applyDateFilter');
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
    fetch(`/keuangan/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with filtered data
            const tableContainer = document.querySelector('#keuangan .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error applying date filter:', error);
            alert('Terjadi kesalahan saat melakukan filtering');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Function to clear date filter
function clearDateFilter() {
    // Clear date inputs
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    
    // Reload original data without filters
    const sortColumn = document.getElementById('sortColumn').value;
    const sortOrder = document.getElementById('sortOrder').value;
    
    // Show loading state
    const clearFilterBtn = document.getElementById('clearDateFilter');
    const originalText = clearFilterBtn.textContent;
    clearFilterBtn.textContent = 'Clearing...';
    clearFilterBtn.disabled = true;
    
    // Build query parameters for sorting only
    const params = new URLSearchParams();
    if (sortColumn) params.append('sort_column', sortColumn);
    if (sortOrder) params.append('sort_order', sortOrder);
    
    // Make API call to get original data
    fetch(`/keuangan/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with original data
            const tableContainer = document.querySelector('#keuangan .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error clearing date filter:', error);
            alert('Terjadi kesalahan saat membersihkan filter');
        })
        .finally(() => {
            // Restore button state
            clearFilterBtn.textContent = originalText;
            clearFilterBtn.disabled = false;
        });
}

// Function to apply specific filter
function applySpecificFilter() {
    const filterColumn = document.getElementById('filterColumn').value;
    const filterValue = document.getElementById('filterValue').value;
    const sortColumn = document.getElementById('sortColumn').value;
    const sortOrder = document.getElementById('sortOrder').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    if (!filterColumn || !filterValue) {
        alert('Silakan pilih kolom dan masukkan nilai yang dicari');
        return;
    }
    
    // Show loading state
    const applyFilterBtn = document.getElementById('applySpecificFilter');
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
    fetch(`/keuangan/specific-filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with filtered data
            const tableContainer = document.querySelector('#keuangan .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error applying specific filter:', error);
            alert('Terjadi kesalahan saat melakukan pencarian');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Function to clear specific filter
function clearSpecificFilter() {
    // Clear filter inputs
    document.getElementById('filterColumn').value = '';
    document.getElementById('filterValue').value = '';
    
    // Reload original data without specific filter
    const sortColumn = document.getElementById('sortColumn').value;
    const sortOrder = document.getElementById('sortOrder').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    // Show loading state
    const clearFilterBtn = document.getElementById('clearSpecificFilter');
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
    fetch(`/keuangan/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with original data
            const tableContainer = document.querySelector('#keuangan .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error clearing specific filter:', error);
            alert('Terjadi kesalahan saat membersihkan filter');
        })
        .finally(() => {
            // Restore button state
            clearFilterBtn.textContent = originalText;
            clearFilterBtn.disabled = false;
        });
}

// Function to load pasien data via AJAX
function loadPasienData() {
    const pasienContent = document.getElementById('pasien');
    
    // Set content dengan urutan filter yang baru - data tidak langsung muncul
    pasienContent.innerHTML = `
        <h2>Analisis Pasien</h2>
        <p>Menampilkan analisis data pasien dengan informasi medis lengkap</p>
        <p class="data-notice"><strong>⚠️ Data hanya akan muncul setelah Anda memilih rentang waktu!</strong></p>
        
        <!-- Date Range Filter Controls (Paling Atas) -->
        <div class="date-filter-controls">
            <div class="filter-group">
                <label for="pasienStartDate">Tanggal Mulai:</label>
                <input type="date" id="pasienStartDate" class="date-input">
            </div>
            <div class="filter-group">
                <label for="pasienEndDate">Tanggal Akhir:</label>
                <input type="date" id="pasienEndDate" class="date-input">
            </div>
            <button id="pasienApplyDateFilter" class="filter-btn">Filter Data</button>
            <button id="pasienClearDateFilter" class="clear-btn">Clear Filter</button>
        </div>
        
        <!-- Sorting Controls (Tengah) -->
        <div class="sorting-controls">
            <div class="sort-group">
                <label for="pasienSortColumn">Sort By:</label>
                <select id="pasienSortColumn" class="sort-select">
                    <option value="">Pilih Kolom</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="pasienSortOrder">Order:</label>
                <select id="pasienSortOrder" class="sort-select">
                    <option value="ASC">ASC</option>
                    <option value="DESC">DESC</option>
                </select>
            </div>
            <button id="pasienApplySort" class="sort-btn">Apply Sort</button>
        </div>
        
        <!-- Specific Data Filter Controls (Paling Bawah) -->
        <div class="specific-filter-controls">
            <div class="filter-group">
                <label for="pasienFilterColumn">Pilih Kolom:</label>
                <select id="pasienFilterColumn" class="filter-select">
                    <option value="">Pilih Kolom</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="pasienFilterValue">Nilai yang Dicari:</label>
                <input type="text" id="pasienFilterValue" class="filter-input" placeholder="Masukkan nilai yang dicari">
            </div>
            <button id="pasienApplySpecificFilter" class="specific-filter-btn">Cari</button>
            <button id="pasienClearSpecificFilter" class="clear-specific-btn">Clear</button>
        </div>
        
        <div class="table-container">
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
        </div>
    `;
    
    // Load filter columns
    loadPasienFilterColumns();
    loadPasienSortingColumns();
    
    // Attach event listeners
    document.getElementById('pasienApplySort').addEventListener('click', applyPasienSorting);
    document.getElementById('pasienApplyDateFilter').addEventListener('click', applyPasienDateFilter);
    document.getElementById('pasienClearDateFilter').addEventListener('click', clearPasienDateFilter);
    document.getElementById('pasienApplySpecificFilter').addEventListener('click', applyPasienSpecificFilter);
    document.getElementById('pasienClearSpecificFilter').addEventListener('click', clearPasienSpecificFilter);
}

// Function to load available columns for patient sorting
function loadPasienSortingColumns() {
    fetch('/pasien/columns')
        .then(response => response.json())
        .then(data => {
            const sortColumnSelect = document.getElementById('pasienSortColumn');
            
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
            console.error('Error loading patient sorting columns:', error);
        });
}

// Function to load available columns for patient filtering
function loadPasienFilterColumns() {
    fetch('/pasien/columns')
        .then(response => response.json())
        .then(data => {
            const filterColumnSelect = document.getElementById('pasienFilterColumn');
            
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
            console.error('Error loading patient filter columns:', error);
        });
}

// Function to apply patient sorting
function applyPasienSorting() {
    const sortColumn = document.getElementById('pasienSortColumn').value;
    const sortOrder = document.getElementById('pasienSortOrder').value;
    
    if (!sortColumn) {
        alert('Silakan pilih kolom untuk sorting');
        return;
    }
    
    // Show loading state
    const applySortBtn = document.getElementById('pasienApplySort');
    const originalText = applySortBtn.textContent;
    applySortBtn.textContent = 'Sorting...';
    applySortBtn.disabled = true;
    
    // Make API call to get sorted data
    fetch(`/pasien/sort?column=${encodeURIComponent(sortColumn)}&order=${encodeURIComponent(sortOrder)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with sorted data
            const tableContainer = document.querySelector('#pasien .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error applying patient sorting:', error);
            alert('Terjadi kesalahan saat melakukan sorting');
        })
        .finally(() => {
            // Restore button state
            applySortBtn.textContent = originalText;
            applySortBtn.disabled = false;
        });
}

// Function to apply patient date filter
function applyPasienDateFilter() {
    const startDate = document.getElementById('pasienStartDate').value;
    const endDate = document.getElementById('pasienEndDate').value;
    const sortColumn = document.getElementById('pasienSortColumn').value;
    const sortOrder = document.getElementById('pasienSortOrder').value;
    
    if (!startDate && !endDate) {
        alert('Silakan pilih minimal satu tanggal untuk filtering');
        return;
    }
    
    // Show loading state
    const applyFilterBtn = document.getElementById('pasienApplyDateFilter');
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
    fetch(`/pasien/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with filtered data
            const tableContainer = document.querySelector('#pasien .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error applying patient date filter:', error);
            alert('Terjadi kesalahan saat melakukan filtering');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Function to clear patient date filter
function clearPasienDateFilter() {
    // Clear date inputs
    document.getElementById('pasienStartDate').value = '';
    document.getElementById('pasienEndDate').value = '';
    
    // Reload original data without filters
    const sortColumn = document.getElementById('pasienSortColumn').value;
    const sortOrder = document.getElementById('pasienSortOrder').value;
    
    // Show loading state
    const clearFilterBtn = document.getElementById('pasienClearDateFilter');
    const originalText = clearFilterBtn.textContent;
    clearFilterBtn.textContent = 'Clearing...';
    clearFilterBtn.disabled = true;
    
    // Build query parameters for sorting only
    const params = new URLSearchParams();
    if (sortColumn) params.append('sort_column', sortColumn);
    if (sortOrder) params.append('sort_order', sortOrder);
    
    // Make API call to get original data
    fetch(`/pasien/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with original data
            const tableContainer = document.querySelector('#pasien .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error clearing patient date filter:', error);
            alert('Terjadi kesalahan saat membersihkan filter');
        })
        .finally(() => {
            // Restore button state
            clearFilterBtn.textContent = originalText;
            clearFilterBtn.disabled = false;
        });
}

// Function to apply patient specific filter
function applyPasienSpecificFilter() {
    const filterColumn = document.getElementById('pasienFilterColumn').value;
    const filterValue = document.getElementById('pasienFilterValue').value;
    const sortColumn = document.getElementById('pasienSortColumn').value;
    const sortOrder = document.getElementById('pasienSortOrder').value;
    const startDate = document.getElementById('pasienStartDate').value;
    const endDate = document.getElementById('pasienEndDate').value;
    
    if (!filterColumn || !filterValue) {
        alert('Silakan pilih kolom dan masukkan nilai yang dicari');
        return;
    }
    
    // Show loading state
    const applyFilterBtn = document.getElementById('pasienApplySpecificFilter');
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
    fetch(`/pasien/specific-filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with filtered data
            const tableContainer = document.querySelector('#pasien .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error applying patient specific filter:', error);
            alert('Terjadi kesalahan saat melakukan pencarian');
        })
        .finally(() => {
            // Restore button state
            applyFilterBtn.textContent = originalText;
            applyFilterBtn.disabled = false;
        });
}

// Function to clear patient specific filter
function clearPasienSpecificFilter() {
    // Clear filter inputs
    document.getElementById('pasienFilterColumn').value = '';
    document.getElementById('pasienFilterValue').value = '';
    
    // Reload original data without specific filter
    const sortColumn = document.getElementById('pasienSortColumn').value;
    const sortOrder = document.getElementById('pasienSortOrder').value;
    const startDate = document.getElementById('pasienStartDate').value;
    const endDate = document.getElementById('pasienEndDate').value;
    
    // Show loading state
    const clearFilterBtn = document.getElementById('pasienClearSpecificFilter');
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
    fetch(`/pasien/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Update the table with original data
            const tableContainer = document.querySelector('#pasien .table-container');
            if (tableContainer && data.table_html) {
                tableContainer.innerHTML = data.table_html;
            }
        })
        .catch(error => {
            console.error('Error clearing patient specific filter:', error);
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


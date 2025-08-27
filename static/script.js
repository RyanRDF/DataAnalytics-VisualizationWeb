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
    fetch('/keuangan')
        .then(response => response.text())
        .then(html => {
            // Create a temporary div to parse the HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            
            // Extract the table from the response
            const tableContainer = tempDiv.querySelector('.table-container');
            const errorMessage = tempDiv.querySelector('.error-message');
            
            const keuanganContent = document.getElementById('keuangan');
            
            if (tableContainer) {
                // Clear existing content
                keuanganContent.innerHTML = '<h2>Analisis Keuangan</h2>';
                
                // Add the sorting controls
                const sortingControls = `
                    <p>Menampilkan analisis data keuangan dengan perhitungan laba rugi</p>
                    
                    <!-- Sorting Controls -->
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
                    
                    <!-- Date Range Filter Controls -->
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
                `;
                
                keuanganContent.innerHTML += sortingControls;
                
                // Add the table
                keuanganContent.appendChild(tableContainer.cloneNode(true));
                
                // Load available columns for sorting
                loadSortingColumns();
                
                // Add event listener for sort button
                document.getElementById('applySort').addEventListener('click', applySorting);
                
                // Add event listeners for date filter buttons
                document.getElementById('applyDateFilter').addEventListener('click', applyDateFilter);
                document.getElementById('clearDateFilter').addEventListener('click', clearDateFilter);
            } else if (errorMessage) {
                // Show error message
                keuanganContent.innerHTML = '<h2>Analisis Keuangan</h2>';
                keuanganContent.appendChild(errorMessage.cloneNode(true));
            } else {
                keuanganContent.innerHTML = '<h2>Analisis Keuangan</h2><p>Tidak ada data yang tersedia. Silakan upload file terlebih dahulu.</p>';
            }
        })
        .catch(error => {
            console.error('Error loading keuangan data:', error);
            const keuanganContent = document.getElementById('keuangan');
            keuanganContent.innerHTML = '<h2>Analisis Keuangan</h2><p>Terjadi kesalahan saat memuat data keuangan.</p>';
        });
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

// Function to load pasien data via AJAX
function loadPasienData() {
    fetch('/pasien')
        .then(response => response.text())
        .then(html => {
            // Create a temporary div to parse the HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            
            // Extract the table from the response
            const tableContainer = tempDiv.querySelector('.table-container');
            const errorMessage = tempDiv.querySelector('.error-message');
            
            const pasienContent = document.getElementById('pasien');
            
            if (tableContainer) {
                // Clear existing content
                pasienContent.innerHTML = '<h2>Data Pasien</h2>';
                
                // Add the table
                pasienContent.appendChild(tableContainer.cloneNode(true));
            } else if (errorMessage) {
                // Show error message
                pasienContent.innerHTML = '<h2>Data Pasien</h2>';
                pasienContent.appendChild(errorMessage.cloneNode(true));
            } else {
                pasienContent.innerHTML = '<h2>Data Pasien</h2><p>Tidak ada data yang tersedia. Silakan upload file terlebih dahulu.</p>';
            }
        })
        .catch(error => {
            console.error('Error loading pasien data:', error);
            const pasienContent = document.getElementById('pasien');
            pasienContent.innerHTML = '<h2>Data Pasien</h2><p>Terjadi kesalahan saat memuat data pasien.</p>';
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


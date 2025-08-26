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
                
                // Add the table
                keuanganContent.appendChild(tableContainer.cloneNode(true));
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


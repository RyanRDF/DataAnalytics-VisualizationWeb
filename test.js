// Function to show content based on button clicked
function showContent(content) {
    // Hide all content first
    document.getElementById('keuangan').style.display = 'none';
    document.getElementById('pasien').style.display = 'none';
    document.getElementById('dokter').style.display = 'none';
    
    // Show the selected content
    document.getElementById(content).style.display = 'block';
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
    
    if (file) {
        const fileName = file.name;
        const fileExtension = fileName.split('.').pop().toLowerCase();
        
        // Check if the file extension is allowed
        const allowedExtensions = ['txt', 'csv', 'xls'];
        if (allowedExtensions.includes(fileExtension)) {
            fileInfo.textContent = `Selected file: ${fileName}`;
        } else {
            fileInfo.textContent = 'Invalid file type. Please select a .txt, .csv, or .xls file.';
        }
    } else {
        fileInfo.textContent = 'No file selected.';
    }
}

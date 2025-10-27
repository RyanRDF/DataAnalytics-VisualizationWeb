/**
 * Admin functionality JavaScript
 */

// Global variables
let currentUsers = [];
let currentCodes = [];

// Initialize admin functionality when admin section is shown
function initializeAdmin() {
    console.log('Initializing admin functionality...');
    loadUsersList();
    loadCodesList();
}

// Load users list
async function loadUsersList() {
    try {
        const response = await fetch('/admin/users');
        const data = await response.json();
        
        if (data.success) {
            currentUsers = data.users;
            renderUsersTable(data.users);
        } else {
            showNotification('Error loading users: ' + data.message, 'error');
        }
    } catch (error) {
        console.error('Error loading users:', error);
        showNotification('Error loading users', 'error');
    }
}

// Load registration codes list
async function loadCodesList() {
    try {
        const response = await fetch('/admin/registration-codes');
        const data = await response.json();
        
        if (data.success) {
            currentCodes = data.codes;
            renderCodesTable(data.codes);
        } else {
            showNotification('Error loading codes: ' + data.message, 'error');
        }
    } catch (error) {
        console.error('Error loading codes:', error);
        showNotification('Error loading codes', 'error');
    }
}

// Render users table
function renderUsersTable(users) {
    const tbody = document.getElementById('usersTableBody');
    if (!tbody) return;
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted">Tidak ada data user</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.user_id}</td>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>${user.full_name}</td>
            <td>
                <span class="badge ${getRoleBadgeClass(user.role)}">${user.role}</span>
            </td>
            <td>
                <span class="badge ${user.is_active ? 'bg-success' : 'bg-danger'}">
                    ${user.is_active ? 'Aktif' : 'Tidak Aktif'}
                </span>
            </td>
            <td>${user.last_login ? formatDateTime(user.last_login) : 'Belum pernah'}</td>
            <td>${formatDateTime(user.created_at)}</td>
            <td>
                <div class="btn-group btn-group-sm" role="group">
                    <button type="button" class="btn btn-outline-primary btn-sm" 
                            onclick="resetUserPassword(${user.user_id}, '${user.username}')" 
                            title="Reset Password">
                        <i class="fas fa-key"></i>
                    </button>
                    ${user.user_id !== getCurrentUserId() ? `
                    <button type="button" class="btn btn-outline-danger btn-sm" 
                            onclick="deleteUser(${user.user_id}, '${user.username}')" 
                            title="Hapus User">
                        <i class="fas fa-trash"></i>
                    </button>
                    ` : ''}
                </div>
            </td>
        </tr>
    `).join('');
}

// Render codes table
function renderCodesTable(codes) {
    const tbody = document.getElementById('codesTableBody');
    if (!tbody) return;
    
    if (codes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Tidak ada kode registrasi</td></tr>';
        return;
    }
    
    tbody.innerHTML = codes.map(code => `
        <tr>
            <td><code>${code.code}</code></td>
            <td>
                <span class="badge ${getRoleBadgeClass(code.role)}">${code.role}</span>
            </td>
            <td>
                <span class="badge ${code.is_used ? 'bg-success' : 'bg-warning'}">
                    ${code.is_used ? 'Digunakan' : 'Belum Digunakan'}
                </span>
            </td>
            <td>${code.used_by_name || '-'}</td>
            <td>${code.created_by_name}</td>
            <td>${formatDateTime(code.created_at)}</td>
            <td>${code.expires_at ? formatDateTime(code.expires_at) : 'Tidak ada'}</td>
            <td>
                ${!code.is_used ? `
                <button type="button" class="btn btn-outline-danger btn-sm" 
                        onclick="deleteCode(${code.code_id}, '${code.code}')" 
                        title="Hapus Kode">
                    <i class="fas fa-trash"></i>
                </button>
                ` : '-'}
            </td>
        </tr>
    `).join('');
}

// Get role badge class
function getRoleBadgeClass(role) {
    switch(role) {
        case 'admin': return 'bg-danger';
        case 'user': return 'bg-primary';
        case 'viewer': return 'bg-info';
        default: return 'bg-secondary';
    }
}

// Format datetime
function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('id-ID', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Get current user ID (you'll need to implement this)
function getCurrentUserId() {
    // This should return the current user's ID from session or global variable
    // You might need to pass this from the server or store it in a global variable
    return window.currentUserId || null;
}

// Reset user password
async function resetUserPassword(userId, username) {
    if (!confirm(`Apakah Anda yakin ingin mereset password untuk user "${username}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/users/${userId}/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            // Show new password in a modal or alert
            alert(`Password baru untuk ${username}: ${data.new_password}`);
            loadUsersList(); // Refresh the list
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Error resetting password:', error);
        showNotification('Error resetting password', 'error');
    }
}

// Delete user
async function deleteUser(userId, username) {
    if (!confirm(`Apakah Anda yakin ingin menghapus user "${username}"? Tindakan ini tidak dapat dibatalkan.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/users/${userId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            loadUsersList(); // Refresh the list
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        showNotification('Error deleting user', 'error');
    }
}

// Delete registration code
async function deleteCode(codeId, code) {
    if (!confirm(`Apakah Anda yakin ingin menghapus kode "${code}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/registration-codes/${codeId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            loadCodesList(); // Refresh the list
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Error deleting code:', error);
        showNotification('Error deleting code', 'error');
    }
}

// Show generate code modal
function showGenerateCodeModal() {
    const modal = new bootstrap.Modal(document.getElementById('generateCodeModal'));
    modal.show();
}

// Generate registration codes
async function generateRegistrationCodes() {
    const role = document.getElementById('codeRole').value;
    const expiryDays = parseInt(document.getElementById('codeExpiry').value);
    const count = parseInt(document.getElementById('codeCount').value);
    
    if (!role) {
        showNotification('Pilih role terlebih dahulu', 'error');
        return;
    }
    
    try {
        const response = await fetch('/admin/registration-codes/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                role: role,
                expiry_days: expiryDays,
                count: count
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            
            // Show generated codes
            let codesText = 'Kode yang digenerate:\n\n';
            data.codes.forEach(code => {
                codesText += `${code.code} (${code.role}) - Expires: ${new Date(code.expires_at).toLocaleDateString('id-ID')}\n`;
            });
            alert(codesText);
            
            // Close modal and refresh codes list
            bootstrap.Modal.getInstance(document.getElementById('generateCodeModal')).hide();
            loadCodesList();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Error generating codes:', error);
        showNotification('Error generating codes', 'error');
    }
}

// Refresh users list
function refreshUsersList() {
    loadUsersList();
}

// Show notification (you might need to implement this function)
function showNotification(message, type = 'info') {
    // This should show a notification to the user
    // You can implement this using your existing notification system
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Simple alert for now - you should replace this with a proper notification system
    if (type === 'error') {
        alert('Error: ' + message);
    } else if (type === 'success') {
        alert('Success: ' + message);
    }
}

// Clear unused codes
async function clearUnusedCodes() {
    if (!confirm('Apakah Anda yakin ingin menghapus semua kode yang belum digunakan? Tindakan ini tidak dapat dibatalkan.')) {
        return;
    }
    
    try {
        const response = await fetch('/admin/registration-codes/clear-unused', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            if (data.deleted_count > 0) {
                alert(`Berhasil menghapus ${data.deleted_count} kode:\n${data.deleted_codes.join(', ')}`);
            }
            loadCodesList(); // Refresh the list
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Error clearing unused codes:', error);
        showNotification('Error clearing unused codes', 'error');
    }
}

// Clear expired codes
async function clearExpiredCodes() {
    if (!confirm('Apakah Anda yakin ingin menghapus semua kode yang sudah kadaluarsa? Tindakan ini tidak dapat dibatalkan.')) {
        return;
    }
    
    try {
        const response = await fetch('/admin/registration-codes/clear-expired', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            if (data.deleted_count > 0) {
                alert(`Berhasil menghapus ${data.deleted_count} kode:\n${data.deleted_codes.join(', ')}`);
            }
            loadCodesList(); // Refresh the list
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Error clearing expired codes:', error);
        showNotification('Error clearing expired codes', 'error');
    }
}

// Export functions for global access
window.initializeAdmin = initializeAdmin;
window.showGenerateCodeModal = showGenerateCodeModal;
window.generateRegistrationCodes = generateRegistrationCodes;
window.refreshUsersList = refreshUsersList;
window.resetUserPassword = resetUserPassword;
window.deleteUser = deleteUser;
window.deleteCode = deleteCode;
window.clearUnusedCodes = clearUnusedCodes;
window.clearExpiredCodes = clearExpiredCodes;

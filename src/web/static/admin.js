/**
 * Admin functionality JavaScript
 */

// Global variables
let currentUsers = [];

// Initialize admin functionality when admin section is shown
function initializeAdmin() {
    console.log('Initializing admin functionality...');
    loadUsersList();
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

// Registration code list removed

// Render users table
function renderUsersTable(users) {
    const tbody = document.getElementById('usersTableBody');
    if (!tbody) return;
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Tidak ada data user</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
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
                    <button type="button" class="btn btn-outline-secondary btn-sm" 
                            onclick="showEditUserModal(${user.user_id})" 
                            title="Edit User">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button type="button" class="btn btn-outline-primary btn-sm" 
                            onclick="resetUserPassword(${user.user_id}, '${user.username}')" 
                            title="Reset Password">
                        <i class="fas fa-key"></i>
                    </button>
                    ${(user.user_id !== getCurrentUserId() && user.role !== 'admin') ? `
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

// Registration code table removed

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

// Registration code deletion removed

// Registration code generation removed

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

// Registration codes housekeeping removed

// Export functions for global access
window.initializeAdmin = initializeAdmin;
window.refreshUsersList = refreshUsersList;
window.resetUserPassword = resetUserPassword;
window.deleteUser = deleteUser;
window.showCreateUserModal = showCreateUserModal;
window.showEditUserModal = showEditUserModal;
window.submitUserForm = submitUserForm;

// Show create user modal
function showCreateUserModal() {
    const modalEl = document.getElementById('userModal');
    if (!modalEl) return;
    document.getElementById('userModalLabel').innerText = 'Buat Akun';
    document.getElementById('userId').value = '';
    document.getElementById('username').value = '';
    document.getElementById('fullName').value = '';
    document.getElementById('email').value = '';
    document.getElementById('role').value = 'user';
    document.getElementById('password').value = '';
    document.getElementById('passwordGroup').style.display = '';
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

// Show edit user modal
function showEditUserModal(userId) {
    const user = currentUsers.find(u => u.user_id === userId);
    if (!user) return;
    const modalEl = document.getElementById('userModal');
    if (!modalEl) return;
    document.getElementById('userModalLabel').innerText = 'Edit Akun';
    document.getElementById('userId').value = user.user_id;
    document.getElementById('username').value = user.username; // disabled for edit
    document.getElementById('username').setAttribute('disabled', 'disabled');
    document.getElementById('fullName').value = user.full_name;
    document.getElementById('email').value = user.email;
    document.getElementById('role').value = user.role;
    // Lock role selector if user is admin
    const roleSelect = document.getElementById('role');
    if (roleSelect) {
        if (user.role === 'admin') {
            roleSelect.setAttribute('disabled', 'disabled');
        } else {
            roleSelect.removeAttribute('disabled');
        }
    }
    document.getElementById('password').value = '';
    document.getElementById('passwordGroup').style.display = '';
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

// Submit create/update user
async function submitUserForm() {
    const userId = document.getElementById('userId').value;
    const payload = {
        username: document.getElementById('username').value.trim(),
        full_name: document.getElementById('fullName').value.trim(),
        email: document.getElementById('email').value.trim(),
        role: document.getElementById('role').value,
        password: document.getElementById('password').value
    };
    
    if (!payload.full_name || !payload.email || (!userId && (!payload.username || !payload.password))) {
        showNotification('Lengkapi data yang wajib diisi', 'error');
        return;
    }
    
    try {
        const url = userId ? `/admin/users/${userId}/update` : '/admin/users/create';
        // For update, do not send username if unchanged
        if (userId) delete payload.username;
        // Exclude empty password on update
        if (userId && !payload.password) delete payload.password;
        // Prevent attempting to create admin via UI
        if (!userId && payload.role === 'admin') {
            showNotification('Pembuatan role admin hanya boleh manual di database', 'error');
            return;
        }
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (data.success) {
            showNotification(data.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('userModal')).hide();
            // Reset username disabled state
            document.getElementById('username').removeAttribute('disabled');
            loadUsersList();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (e) {
        console.error('Error submitting user form:', e);
        showNotification('Gagal menyimpan data user', 'error');
    }
}

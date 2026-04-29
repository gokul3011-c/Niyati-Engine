// Global variables
let uploadedFiles = [];
let pieChart = null;
let barChart = null;
let currentResults = null;
let currentUserId = null;
let currentUsername = null;
let screeningHistory = [];
let selectedScreenings = new Set();

// API Base URL - automatically detects local or production
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : '';

// Check authentication on load
window.addEventListener('DOMContentLoaded', () => {
    currentUserId = localStorage.getItem('user_id');
    currentUsername = localStorage.getItem('username');
    
    if (!currentUserId) {
        // Redirect to login if not authenticated
        window.location.href = 'auth.html';
        return;
    }
    
    // Show user info
    const userSection = document.getElementById('userSection');
    const welcomeUser = document.getElementById('welcomeUser');
    if (userSection && welcomeUser) {
        welcomeUser.textContent = currentUsername;
        userSection.style.display = 'flex';
    }
    
    // Load profile data
    loadUserProfile();
});

// Profile Popup Functionality
const userProfile = document.querySelector('.user-profile');
const profileModal = document.getElementById('profileModal');
const profileOverlay = document.getElementById('profileOverlay');
const closeProfile = document.getElementById('closeProfile');
const editProfileBtn = document.getElementById('editProfileBtn');
const cancelEdit = document.getElementById('cancelEdit');
const saveProfile = document.getElementById('saveProfile');
const profileViewMode = document.getElementById('profileViewMode');
const profileEditMode = document.getElementById('profileEditMode');

// Open profile modal
if (userProfile) {
    userProfile.addEventListener('click', () => {
        profileModal.classList.add('active');
        profileOverlay.style.display = 'block';
        // Always show view mode when opening
        showViewMode();
    });
}

// Close profile modal
function closeProfileModal() {
    profileModal.classList.remove('active');
    profileOverlay.style.display = 'none';
    showViewMode(); // Reset to view mode
}

if (closeProfile) {
    closeProfile.addEventListener('click', closeProfileModal);
}

if (profileOverlay) {
    profileOverlay.addEventListener('click', closeProfileModal);
}

// Edit profile button
if (editProfileBtn) {
    editProfileBtn.addEventListener('click', () => {
        showEditMode();
    });
}

// Cancel edit
if (cancelEdit) {
    cancelEdit.addEventListener('click', () => {
        showViewMode();
    });
}

// Save profile
if (saveProfile) {
    saveProfile.addEventListener('click', async () => {
        const newName = document.getElementById('editName').value.trim();
        const newCompany = document.getElementById('editCompany').value.trim();
        const newEmail = document.getElementById('editEmail').value.trim();

        if (!newName) {
            showNotification('Name is required', 'warning');
            return;
        }

        // Validate email format if provided
        if (newEmail && !isValidEmail(newEmail)) {
            showNotification('Please enter a valid email address', 'warning');
            return;
        }

        saveProfile.disabled = true;
        saveProfile.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

        try {
            const response = await fetch(`${API_BASE_URL}/api/user/${currentUserId}/profile`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: newName,
                    company: newCompany,
                    email: newEmail
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Update localStorage
                localStorage.setItem('username', data.username);
                localStorage.setItem('company', data.company || '');
                localStorage.setItem('email', data.email || '');

                // Update UI
                document.getElementById('profileName').textContent = data.username;
                document.getElementById('profileCompany').textContent = data.company || 'Not specified';
                document.getElementById('profileEmail').textContent = data.email || 'Not specified';
                
                // Update welcome user text
                const welcomeUser = document.getElementById('welcomeUser');
                if (welcomeUser) {
                    welcomeUser.textContent = data.username;
                }

                showNotification('Profile updated successfully!', 'success');
                showViewMode();
            } else {
                showNotification(data.error || 'Failed to update profile', 'error');
            }
        } catch (error) {
            console.error('Error updating profile:', error);
            showNotification('Failed to update profile', 'error');
        } finally {
            saveProfile.disabled = false;
            saveProfile.innerHTML = '<i class="fas fa-save"></i> Save Changes';
        }
    });
}

// Show view mode
function showViewMode() {
    profileViewMode.style.display = 'block';
    profileEditMode.style.display = 'none';
    if (editProfileBtn) {
        editProfileBtn.style.display = 'flex';
    }
}

// Show edit mode
function showEditMode() {
    profileViewMode.style.display = 'none';
    profileEditMode.style.display = 'block';
    if (editProfileBtn) {
        editProfileBtn.style.display = 'none';
    }

    // Populate form with current data
    document.getElementById('editName').value = localStorage.getItem('username') || '';
    document.getElementById('editCompany').value = localStorage.getItem('company') || '';
    document.getElementById('editEmail').value = localStorage.getItem('email') || '';
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Load user profile data
async function loadUserProfile() {
    try {
        // Try to get from localStorage first
        const storedName = localStorage.getItem('username');
        const storedCompany = localStorage.getItem('company');
        const storedEmail = localStorage.getItem('email');
        
        // Update profile modal with stored data
        if (storedName) document.getElementById('profileName').textContent = storedName;
        if (storedCompany) document.getElementById('profileCompany').textContent = storedCompany || 'Not specified';
        if (storedEmail) document.getElementById('profileEmail').textContent = storedEmail || 'Not specified';
        
        // Fetch fresh data from API
        const response = await fetch(`${API_BASE_URL}/api/user/${currentUserId}/profile`);
        
        if (response.ok) {
            const data = await response.json();
            
            // Update localStorage with fresh data
            localStorage.setItem('username', data.username);
            localStorage.setItem('company', data.company || '');
            localStorage.setItem('email', data.email || '');
            
            // Update profile modal
            document.getElementById('profileName').textContent = data.username;
            document.getElementById('profileCompany').textContent = data.company;
            document.getElementById('profileEmail').textContent = data.email;
            
            // Update welcome user text
            const welcomeUser = document.getElementById('welcomeUser');
            if (welcomeUser) {
                welcomeUser.textContent = data.username;
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        // Use localStorage data as fallback (already set above)
    }
}

// Settings Panel Functionality
const settingsBtn = document.getElementById('settingsBtn');
const settingsPanel = document.getElementById('settingsPanel');
const settingsOverlay = document.getElementById('settingsOverlay');
const closeSettings = document.getElementById('closeSettings');
const deleteScreeningsBtn = document.getElementById('deleteScreeningsBtn');
const deleteMode = document.getElementById('deleteMode');
const cancelDelete = document.getElementById('cancelDelete');
const confirmDelete = document.getElementById('confirmDelete');
const logoutSettingsBtn = document.getElementById('logoutSettingsBtn');
const refreshBtn = document.getElementById('refreshBtn');

// Refresh button
if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
        location.reload();
    });
}

// Open settings panel
if (settingsBtn) {
    settingsBtn.addEventListener('click', () => {
        settingsPanel.classList.add('active');
        settingsOverlay.style.display = 'block';
        loadScreeningHistory();
    });
}

// Close settings panel
function closeSettingsPanel() {
    settingsPanel.classList.remove('active');
    settingsOverlay.style.display = 'none';
    deleteMode.style.display = 'none';
}

if (closeSettings) {
    closeSettings.addEventListener('click', closeSettingsPanel);
}

if (settingsOverlay) {
    settingsOverlay.addEventListener('click', closeSettingsPanel);
}

// Load screening history
async function loadScreeningHistory() {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '<p class="loading-text"><i class="fas fa-spinner fa-spin"></i> Loading history...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/user/${currentUserId}/history`);
        
        if (!response.ok) {
            throw new Error('Failed to load history');
        }
        
        const data = await response.json();
        screeningHistory = data.sessions || [];
        
        if (screeningHistory.length === 0) {
            historyList.innerHTML = '<p class="no-history"><i class="fas fa-inbox"></i><br>No screening history yet</p>';
            return;
        }
        
        historyList.innerHTML = '';
        screeningHistory.forEach((session, index) => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.innerHTML = `
                <div class="history-item-header">
                    <span class="history-item-title">Screening ${index + 1}</span>
                    <span class="history-item-date">${formatDate(session.created_at)}</span>
                </div>
                <div class="history-item-stats">
                    <span class="history-stat total">
                        <i class="fas fa-users"></i> ${session.total_candidates} Total
                    </span>
                    <span class="history-stat accepted">
                        <i class="fas fa-check"></i> ${session.accepted_count} Accepted
                    </span>
                    <span class="history-stat rejected">
                        <i class="fas fa-times"></i> ${session.rejected_count} Rejected
                    </span>
                </div>
            `;
            
            historyItem.addEventListener('click', () => viewScreeningDetails(session.session_id));
            historyList.appendChild(historyItem);
        });
        
    } catch (error) {
        console.error('Error loading history:', error);
        historyList.innerHTML = '<p class="no-history"><i class="fas fa-exclamation-triangle"></i><br>Failed to load history</p>';
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (hours < 1) {
        return 'Just now';
    } else if (hours < 24) {
        return `${hours}h ago`;
    } else if (days < 7) {
        return `${days}d ago`;
    } else {
        return date.toLocaleDateString();
    }
}

// View screening details
async function viewScreeningDetails(sessionId) {
    try {
        console.log('Loading session:', sessionId);
        
        const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}`);
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            throw new Error(errorData.error || 'Failed to load session details');
        }
        
        const session = await response.json();
        
        console.log('Session data:', session);
        console.log('Candidates count:', session.candidates ? session.candidates.length : 0);
        
        if (!session.candidates || session.candidates.length === 0) {
            console.warn('No candidates found for this session');
        }
        
        // Close settings panel
        closeSettingsPanel();
        
        // Filter candidates by status
        const acceptedCandidates = session.candidates ? session.candidates.filter(c => c.status === 'accepted') : [];
        const rejectedCandidates = session.candidates ? session.candidates.filter(c => c.status === 'rejected') : [];
        
        console.log('Accepted:', acceptedCandidates.length, 'Rejected:', rejectedCandidates.length);
        
        // Display the results
        currentResults = session;
        displayResults({
            total: session.total_candidates || session.candidates.length,
            accepted: session.accepted_count || acceptedCandidates.length,
            rejected: session.rejected_count || rejectedCandidates.length,
            accepted_candidates: acceptedCandidates,
            rejected_candidates: rejectedCandidates,
            all_candidates: session.candidates || []
        });
        
        showNotification('Screening history loaded!', 'success');
        
    } catch (error) {
        console.error('Error loading session:', error);
        showNotification(`Failed to load screening: ${error.message}`, 'error');
    }
}

// Delete screenings mode
if (deleteScreeningsBtn) {
    deleteScreeningsBtn.addEventListener('click', () => {
        deleteMode.style.display = 'block';
        loadDeleteList();
    });
}

// Load delete list
function loadDeleteList() {
    const deleteList = document.getElementById('deleteList');
    selectedScreenings.clear();
    
    if (screeningHistory.length === 0) {
        deleteList.innerHTML = '<p class="no-history">No screenings to delete</p>';
        return;
    }
    
    deleteList.innerHTML = '';
    screeningHistory.forEach((session, index) => {
        const deleteItem = document.createElement('div');
        deleteItem.className = 'delete-item';
        deleteItem.innerHTML = `
            <input type="checkbox" id="delete-${session.session_id}" data-id="${session.session_id}">
            <label for="delete-${session.session_id}" class="delete-item-info">
                <div class="delete-item-title">Screening ${index + 1}</div>
                <div class="delete-item-date">${formatDate(session.created_at)} - ${session.total_candidates} candidates</div>
            </label>
        `;
        
        const checkbox = deleteItem.querySelector('input[type="checkbox"]');
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                selectedScreenings.add(session.session_id);
                deleteItem.classList.add('selected');
            } else {
                selectedScreenings.delete(session.session_id);
                deleteItem.classList.remove('selected');
            }
            confirmDelete.disabled = selectedScreenings.size === 0;
        });
        
        deleteItem.addEventListener('click', (e) => {
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event('change'));
            }
        });
        
        deleteList.appendChild(deleteItem);
    });
    
    confirmDelete.disabled = true;
}

// Cancel delete
if (cancelDelete) {
    cancelDelete.addEventListener('click', () => {
        deleteMode.style.display = 'none';
        selectedScreenings.clear();
    });
}

// Confirm delete
if (confirmDelete) {
    confirmDelete.addEventListener('click', async () => {
        if (selectedScreenings.size === 0) return;
        
        if (!confirm(`Are you sure you want to delete ${selectedScreenings.size} screening(s)?`)) {
            return;
        }
        
        try {
            // Note: You'll need to add a delete endpoint to your API
            const response = await fetch(`${API_BASE_URL}/api/screenings/delete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: currentUserId,
                    session_ids: Array.from(selectedScreenings)
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to delete screenings');
            }
            
            showNotification(`${selectedScreenings.size} screening(s) deleted!`, 'success');
            deleteMode.style.display = 'none';
            selectedScreenings.clear();
            
            // Reload history
            loadScreeningHistory();
            
        } catch (error) {
            console.error('Error deleting screenings:', error);
            showNotification('Failed to delete screenings', 'error');
        }
    });
}

// Logout from settings
if (logoutSettingsBtn) {
    logoutSettingsBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('user_id');
            localStorage.removeItem('username');
            localStorage.removeItem('company');
            localStorage.removeItem('email');
            window.location.href = 'auth.html';
        }
    });
}

// DOM Elements
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const jobDescription = document.getElementById('jobDescription');
const cutoffSlider = document.getElementById('cutoffSlider');
const cutoffValue = document.getElementById('cutoffValue');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsPanel = document.getElementById('resultsPanel');
const loadingOverlay = document.getElementById('loadingOverlay');
const downloadBtn = document.getElementById('downloadBtn');

// File Upload Handling
uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--primary)';
    uploadZone.style.background = 'rgba(0, 255, 213, 0.05)';
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.style.borderColor = 'var(--border)';
    uploadZone.style.background = 'transparent';
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--border)';
    uploadZone.style.background = 'transparent';
    
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
});

fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    addFiles(files);
});

function addFiles(files) {
    files.forEach(file => {
        if (!uploadedFiles.find(f => f.name === file.name)) {
            uploadedFiles.push(file);
        }
    });
    displayFiles();
}

function displayFiles() {
    fileList.innerHTML = '';
    uploadedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <i class="fas fa-file"></i>
            <span>${file.name}</span>
            <i class="fas fa-times remove-file" data-index="${index}"></i>
        `;
        fileList.appendChild(fileItem);
    });
    
    // Add remove event listeners
    document.querySelectorAll('.remove-file').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const index = parseInt(e.target.dataset.index);
            uploadedFiles.splice(index, 1);
            displayFiles();
        });
    });
}

// Cutoff Slider
cutoffSlider.addEventListener('input', (e) => {
    cutoffValue.textContent = e.target.value;
});

// Tab Switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        
        btn.classList.add('active');
        const tab = btn.dataset.tab;
        document.getElementById(`${tab}Pane`).classList.add('active');
    });
});

// Analyze Button
analyzeBtn.addEventListener('click', async () => {
    // Validation
    if (uploadedFiles.length === 0) {
        showNotification('Please upload at least one resume', 'warning');
        return;
    }
    
    if (!jobDescription.value.trim()) {
        showNotification('Please enter a job description', 'warning');
        return;
    }
    
    // Show loading
    loadingOverlay.style.display = 'flex';
    analyzeBtn.disabled = true;
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('user_id', currentUserId); // 🔥 Add user_id
        formData.append('job_description', jobDescription.value);
        
        formData.append('cutoff', cutoffSlider.value);
        
        uploadedFiles.forEach(file => {
            formData.append('resumes', file);
        });
        
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }
        
        const data = await response.json();
        currentResults = data;
        
        // Display results
        displayResults(data);
        
        showNotification('Analysis completed successfully!', 'success');
    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'error');
    } finally {
        loadingOverlay.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});

// Display Results
function displayResults(data) {
    resultsPanel.style.display = 'block';
    
    // Update stats
    document.getElementById('totalCount').textContent = data.total;
    document.getElementById('acceptedCount').textContent = data.accepted;
    document.getElementById('rejectedCount').textContent = data.rejected;
    document.getElementById('acceptedTabCount').textContent = data.accepted;
    document.getElementById('rejectedTabCount').textContent = data.rejected;
    
    // Display candidates
    displayCandidates(data.accepted_candidates, 'acceptedList', true);
    displayCandidates(data.rejected_candidates, 'rejectedList', false);
    
    // Create charts
    createCharts(data);
    
    // Scroll to results
    resultsPanel.scrollIntoView({ behavior: 'smooth' });
}

function displayCandidates(candidates, containerId, isAccepted) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (candidates.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: 40px;">No candidates in this category</p>';
        return;
    }
    
    candidates.forEach((candidate, index) => {
        const card = createCandidateCard(candidate, index + 1, isAccepted);
        container.appendChild(card);
    });
}

function createCandidateCard(candidate, rank, isAccepted) {
    const card = document.createElement('div');
    card.className = 'candidate-card';
    
    if (rank === 1 && isAccepted) {
        card.classList.add('top-match');
    }
    
    // Handle both API response formats (analyze endpoint vs session endpoint)
    const candidateName = candidate['Candidate Name'] || candidate.name || 'Unknown';
    const predictedRole = candidate['Predicted Role'] || candidate.role || 'N/A';
    
    // Fix: Properly handle 0 values and undefined
    const finalScore = candidate['Final Score %'] !== undefined ? candidate['Final Score %'] : (candidate.final_score || 0);
    const similarity = candidate['Similarity %'] !== undefined ? candidate['Similarity %'] : (candidate.similarity || 0);
    const skillMatch = candidate['Skill Match %'] !== undefined ? candidate['Skill Match %'] : (candidate.skill_match || 0);
    const experience = candidate['Experience %'] !== undefined ? candidate['Experience %'] : (candidate.experience || 0);
    
    const matchedSkills = candidate['Matched Skills'] || candidate.matched_skills || [];
    const missingSkills = candidate['Missing Skills'] || candidate.missing_skills || [];
    
    let scoreColor = 'success';
    if (finalScore < 50) scoreColor = 'danger';
    else if (finalScore < 70) scoreColor = 'warning';
    
    card.innerHTML = `
        <div class="candidate-header">
            <div class="candidate-info">
                ${isAccepted && rank === 1 ? '<span class="rank">#1</span>' : ''}
                <h3>${candidateName}</h3>
                <p class="role"><i class="fas fa-briefcase"></i> ${predictedRole}</p>
            </div>
            ${rank === 1 && isAccepted ? '<div class="top-badge"><i class="fas fa-trophy"></i> Top Match</div>' : ''}
        </div>
        
        <div class="final-score-display">
            <div class="final-score-label">Final Score</div>
            <div class="final-score-value ${scoreColor}">${finalScore}%</div>
            <div class="final-score-bar">
                <div class="final-score-bar-fill" style="width: ${finalScore}%"></div>
            </div>
        </div>
        
        <div class="candidate-scores">
            <div class="score-item">
                <div class="label">Similarity</div>
                <div class="value">${similarity}%</div>
            </div>
            <div class="score-item">
                <div class="label">Experience</div>
                <div class="value">${experience > 0 ? experience + '%' : 'N/A'}</div>
            </div>
            <div class="score-item">
                <div class="label">Skill Match</div>
                <div class="value">${skillMatch}%</div>
            </div>
        </div>
        
        <div class="skills-section">
            <div class="skill-group matched">
                <h4><i class="fas fa-check-circle"></i> Matched Skills</h4>
                <div class="skill-tags">
                    ${matchedSkills.map(skill => `<span class="skill-tag matched">${skill}</span>`).join('')}
                </div>
            </div>
            <div class="skill-group missing">
                <h4><i class="fas fa-times-circle"></i> Missing Skills</h4>
                <div class="skill-tags">
                    ${missingSkills.map(skill => `<span class="skill-tag missing">${skill}</span>`).join('')}
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Create Charts
function createCharts(data) {
    // Destroy existing charts
    if (pieChart) pieChart.destroy();
    if (barChart) barChart.destroy();
    
    // Pie Chart
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    pieChart = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: ['Accepted', 'Rejected'],
            datasets: [{
                data: [data.accepted, data.rejected],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        font: { size: 14 }
                    }
                },
                title: {
                    display: true,
                    text: 'Selection Distribution',
                    color: '#ffffff',
                    font: { size: 16, weight: 'bold' }
                }
            }
        }
    });
    
    // Bar Chart
    const allCandidates = data.all_candidates.slice(0, 10); // Top 10
    const barCtx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: allCandidates.map(c => c['Candidate Name']),
            datasets: [{
                label: 'Final Score %',
                data: allCandidates.map(c => c['Final Score %']),
                backgroundColor: allCandidates.map(c => {
                    return c['Final Score %'] >= parseFloat(cutoffSlider.value) 
                        ? 'rgba(16, 185, 129, 0.8)' 
                        : 'rgba(239, 68, 68, 0.8)';
                }),
                borderColor: allCandidates.map(c => {
                    return c['Final Score %'] >= parseFloat(cutoffSlider.value) 
                        ? 'rgba(16, 185, 129, 1)' 
                        : 'rgba(239, 68, 68, 1)';
                }),
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Top 10 Candidates Score',
                    color: '#ffffff',
                    font: { size: 16, weight: 'bold' }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Download Button
downloadBtn.addEventListener('click', async () => {
    if (!currentResults) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ results: currentResults.all_candidates })
        });
        
        if (!response.ok) throw new Error('Download failed');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'niyati_results.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showNotification('Results downloaded successfully!', 'success');
    } catch (error) {
        console.error('Error:', error);
        showNotification('Download failed', 'error');
    }
});

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? 'rgba(16, 185, 129, 0.9)' : type === 'error' ? 'rgba(239, 68, 68, 0.9)' : 'rgba(245, 158, 11, 0.9)'};
        color: white;
        border-radius: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

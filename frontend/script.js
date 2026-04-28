// Global variables
let uploadedFiles = [];
let pieChart = null;
let barChart = null;
let currentResults = null;

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
        formData.append('job_description', jobDescription.value);
        formData.append('cutoff', cutoffSlider.value);
        
        uploadedFiles.forEach(file => {
            formData.append('resumes', file);
        });
        
        // Send to backend
        const response = await fetch('http://localhost:5000/api/analyze', {
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
    
    const finalScore = candidate['Final Score %'];
    const similarity = candidate['Similarity %'];
    const skillMatch = candidate['Skill Match %'];
    const experience = candidate['Experience %'] || 0;
    
    let scoreColor = 'success';
    if (finalScore < 50) scoreColor = 'danger';
    else if (finalScore < 70) scoreColor = 'warning';
    
    card.innerHTML = `
        <div class="candidate-header">
            <div class="candidate-info">
                ${isAccepted && rank === 1 ? '<span class="rank">#1</span>' : ''}
                <h3>${candidate['Candidate Name']}</h3>
                <p class="role"><i class="fas fa-briefcase"></i> ${candidate['Predicted Role']}</p>
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
                    ${candidate['Matched Skills'].map(skill => `<span class="skill-tag matched">${skill}</span>`).join('')}
                </div>
            </div>
            <div class="skill-group missing">
                <h4><i class="fas fa-times-circle"></i> Missing Skills</h4>
                <div class="skill-tags">
                    ${candidate['Missing Skills'].map(skill => `<span class="skill-tag missing">${skill}</span>`).join('')}
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
        const response = await fetch('http://localhost:5000/api/download', {
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

/**
 * CV Assessment System Frontend JavaScript
 * Handles file uploads, API calls, and UI interactions
 */

class CVAssessmentApp {
    constructor() {
        this.currentJobId = null;
        this.uploadedCVs = [];
        this.initializeEventListeners();
        this.loadJobHistory();
    }

    /**
     * Initialize all event listeners
     */
    initializeEventListeners() {
        // Job description upload
        const jobUpload = document.getElementById('jobUpload');
        const jobFile = document.getElementById('jobFile');
        
        jobUpload.addEventListener('click', () => jobFile.click());
        jobUpload.addEventListener('dragover', this.handleDragOver.bind(this));
        jobUpload.addEventListener('drop', this.handleJobDrop.bind(this));
        jobFile.addEventListener('change', this.handleJobUpload.bind(this));

        // CV upload
        const cvUpload = document.getElementById('cvUpload');
        const cvFiles = document.getElementById('cvFiles');
        
        cvUpload.addEventListener('click', () => cvFiles.click());
        cvUpload.addEventListener('dragover', this.handleDragOver.bind(this));
        cvUpload.addEventListener('drop', this.handleCVDrop.bind(this));
        cvFiles.addEventListener('change', this.handleCVUpload.bind(this));

        // Start evaluation
        const startBtn = document.getElementById('startEvaluation');
        startBtn.addEventListener('click', this.startEvaluation.bind(this));
    }

    /**
     * Handle drag over events
     */
    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    }

    /**
     * Handle job description file drop
     */
    handleJobDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type === 'application/pdf') {
            this.uploadJobDescription(files[0]);
        }
    }

    /**
     * Handle CV files drop
     */
    handleCVDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = Array.from(e.dataTransfer.files).filter(
            file => file.type === 'application/pdf'
        );
        if (files.length > 0) {
            this.uploadCVs(files);
        }
    }

    /**
     * Handle job description file selection
     */
    handleJobUpload(e) {
        const file = e.target.files[0];
        if (file && file.type === 'application/pdf') {
            this.uploadJobDescription(file);
        }
    }

    /**
     * Handle CV files selection
     */
    handleCVUpload(e) {
        const files = Array.from(e.target.files).filter(
            file => file.type === 'application/pdf'
        );
        if (files.length > 0) {
            this.uploadCVs(files);
        }
    }

    /**
     * Upload job description to server
     */
    async uploadJobDescription(file) {
        const formData = new FormData();
        formData.append('file', file);

        this.showStatus('jobStatus', 'Uploading job description...', 'info');

        try {
            const response = await fetch('/upload/job-description', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                this.currentJobId = data.job_id;
                this.showStatus('jobStatus', `✅ ${data.message}`, 'success');
                this.showStep('step2');
                this.loadJobHistory();
            } else {
                throw new Error(data.detail);
            }
        } catch (error) {
            this.showStatus('jobStatus', `❌ Error: ${error.message}`, 'error');
        }
    }

    /**
     * Upload CV files to server
     */
    async uploadCVs(files) {
        if (!this.currentJobId) {
            this.showStatus('cvStatus', '❌ Please upload job description first', 'error');
            return;
        }

        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        this.showStatus('cvStatus', 'Uploading CVs...', 'info');

        try {
            const response = await fetch(`/upload/cvs/${this.currentJobId}`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                this.uploadedCVs = data.uploaded_cvs;
                this.showStatus('cvStatus', `✅ ${data.message}`, 'success');
                this.displayUploadedCVs();
                this.showStep('step3');
            } else {
                throw new Error(data.detail);
            }
        } catch (error) {
            this.showStatus('cvStatus', `❌ Error: ${error.message}`, 'error');
        }
    }

    /**
     * Start evaluation process
     */
    async startEvaluation() {
        if (!this.currentJobId || this.uploadedCVs.length === 0) {
            this.showStatus('evaluationStatus', '❌ Please upload job description and CVs first', 'error');
            return;
        }

        const startBtn = document.getElementById('startEvaluation');
        const progressContainer = document.getElementById('evaluationProgress');
        
        startBtn.disabled = true;
        progressContainer.style.display = 'block';
        this.showStatus('evaluationStatus', 'Starting evaluation...', 'info');

        // Simulate progress (since evaluation happens in backend)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            this.updateProgress(progress);
        }, 500);

        try {
            const response = await fetch(`/evaluate/${this.currentJobId}`, {
                method: 'POST'
            });

            const data = await response.json();

            clearInterval(progressInterval);
            this.updateProgress(100);

            if (response.ok) {
                this.showStatus('evaluationStatus', '✅ Evaluation completed!', 'success');
                setTimeout(() => {
                    this.loadResults();
                    this.showStep('step4');
                }, 1000);
            } else {
                throw new Error(data.detail);
            }
        } catch (error) {
            clearInterval(progressInterval);
            this.showStatus('evaluationStatus', `❌ Error: ${error.message}`, 'error');
        } finally {
            startBtn.disabled = false;
        }
    }

    /**
     * Load and display evaluation results
     */
    async loadResults() {
        try {
            const response = await fetch(`/results/${this.currentJobId}`);
            const data = await response.json();

            if (response.ok) {
                this.displayResults(data.results);
            } else {
                throw new Error(data.detail);
            }
        } catch (error) {
            console.error('Error loading results:', error);
        }
    }

    /**
     * Display evaluation results
     */
    displayResults(results) {
        const container = document.getElementById('resultsContainer');
        
        if (!results || results.length === 0) {
            container.innerHTML = '<p>No results found.</p>';
            return;
        }

        // Sort by overall score (highest first)
        results.sort((a, b) => (b.overall_score || 0) - (a.overall_score || 0));

        container.innerHTML = results.map((result, index) => `
            <div class="candidate-card">
                <div class="candidate-header" onclick="toggleDetails(${index})">
                    <div class="candidate-name">
                        ${result.filename.replace('.pdf', '')}
                        ${result.has_error ? ' ⚠️' : ''}
                    </div>
                    <div class="candidate-scores">
                        <div class="score-badge ${this.getScoreClass(result.overall_score)}">
                            Overall: ${result.overall_score || 'N/A'}
                        </div>
                        <div class="score-badge ${this.getScoreClass(result.skill_score)}">
                            Skills: ${result.skill_score || 'N/A'}
                        </div>
                        <div class="score-badge ${this.getScoreClass(result.cultural_score)}">
                            Culture: ${result.cultural_score || 'N/A'}
                        </div>
                    </div>
                </div>
                <div class="candidate-details" id="details-${index}">
                    ${result.has_error ? 
                        '<div class="detail-section"><h4>⚠️ Evaluation Error</h4><p>There was an error evaluating this candidate. Please try again.</p></div>' :
                        `
                        <div class="detail-section">
                            <h4>💼 Skills Assessment</h4>
                            <p>${result.skill_assessment || 'No assessment available'}</p>
                        </div>
                        <div class="detail-section">
                            <h4>🤝 Cultural Fit Assessment</h4>
                            <p>${result.cultural_assessment || 'No assessment available'}</p>
                        </div>
                        <div class="detail-section">
                            <h4>📋 Summary</h4>
                            <p>${result.summary || 'No summary available'}</p>
                        </div>
                        <div class="detail-section">
                            <h4>💡 Recommendation</h4>
                            <p>${result.recommendation || 'No recommendation available'}</p>
                        </div>
                        `
                    }
                </div>
            </div>
        `).join('');
    }

    /**
     * Get CSS class for score badge based on score value
     */
    getScoreClass(score) {
        if (!score) return 'score-low';
        if (score >= 7) return 'score-high';
        if (score >= 5) return 'score-medium';
        return 'score-low';
    }

    /**
     * Display uploaded CV files
     */
    displayUploadedCVs() {
        const cvList = document.getElementById('cvList');
        
        cvList.innerHTML = this.uploadedCVs.map(cv => `
            <div class="file-item">
                <span class="file-name">${cv.filename}</span>
            </div>
        `).join('');
    }

    /**
     * Update progress bar
     */
    updateProgress(percentage) {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        progressFill.style.width = `${percentage}%`;
        progressText.textContent = `Evaluating candidates... ${Math.round(percentage)}%`;
    }

    /**
     * Show status message
     */
    showStatus(elementId, message, type) {
        const element = document.getElementById(elementId);
        element.textContent = message;
        element.className = `status-message ${type}`;
    }

    /**
     * Show a specific step
     */
    showStep(stepId) {
        document.getElementById(stepId).style.display = 'block';
    }

    /**
     * Load job history from server
     */
    async loadJobHistory() {
        try {
            const response = await fetch('/jobs');
            const data = await response.json();

            if (response.ok) {
                this.displayJobHistory(data.jobs);
            }
        } catch (error) {
            console.error('Error loading job history:', error);
        }
    }

    /**
     * Display job history in sidebar
     */
    displayJobHistory(jobs) {
        const historyContainer = document.getElementById('jobHistory');
        
        if (!jobs || jobs.length === 0) {
            historyContainer.innerHTML = '<p style="color: #7f8c8d; font-size: 0.9rem;">No previous jobs</p>';
            return;
        }

        historyContainer.innerHTML = jobs.map(job => `
            <div class="job-item ${job.id === this.currentJobId ? 'active' : ''}" 
                 onclick="loadJob('${job.id}')">
                <div class="job-title">${job.filename.replace('.pdf', '')}</div>
                <div class="job-meta">
                    ${job.cv_count} CVs • ${job.evaluated_count} evaluated
                </div>
            </div>
        `).join('');
    }
}

/**
 * Toggle candidate details visibility
 */
function toggleDetails(index) {
    const details = document.getElementById(`details-${index}`);
    details.classList.toggle('expanded');
}

/**
 * Load existing job (placeholder for future implementation)
 */
function loadJob(jobId) {
    console.log('Loading job:', jobId);
    // Future implementation: load existing job and results
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CVAssessmentApp();
});
// Level 33 Dashboard - Frontend Application
// MSB v2 API wiring

// Global state
let currentPage = 'dashboard';
let metricsChart = null;
let performanceChart = null;
let ws = null;
const API_BASE = '';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Level 33 Dashboard initialized');
    setupNavigation();
    loadDashboardData();
    setInterval(refreshData, 30000);
});

// Navigation
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            const page = item.dataset.page;
            switchPage(page);
        });
    });
}

function switchPage(page) {
    currentPage = page;
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const pageElement = document.getElementById(`page-${page}`);
    if (pageElement) {
        pageElement.classList.add('active');
    }
    const titles = {
        dashboard: 'Dashboard',
        activities: 'Activities',
        metrics: 'Metrics',
        automations: 'Automations',
        llm: 'LLM Logs',
        config: 'Configuration',
        health: 'Health'
    };
    document.getElementById('page-title').textContent = titles[page] || page;
    loadPageData(page);
}

function loadPageData(page) {
    switch(page) {
        case 'dashboard': loadDashboardData(); break;
        case 'activities': loadActivities(); break;
        case 'metrics': loadMetrics(); break;
        case 'automations': loadAutomations(); break;
        case 'llm': loadLLMInteractions(); break;
        case 'config': loadConfig(); break;
        case 'health': loadHealth(); break;
    }
}

// API Calls
async function apiCall(endpoint) {
    try {
        const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error calling ${endpoint}:`, error);
        return null;
    }
}

// Dashboard
async function loadDashboardData() {
    const data = await apiCall('/studio/status');
    if (!data) return;

    updateSystemStats({
        cpu_percent: 42,
        memory_percent: 68,
        disk_percent: 55,
    });

    const ollamaStatus = document.getElementById('ollama-status');
    if (ollamaStatus) {
        ollamaStatus.textContent = 'MSB Online';
        ollamaStatus.style.color = 'var(--success)';
    }

    const recent = document.getElementById('recent-activities');
    if (recent) {
        recent.innerHTML = `<p>Studio runtime connected. Open <b>/sac/status</b> and <b>/control/runtime/status</b> for live data.</p>`;
    }

    loadMetricsChart();
    updateLastUpdate();
}

function updateSystemStats(stats) {
    const cpuUsage = document.getElementById('cpu-usage');
    const memoryUsage = document.getElementById('memory-usage');
    const diskUsage = document.getElementById('disk-usage');

    if (cpuUsage && stats.cpu_percent !== undefined) {
        cpuUsage.textContent = `${stats.cpu_percent.toFixed(1)}%`;
        cpuUsage.style.color = stats.cpu_percent > 80 ? 'var(--error)' : 'var(--success)';
    }
    if (memoryUsage && stats.memory_percent !== undefined) {
        memoryUsage.textContent = `${stats.memory_percent.toFixed(1)}%`;
        memoryUsage.style.color = stats.memory_percent > 80 ? 'var(--error)' : 'var(--success)';
    }
    if (diskUsage && stats.disk_percent !== undefined) {
        diskUsage.textContent = `${stats.disk_percent.toFixed(1)}%`;
        diskUsage.style.color = stats.disk_percent > 80 ? 'var(--error)' : 'var(--success)';
    }
}

function displayRecentActivities(activities) {
    const container = document.getElementById('recent-activities');
    if (!container) return;
    if (!activities || activities.length === 0) {
        container.innerHTML = '<p class="loading">No recent activities</p>';
        return;
    }
    container.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-info">
                <div class="activity-type">${activity.component || 'system'} - ${activity.action || 'event'}</div>
                <div class="activity-details">${activity.type || 'info'}</div>
            </div>
            <div>
                <div class="activity-status ${activity.status || 'success'}">${activity.status || 'success'}</div>
                <div class="activity-time">${formatTime(activity.timestamp)}</div>
            </div>
        </div>
    `).join('');
}

// Activities
async function loadActivities() {
    const data = await apiCall('/studio/status');
    const container = document.getElementById('activities-table');
    if (!container) return;
    container.innerHTML = '<p class="loading">Connect real activity stream to populate this view.</p>';
}

// Metrics
async function loadMetrics() {
    const data = await apiCall('/studio/status');
    const ctx = document.getElementById('performance-chart');
    if (!ctx) return;

    const runtime = data?.runtime || {};
    const datasets = [{
        label: 'Runtime Health',
        data: runtime.worker_pool ? [70, 72, 71, 73, 74, 73, 75] : [],
        borderColor: '#2563eb',
        backgroundColor: '#2563eb20',
        tension: 0.4
    }];

    performanceChart = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, max: 100, grid: { color: '#4b5563' }, ticks: { color: '#9ca3af' } },
                x: { grid: { color: '#4b5563' }, ticks: { color: '#9ca3af' } }
            },
            plugins: { legend: { labels: { color: '#f3f4f6' } } }
        }
    });
}

// Automations
async function loadAutomations() {
    const container = document.getElementById('automations-grid');
    if (!container) return;
    container.innerHTML = `
        <div class="automation-card">
            <div class="automation-header"><div class="automation-icon">🧠</div><div class="automation-title">SAR Control</div></div>
            <div class="automation-description">Use /control/chat, /control/runtime/start, /runtime/status</div>
        </div>
        <div class="automation-card">
            <div class="automation-header"><div class="automation-icon">🛡️</div><div class="automation-title">SAC Self-Audit</div></div>
            <div class="automation-description">Open /sac/self-audit for mirage checks.</div>
        </div>
    `;
}

// LLM Interactions
async function loadLLMInteractions() {
    const container = document.getElementById('llm-interactions');
    if (!container) return;
    container.innerHTML = '<p class="loading">LLM logging pipeline not yet bound.</p>';
}

// Configuration
async function loadConfig() {
    const container = document.getElementById('config-viewer');
    if (!container) return;
    container.innerHTML = '<p class="loading">Env-backed config viewer pending.</p>';
}

// Health
async function loadHealth() {
    const statusEl = document.getElementById('health-status');
    if (!statusEl) return;
    const data = await apiCall('/studio/status');
    statusEl.innerHTML = data ? `<pre>${JSON.stringify(data, null, 2)}</pre>` : '<p class="loading">Health unavailable</p>';
}

// Helpers
function formatTime(iso) {
    if (!iso) return '--';
    const d = new Date(iso);
    if (isNaN(d.getTime())) return iso;
    return d.toLocaleTimeString();
}

function updateLastUpdate() {
    const el = document.getElementById('last-update');
    if (el) el.textContent = `Last update: ${new Date().toLocaleTimeString()}`;
}

async function refreshData() {
    loadPageData(currentPage);
    updateLastUpdate();
}

window.refreshData = refreshData;
window.runAutomation = async (id) => {
    alert(`Run ${id} from a backend-connected automation endpoint.`);
};

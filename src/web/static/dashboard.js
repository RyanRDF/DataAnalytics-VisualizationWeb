// ===== DASHBOARD MODULE =====
// This module handles all Dashboard-related functionality
// Separated from main script.js for easier maintenance and modification

// Dashboard state
const DashboardState = {
    charts: [],
    isInitialized: false,
    chartInstances: {},
    chartPositions: {} // Store chart positions
};

// Chart configuration
const ChartConfig = {
    minWidth: 300,
    minHeight: 250,
    maxWidth: 1200,
    maxHeight: 600,
    defaultWidth: 500,
    defaultHeight: 350,
    gridSize: 20, // Grid snap size in pixels
    snapEnabled: true // Enable/disable snap to grid
};

// Load saved chart positions from localStorage
function loadChartPositions() {
    try {
        const saved = localStorage.getItem('dashboardChartPositions');
        if (saved) {
            DashboardState.chartPositions = JSON.parse(saved);
        }
    } catch (e) {
        console.warn('Failed to load chart positions:', e);
    }
}

// Save chart positions to localStorage
function saveChartPositions() {
    try {
        localStorage.setItem('dashboardChartPositions', JSON.stringify(DashboardState.chartPositions));
    } catch (e) {
        console.warn('Failed to save chart positions:', e);
    }
}

// Initialize Dashboard
function initDashboard() {
    if (DashboardState.isInitialized) {
        // If already initialized, just ensure charts are visible
        const container = document.getElementById('dashboardChartsContainer');
        if (container) {
            // Resize all charts to ensure proper rendering
            setTimeout(() => {
                Object.values(DashboardState.chartInstances).forEach(chart => {
                    if (chart && typeof chart.resize === 'function') {
                        chart.resize();
                    }
                });
            }, 100);
        }
        return;
    }
    
    const homeContent = document.getElementById('home');
    if (!homeContent) {
        console.error('Dashboard: Home content element not found');
        return;
    }
    
    // Generate Dashboard HTML
    homeContent.innerHTML = generateDashboardHTML();
    
    // Initialize charts after a short delay to ensure DOM is ready
    setTimeout(() => {
        initializeDashboardCharts();
        DashboardState.isInitialized = true;
    }, 150);
}

// Generate Dashboard HTML structure
function generateDashboardHTML() {
    return `
        <!-- Overview Cards -->
        <div class="dashboard-cards-grid">
            <div class="dashboard-card dashboard-card-blue" onclick="showContent('keuangan')">
                <div class="dashboard-card-content">
                    <div class="dashboard-card-text">
                        <p class="dashboard-card-label">B.Clear</p>
                        <h3 class="dashboard-card-title">Financial Data</h3>
                    </div>
                    <div class="dashboard-card-icon">
                        <div class="dashboard-icon-square"></div>
                    </div>
                </div>
                <button class="dashboard-card-button dashboard-button-blue">
                    View Details <i class="fas fa-chevron-right"></i>
                </button>
            </div>

            <div class="dashboard-card dashboard-card-green" onclick="showContent('pasien')">
                <div class="dashboard-card-content">
                    <div class="dashboard-card-text">
                        <p class="dashboard-card-label">Report</p>
                        <h3 class="dashboard-card-title">Patient Data</h3>
                    </div>
                    <div class="dashboard-card-icon">
                        <div class="dashboard-icon-square"></div>
                    </div>
                </div>
                <button class="dashboard-card-button dashboard-button-green">
                    View Details <i class="fas fa-chevron-right"></i>
                </button>
            </div>

            <div class="dashboard-card dashboard-card-orange" onclick="showContent('selisih-tarif')">
                <div class="dashboard-card-content">
                    <div class="dashboard-card-text">
                        <p class="dashboard-card-label">Statistics</p>
                        <h3 class="dashboard-card-title">Site Analysis</h3>
                    </div>
                    <div class="dashboard-card-icon">
                        <div class="dashboard-icon-square"></div>
                    </div>
                </div>
                <button class="dashboard-card-button dashboard-button-orange">
                    View Details <i class="fas fa-chevron-right"></i>
                </button>
            </div>

            <div class="dashboard-card dashboard-card-red" onclick="showFileUpload()">
                <div class="dashboard-card-content">
                    <div class="dashboard-card-text">
                        <p class="dashboard-card-label">Upload</p>
                        <h3 class="dashboard-card-title">File Upload</h3>
                    </div>
                    <div class="dashboard-card-icon">
                        <div class="dashboard-icon-square"></div>
                    </div>
                </div>
                <button class="dashboard-card-button dashboard-button-red">
                    View Details <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>

        <!-- Welcome Section -->
        <div class="dashboard-welcome-card">
            <h2 class="dashboard-welcome-title">Welcome to IHC Data Analytics Dashboard</h2>
            <p class="dashboard-welcome-text">This dashboard provides various data analysis for:</p>
            <div class="dashboard-features-grid">
                <div class="dashboard-feature-item">
                    <span class="dashboard-checkmark">✓</span>
                    <span>Financial and patient data analysis with accurate profit and loss calculation</span>
                </div>
                <div class="dashboard-feature-item">
                    <span class="dashboard-checkmark">✓</span>
                    <span>Patient data management with complete and structured medical information</span>
                </div>
                <div class="dashboard-feature-item">
                    <span class="dashboard-checkmark">✓</span>
                    <span>Rate difference, LOS, and NACCR5 with interactive data visualization</span>
                </div>
                <div class="dashboard-feature-item">
                    <span class="dashboard-checkmark">✓</span>
                    <span>Ventilator usage monitoring with detailed analysis and reports</span>
                </div>
            </div>
            <div class="dashboard-getting-started">
                <span class="dashboard-info-icon">💡</span>
                <strong>Getting Started:</strong> To get started, please upload .txt, .xlsx, or .xls file using the Upload File menu in the sidebar.
            </div>
        </div>

        <!-- Charts Container -->
        <div class="dashboard-charts-container" id="dashboardChartsContainer">
            <!-- Charts will be dynamically added here -->
        </div>
    `;
}

// Initialize Dashboard Charts
function initializeDashboardCharts() {
    const container = document.getElementById('dashboardChartsContainer');
    if (!container) {
        console.error('Dashboard: Charts container not found');
        return;
    }

    // Load saved positions
    loadChartPositions();

    // Clear existing charts
    container.innerHTML = '';
    DashboardState.charts = [];
    DashboardState.chartInstances = {};

    // Ensure container has proper height
    updateContainerHeight();

    // Create chart elements with default positions (snapped to grid)
    const gridSize = ChartConfig.gridSize;
    const charts = [
        { id: 'trendChart', type: 'line', title: 'Trend Analysis', defaultX: 0, defaultY: 0, defaultWidth: 500, defaultHeight: 350 },
        { id: 'distributionChart', type: 'pie', title: 'Data Distribution', defaultX: 520, defaultY: 0, defaultWidth: 500, defaultHeight: 350 },
        { id: 'activityChart', type: 'bar', title: 'Monthly Activity', defaultX: 0, defaultY: 380, defaultWidth: 500, defaultHeight: 350 }
    ];

    charts.forEach((chartConfig, index) => {
        const chartElement = createDraggableChartElement(chartConfig, index);
        container.appendChild(chartElement);
        
        // Apply saved position or use default (snap to grid)
        const savedPos = DashboardState.chartPositions[chartConfig.id];
        if (savedPos) {
            let x = savedPos.x;
            let y = savedPos.y;
            
            // Snap saved positions to grid
            if (ChartConfig.snapEnabled) {
                x = Math.round(x / gridSize) * gridSize;
                y = Math.round(y / gridSize) * gridSize;
            }
            
            chartElement.style.left = x + 'px';
            chartElement.style.top = y + 'px';
            if (savedPos.width) chartElement.style.width = savedPos.width;
            if (savedPos.height) chartElement.style.height = savedPos.height;
        } else {
            // Snap default positions to grid
            let x = chartConfig.defaultX;
            let y = chartConfig.defaultY;
            
            if (ChartConfig.snapEnabled) {
                x = Math.round(x / gridSize) * gridSize;
                y = Math.round(y / gridSize) * gridSize;
            }
            
            chartElement.style.left = x + 'px';
            chartElement.style.top = y + 'px';
            chartElement.style.width = chartConfig.defaultWidth + 'px';
            chartElement.style.height = chartConfig.defaultHeight + 'px';
        }
        
        DashboardState.charts.push({
            id: chartConfig.id,
            type: chartConfig.type,
            element: chartElement,
            index: index
        });
    });

    // Initialize Chart.js instances
    initializeChartInstances();
    
    // Setup drag and resize handlers
    setupChartInteractions();
    
    // Update container height after charts are positioned
    setTimeout(updateContainerHeight, 100);
    
    // Update grid overlay on window resize
    window.addEventListener('resize', () => {
        if (isDragging) {
            updateGridOverlay();
        }
    });
}

// Update container height based on chart positions
function updateContainerHeight() {
    const container = document.getElementById('dashboardChartsContainer');
    if (!container) return;
    
    const charts = container.querySelectorAll('.dashboard-chart-wrapper');
    let maxBottom = 0;
    
    charts.forEach(chart => {
        const rect = chart.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        const relativeTop = parseInt(window.getComputedStyle(chart).top) || 0;
        const height = parseInt(window.getComputedStyle(chart).height) || 350;
        const bottom = relativeTop + height;
        maxBottom = Math.max(maxBottom, bottom);
    });
    
    // Set minimum height and add padding
    container.style.minHeight = Math.max(800, maxBottom + 50) + 'px';
}

// Create draggable chart element
function createDraggableChartElement(config, index) {
    const chartWrapper = document.createElement('div');
    chartWrapper.className = 'dashboard-chart-wrapper dashboard-chart-free';
    chartWrapper.id = `chart-${config.id}`;
    chartWrapper.dataset.chartId = config.id;
    chartWrapper.dataset.chartIndex = index;

    chartWrapper.innerHTML = `
        <div class="dashboard-chart-header">
            <h3 class="dashboard-chart-title">
                <i class="fas fa-grip-vertical" style="margin-right: 8px; opacity: 0.5;"></i>
                ${config.title}
            </h3>
            <div class="dashboard-chart-controls">
                <button class="dashboard-chart-resize-handle" title="Resize">
                    <i class="fas fa-expand-arrows-alt"></i>
                </button>
                <button class="dashboard-chart-close" title="Remove" onclick="removeChart('${config.id}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        <div class="dashboard-chart-body">
            <canvas id="canvas-${config.id}"></canvas>
        </div>
    `;

    return chartWrapper;
}

// Initialize Chart.js instances
function initializeChartInstances() {
    // Wait a bit to ensure DOM is fully ready
    setTimeout(() => {
        // Trend Analysis Line Chart
        const trendCtx = document.getElementById('canvas-trendChart');
        if (trendCtx) {
            const trendData = {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7'],
                datasets: [
                    {
                        label: 'financial',
                        data: [4000, 3000, 2000, 2780, 1890, 2390, 3490],
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'patient',
                        data: [2400, 1398, 9800, 3908, 4800, 3800, 4300],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'site',
                        data: [2400, 2210, 2290, 2000, 2181, 2500, 2100],
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }
                ]
            };

            DashboardState.chartInstances.trendChart = new Chart(trendCtx, {
                type: 'line',
                data: trendData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 15,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 2500
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        }
                    }
                }
            });
        }

        // Data Distribution Pie Chart
        const distributionCtx = document.getElementById('canvas-distributionChart');
        if (distributionCtx) {
            const distributionData = {
                labels: ['Financial Data', 'Patient Data', 'Site Analysis', 'File Upload'],
                datasets: [{
                    data: [400, 300, 300, 200],
                    backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#ef4444']
                }]
            };

            DashboardState.chartInstances.distributionChart = new Chart(distributionCtx, {
                type: 'pie',
                data: distributionData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 15,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(0);
                                    return `${label}: ${percentage}%`;
                                }
                            }
                        }
                    }
                }
            });
        }

        // Monthly Activity Bar Chart
        const activityCtx = document.getElementById('canvas-activityChart');
        if (activityCtx) {
            const activityData = {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [
                    {
                        label: 'uploads',
                        data: [40, 30, 20, 27, 18, 23],
                        backgroundColor: '#2563eb'
                    },
                    {
                        label: 'analysis',
                        data: [24, 13, 28, 39, 48, 38],
                        backgroundColor: '#10b981'
                    }
                ]
            };

            DashboardState.chartInstances.activityChart = new Chart(activityCtx, {
                type: 'bar',
                data: activityData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 15,
                                usePointStyle: true
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 15
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
    }, 200);
}

// Setup chart interactions (drag and resize)
function setupChartInteractions() {
    // Drag functionality - use mouse events for free positioning
    const chartWrappers = document.querySelectorAll('.dashboard-chart-wrapper');
    
    chartWrappers.forEach(wrapper => {
        // Make draggable - use header as drag handle
        const header = wrapper.querySelector('.dashboard-chart-header');
        if (header) {
            header.style.cursor = 'move';
            header.addEventListener('mousedown', (e) => handleFreeDragStart(e, wrapper));
        }

        // Resize functionality
        const resizeHandle = wrapper.querySelector('.dashboard-chart-resize-handle');
        if (resizeHandle) {
            resizeHandle.addEventListener('mousedown', (e) => handleResizeStart(e, wrapper));
        }
    });
}

// Free drag handlers for absolute positioning
let isDragging = false;
let dragElement = null;
let dragOffset = { x: 0, y: 0 };
let dragStartPos = { x: 0, y: 0 };

function handleFreeDragStart(e, element) {
    e.preventDefault();
    e.stopPropagation();
    
    isDragging = true;
    dragElement = element;
    
    // Get current position
    const rect = element.getBoundingClientRect();
    const container = document.getElementById('dashboardChartsContainer');
    const containerRect = container.getBoundingClientRect();
    
    // Calculate offset from mouse to element top-left
    dragOffset.x = e.clientX - rect.left;
    dragOffset.y = e.clientY - rect.top;
    
    // Get current computed position
    const computedStyle = window.getComputedStyle(element);
    dragStartPos.x = parseInt(computedStyle.left) || 0;
    dragStartPos.y = parseInt(computedStyle.top) || 0;
    
    element.classList.add('dragging');
    element.style.zIndex = '1000';
    
    // Show grid overlay if snap is enabled
    if (ChartConfig.snapEnabled) {
        showGridOverlay();
    }
    
    // Add global mouse move and up handlers
    document.addEventListener('mousemove', handleFreeDrag);
    document.addEventListener('mouseup', handleFreeDragEnd);
}

function handleFreeDrag(e) {
    if (!isDragging || !dragElement) return;
    
    e.preventDefault();
    
    const container = document.getElementById('dashboardChartsContainer');
    if (!container) return;
    
    const containerRect = container.getBoundingClientRect();
    
    // Calculate new position relative to container
    let newX = e.clientX - containerRect.left - dragOffset.x;
    let newY = e.clientY - containerRect.top - dragOffset.y;
    
    // Apply snap to grid if enabled
    if (ChartConfig.snapEnabled) {
        newX = Math.round(newX / ChartConfig.gridSize) * ChartConfig.gridSize;
        newY = Math.round(newY / ChartConfig.gridSize) * ChartConfig.gridSize;
    }
    
    // Constrain to container bounds
    const elementRect = dragElement.getBoundingClientRect();
    const elementWidth = parseInt(window.getComputedStyle(dragElement).width) || elementRect.width;
    const elementHeight = parseInt(window.getComputedStyle(dragElement).height) || elementRect.height;
    
    const maxX = containerRect.width - elementWidth;
    const maxY = containerRect.height - elementHeight;
    
    newX = Math.max(0, Math.min(newX, maxX));
    newY = Math.max(0, Math.min(newY, maxY));
    
    // Apply new position
    dragElement.style.left = newX + 'px';
    dragElement.style.top = newY + 'px';
}

function handleFreeDragEnd(e) {
    if (!isDragging || !dragElement) return;
    
    isDragging = false;
    dragElement.classList.remove('dragging');
    dragElement.style.zIndex = '';
    dragElement.style.transform = '';
    
    // Hide grid overlay
    hideGridOverlay();
    
    // Save position (snap to grid one final time)
    const chartId = dragElement.dataset.chartId;
    const computedStyle = window.getComputedStyle(dragElement);
    let finalX = parseInt(computedStyle.left) || 0;
    let finalY = parseInt(computedStyle.top) || 0;
    
    // Final snap to grid
    if (ChartConfig.snapEnabled) {
        finalX = Math.round(finalX / ChartConfig.gridSize) * ChartConfig.gridSize;
        finalY = Math.round(finalY / ChartConfig.gridSize) * ChartConfig.gridSize;
        dragElement.style.left = finalX + 'px';
        dragElement.style.top = finalY + 'px';
    }
    
    DashboardState.chartPositions[chartId] = {
        x: finalX,
        y: finalY,
        width: computedStyle.width,
        height: computedStyle.height
    };
    saveChartPositions();
    
    // Update container height
    updateContainerHeight();
    
    // Resize chart to ensure proper rendering
    setTimeout(() => {
        if (DashboardState.chartInstances[chartId] && typeof DashboardState.chartInstances[chartId].resize === 'function') {
            DashboardState.chartInstances[chartId].resize();
        }
    }, 50);
    
    dragElement = null;
    dragOffset = { x: 0, y: 0 };
    
    // Remove global handlers
    document.removeEventListener('mousemove', handleFreeDrag);
    document.removeEventListener('mouseup', handleFreeDragEnd);
}

// Resize handlers
let isResizing = false;
let resizeElement = null;
let startX = 0;
let startY = 0;
let startWidth = 0;
let startHeight = 0;
let startWidthGrid = 0; // Starting width in grid units
let startHeightGrid = 0; // Starting height in grid units
let currentWidthGrid = 0; // Current width in grid units (to track changes)
let currentHeightGrid = 0; // Current height in grid units (to track changes)

function handleResizeStart(e, element) {
    e.preventDefault();
    e.stopPropagation();
    
    isResizing = true;
    resizeElement = element;
    startX = e.clientX;
    startY = e.clientY;
    startWidth = parseInt(window.getComputedStyle(element).width, 10);
    startHeight = parseInt(window.getComputedStyle(element).height, 10);
    
    // Calculate starting size in grid units (snapped to grid)
    const gridSize = ChartConfig.gridSize;
    startWidthGrid = Math.round(startWidth / gridSize);
    startHeightGrid = Math.round(startHeight / gridSize);
    currentWidthGrid = startWidthGrid;
    currentHeightGrid = startHeightGrid;

    document.addEventListener('mousemove', handleResize);
    document.addEventListener('mouseup', handleResizeEnd);
    
    element.style.cursor = 'nwse-resize';
}

function handleResize(e) {
    if (!isResizing || !resizeElement) return;

    const gridSize = ChartConfig.gridSize;
    
    // Calculate mouse movement in pixels
    const deltaX = e.clientX - startX;
    const deltaY = e.clientY - startY;
    
    // Calculate new size in grid units based on mouse movement
    // Round to nearest grid unit to determine target grid size
    const targetWidthGrid = Math.round((startWidth + deltaX) / gridSize);
    const targetHeightGrid = Math.round((startHeight + deltaY) / gridSize);
    
    // Only update if the grid unit count has changed by at least 1
    let newWidthGrid = currentWidthGrid;
    let newHeightGrid = currentHeightGrid;
    
    if (targetWidthGrid !== currentWidthGrid) {
        // Only allow change by one grid unit at a time
        if (targetWidthGrid > currentWidthGrid) {
            newWidthGrid = currentWidthGrid + 1;
        } else if (targetWidthGrid < currentWidthGrid) {
            newWidthGrid = currentWidthGrid - 1;
        }
    }
    
    if (targetHeightGrid !== currentHeightGrid) {
        // Only allow change by one grid unit at a time
        if (targetHeightGrid > currentHeightGrid) {
            newHeightGrid = currentHeightGrid + 1;
        } else if (targetHeightGrid < currentHeightGrid) {
            newHeightGrid = currentHeightGrid - 1;
        }
    }
    
    // Convert grid units back to pixels
    let newWidth = newWidthGrid * gridSize;
    let newHeight = newHeightGrid * gridSize;
    
    // Apply constraints (in grid units first, then convert)
    const minWidthGrid = Math.ceil(ChartConfig.minWidth / gridSize);
    const maxWidthGrid = Math.floor(ChartConfig.maxWidth / gridSize);
    const minHeightGrid = Math.ceil(ChartConfig.minHeight / gridSize);
    const maxHeightGrid = Math.floor(ChartConfig.maxHeight / gridSize);
    
    newWidthGrid = Math.max(minWidthGrid, Math.min(maxWidthGrid, newWidthGrid));
    newHeightGrid = Math.max(minHeightGrid, Math.min(maxHeightGrid, newHeightGrid));
    
    // Convert back to pixels
    newWidth = newWidthGrid * gridSize;
    newHeight = newHeightGrid * gridSize;
    
    // Only update if size actually changed
    if (newWidthGrid !== currentWidthGrid || newHeightGrid !== currentHeightGrid) {
        currentWidthGrid = newWidthGrid;
        currentHeightGrid = newHeightGrid;
        
        resizeElement.style.width = newWidth + 'px';
        resizeElement.style.height = newHeight + 'px';
        resizeElement.classList.add('resizing');

        // Update chart after a small delay to avoid too many resize calls
        clearTimeout(resizeElement._resizeTimeout);
        resizeElement._resizeTimeout = setTimeout(() => {
            const chartId = resizeElement.dataset.chartId;
            if (DashboardState.chartInstances[chartId] && typeof DashboardState.chartInstances[chartId].resize === 'function') {
                DashboardState.chartInstances[chartId].resize();
            }
        }, 50);
    }
}

function handleResizeEnd() {
    isResizing = false;
    if (resizeElement) {
        resizeElement.style.cursor = 'default';
        resizeElement.classList.remove('resizing');
        
        // Ensure final size is snapped to grid
        const gridSize = ChartConfig.gridSize;
        const computedStyle = window.getComputedStyle(resizeElement);
        let finalWidth = parseInt(computedStyle.width, 10);
        let finalHeight = parseInt(computedStyle.height, 10);
        
        // Snap to grid
        finalWidth = Math.round(finalWidth / gridSize) * gridSize;
        finalHeight = Math.round(finalHeight / gridSize) * gridSize;
        
        // Apply constraints one more time
        finalWidth = Math.max(ChartConfig.minWidth, Math.min(ChartConfig.maxWidth, finalWidth));
        finalHeight = Math.max(ChartConfig.minHeight, Math.min(ChartConfig.maxHeight, finalHeight));
        
        // Update element size
        resizeElement.style.width = finalWidth + 'px';
        resizeElement.style.height = finalHeight + 'px';
        
        // Save position and size
        const chartId = resizeElement.dataset.chartId;
        DashboardState.chartPositions[chartId] = {
            x: parseInt(computedStyle.left) || 0,
            y: parseInt(computedStyle.top) || 0,
            width: finalWidth + 'px',
            height: finalHeight + 'px'
        };
        saveChartPositions();
        
        // Final resize call
        if (DashboardState.chartInstances[chartId] && typeof DashboardState.chartInstances[chartId].resize === 'function') {
            DashboardState.chartInstances[chartId].resize();
        }
        
        // Reset tracking variables
        resizeElement = null;
        currentWidthGrid = 0;
        currentHeightGrid = 0;
    }
    document.removeEventListener('mousemove', handleResize);
    document.removeEventListener('mouseup', handleResizeEnd);
}

// Show grid overlay for visual feedback
function showGridOverlay() {
    const container = document.getElementById('dashboardChartsContainer');
    if (!container) return;
    
    // Remove existing overlay if any
    let overlay = container.querySelector('.dashboard-grid-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'dashboard-grid-overlay';
        container.appendChild(overlay);
    }
    
    overlay.style.display = 'block';
    updateGridOverlay();
}

// Hide grid overlay
function hideGridOverlay() {
    const container = document.getElementById('dashboardChartsContainer');
    if (!container) return;
    
    const overlay = container.querySelector('.dashboard-grid-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Update grid overlay to match container size
function updateGridOverlay() {
    const container = document.getElementById('dashboardChartsContainer');
    if (!container) return;
    
    const overlay = container.querySelector('.dashboard-grid-overlay');
    if (!overlay) return;
    
    const containerRect = container.getBoundingClientRect();
    const gridSize = ChartConfig.gridSize;
    
    // Create grid pattern using CSS
    const gridPattern = `
        linear-gradient(to right, rgba(37, 99, 235, 0.1) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(37, 99, 235, 0.1) 1px, transparent 1px)
    `;
    
    overlay.style.backgroundImage = gridPattern;
    overlay.style.backgroundSize = `${gridSize}px ${gridSize}px`;
    overlay.style.width = containerRect.width + 'px';
    overlay.style.height = containerRect.height + 'px';
}

// Remove chart
function removeChart(chartId) {
    const chartElement = document.getElementById(`chart-${chartId}`);
    if (chartElement) {
        chartElement.remove();
        
        // Destroy chart instance
        if (DashboardState.chartInstances[chartId]) {
            DashboardState.chartInstances[chartId].destroy();
            delete DashboardState.chartInstances[chartId];
        }

        // Remove from state
        DashboardState.charts = DashboardState.charts.filter(chart => chart.id !== chartId);
        
        // Remove saved position
        delete DashboardState.chartPositions[chartId];
        saveChartPositions();
        
        // Update container height
        updateContainerHeight();
    }
}

// Load Dashboard content
function loadDashboardView() {
    // Reset initialization state to allow re-initialization
    DashboardState.isInitialized = false;
    initDashboard();
    
    // Show processing info if available
    setTimeout(() => {
        const processingInfo = document.getElementById('processing-info');
        if (processingInfo) {
            processingInfo.style.display = 'block';
        }
    }, 300);
}

// Export for use in main script
if (typeof window !== 'undefined') {
    window.initDashboard = initDashboard;
    window.loadDashboardView = loadDashboardView;
    window.removeChart = removeChart;
}



const dashboard = {
  chartsInstance: {},

  render() {
    const user = api.getUser();
    
    document.getElementById('app').innerHTML = `
      <div class="dashboard">
        <aside class="sidebar">
          <div class="sidebar-logo">
            <div class="logo-icon">🧵</div>
            <h2 class="floating-title" style="font-size: 1.2rem; animation: glowPulse 3s infinite;">TWIP</h2>
          </div>
          <nav>
            <div class="nav-item active" id="nav-overview" onclick="dashboard.navigate('overview')">
              <span style="font-size: 1.2rem;">📊</span> Overview
            </div>
            <div class="nav-item" id="nav-inventory" onclick="dashboard.navigate('inventory')">
              <span style="font-size: 1.2rem;">📦</span> Inventory
            </div>
            <div class="nav-item" id="nav-classification" onclick="dashboard.navigate('classification')">
              <span style="font-size: 1.2rem;">🔬</span> Classification
            </div>
            <div class="nav-item" id="nav-reports" onclick="dashboard.navigate('reports')">
              <span style="font-size: 1.2rem;">📋</span> Reports
            </div>
            <div class="nav-item" id="nav-upload" onclick="dashboard.navigate('upload')">
              <span style="font-size: 1.2rem;">☁️</span> Upload Data
            </div>
            <div class="nav-item" id="nav-analytics" onclick="dashboard.navigate('analytics')">
              <span style="font-size: 1.2rem;">📈</span> Analytics
            </div>
            <div class="nav-item" id="nav-profile" onclick="dashboard.navigate('profile')">
              <span style="font-size: 1.2rem;">👤</span> Profile
            </div>
          </nav>
          <div class="user-info">
            <div style="color: white; font-weight: 600; font-family: Outfit;">${user?.username || 'Guest User'}</div>
            <div style="color: var(--text-muted); font-size: 0.8rem; margin-bottom: 1.2rem;">${user?.role || 'Operator'}</div>
            <button class="btn-primary" onclick="app.logout()" style="padding: 0.7rem; font-size: 0.9rem;">Log Out</button>
          </div>
        </aside>
        <main class="main-content" id="main-content">
          <!-- View gets injected here -->
        </main>
      </div>
    `;

    this.navigate('overview');
  },

  navigate(view) {
    // Update nav active state
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    const activeNav = document.getElementById(`nav-${view}`);
    if(activeNav) activeNav.classList.add('active');

    // Destroy existing charts to prevent memory leaks
    Object.values(this.chartsInstance).forEach(chart => chart.destroy());
    this.chartsInstance = {};

    const main = document.getElementById('main-content');
    main.innerHTML = '';
    
    switch(view) {
      case 'overview':
        this.renderOverview(main);
        break;
      case 'inventory':
        this.renderInventory(main);
        break;
      case 'classification':
        this.renderClassification(main);
        break;
      case 'reports':
        this.renderReports(main);
        break;
      case 'upload':
        this.renderUpload(main);
        break;
      case 'analytics':
        this.renderAnalytics(main);
        break;
      case 'profile':
        this.renderProfile(main);
        break;
    }
  },

  renderOverview(container) {
    container.innerHTML = `
      <div class="section-header">
        <div>
          <h1 class="section-title floating-title" style="font-size: 2rem; background: linear-gradient(135deg, #f3f4f6, #9ca3af); -webkit-background-clip: text;">Dashboard Overview</h1>
          <p class="section-subtitle">Real-time intelligence on textile waste flows.</p>
        </div>
      </div>
      
      <div class="metrics-grid" id="metrics-container">
        <!-- Metrics generated here -->
      </div>
      
      <div class="charts-grid">
        <div class="chart-card">
          <h3>Material Distribution</h3>
          <canvas id="materialChart"></canvas>
        </div>
        <div class="chart-card">
          <h3>Waste Categories</h3>
          <canvas id="categoryChart"></canvas>
        </div>
        <div class="chart-card" style="grid-column: 1 / -1;">
          <h3>Monthly Waste Volume Trends</h3>
          <canvas id="trendChart"></canvas>
        </div>
      </div>
    `;

    this.renderMetricCards();
    setTimeout(() => this.renderCharts(), 100);
  },

  renderMetricCards() {
    const metrics = [
      { label: 'Total Batches', value: 1248, change: '+12.5%', isPos: true, icon: '📦' },
      { label: 'Total Weight (kg)', value: 85400, change: '+5.2%', isPos: true, icon: '⚖️' },
      { label: 'Avg Recyclability', value: 68, suffix: '%', change: '+2.1%', isPos: true, icon: '♻️' },
      { label: 'Carbon Saved (tons)', value: 342, change: '-1.4%', isPos: false, icon: '🌱' }
    ];

    const container = document.getElementById('metrics-container');
    container.innerHTML = metrics.map((m, idx) => `
      <div class="metric-card" style="animation-delay: ${idx * 0.1}s">
        <div class="metric-icon">${m.icon}</div>
        <div class="metric-value" data-target="${m.value}">0</div>
        <div class="metric-label">${m.label}</div>
        <div class="metric-change ${m.isPos ? 'positive' : 'negative'}">
          ${m.isPos ? '↑' : '↓'} ${m.change} from last month
        </div>
      </div>
    `).join('');

    // Animate numbers
    document.querySelectorAll('.metric-value').forEach(el => {
      const target = parseInt(el.getAttribute('data-target'));
      const suffix = el.nextElementSibling.innerText.includes('Recyclability') ? '%' : '';
      this.animateValue(el, 0, target, 1500, suffix);
    });
  },

  animateValue(obj, start, end, duration, suffix = '') {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      // Ease out quad
      const easeOut = progress * (2 - progress);
      const current = Math.floor(easeOut * (end - start) + start);
      obj.innerHTML = current.toLocaleString() + suffix;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        obj.innerHTML = end.toLocaleString() + suffix;
      }
    };
    window.requestAnimationFrame(step);
  },

  renderCharts() {
    Chart.defaults.color = '#9ca3af';
    Chart.defaults.font.family = 'Inter';

    // Doughnut Chart
    const ctxMat = document.getElementById('materialChart').getContext('2d');
    this.chartsInstance.material = new Chart(ctxMat, {
      type: 'doughnut',
      data: {
        labels: ['Cotton', 'Polyester', 'Wool', 'Silk', 'Blends'],
        datasets: [{
          data: [45, 25, 10, 5, 15],
          backgroundColor: ['#10b981', '#06b6d4', '#f59e0b', '#ec4899', '#8b5cf6'],
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }
    });

    // Bar Chart
    const ctxCat = document.getElementById('categoryChart').getContext('2d');
    this.chartsInstance.category = new Chart(ctxCat, {
      type: 'bar',
      data: {
        labels: ['Recyclable', 'Reusable', 'Repairable', 'Hazardous', 'Compostable'],
        datasets: [{
          label: 'Volume (kg)',
          data: [35000, 22000, 15000, 3400, 10000],
          backgroundColor: '#38bdf8',
          borderRadius: 6
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });

    // Line Chart
    const ctxTrend = document.getElementById('trendChart').getContext('2d');
    const gradient = ctxTrend.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(16, 185, 129, 0.5)');
    gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');
    
    this.chartsInstance.trend = new Chart(ctxTrend, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Total Collected',
          data: [12000, 13500, 11000, 14200, 16000, 15500, 18000],
          borderColor: '#10b981',
          backgroundColor: gradient,
          borderWidth: 3,
          tension: 0.4,
          fill: true
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });
  },

  renderInventory(container) {
    container.innerHTML = `
      <div class="section-header">
        <div>
          <h1 class="section-title">Waste Inventory</h1>
          <p class="section-subtitle">Manage and track textile waste batches.</p>
        </div>
        <button class="btn-primary" style="width: auto; padding: 0.6rem 1.2rem;" onclick="dashboard.toggleAddForm()">+ Add New Batch</button>
      </div>

      <div class="chart-card" id="addBatchForm" style="display: none; margin-bottom: 2rem;">
        <h3 style="margin-bottom: 1.5rem;">Register New Batch</h3>
        <form onsubmit="dashboard.submitBatch(event)">
          <div class="form-row">
            <div class="form-group">
              <label>Material Type</label>
              <select class="form-select" required>
                <option value="Cotton">Cotton</option>
                <option value="Polyester">Polyester</option>
                <option value="Wool">Wool</option>
                <option value="Blends">Blends</option>
              </select>
            </div>
            <div class="form-group">
              <label>Weight (kg)</label>
              <input type="number" class="form-input" required>
            </div>
            <div class="form-group">
              <label>Category</label>
              <select class="form-select" required>
                <option value="Recyclable">Recyclable</option>
                <option value="Reusable">Reusable</option>
                <option value="Compostable">Compostable</option>
                <option value="Hazardous">Hazardous</option>
              </select>
            </div>
            <div class="form-group">
              <label>Source Facility</label>
              <input type="text" class="form-input" required>
            </div>
          </div>
          <button type="submit" class="btn-primary" style="margin-top: 1rem; width: auto; padding: 0.7rem 2rem;">Save Batch</button>
        </form>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Batch ID</th>
              <th>Date Registered</th>
              <th>Material</th>
              <th>Weight</th>
              <th>Category</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>#BW-8492</td>
              <td>2023-10-12</td>
              <td>100% Cotton</td>
              <td>450 kg</td>
              <td><span class="badge badge-recyclable">Recyclable</span></td>
              <td>Processing</td>
              <td><button class="btn-primary" style="padding: 0.3rem 0.8rem; font-size:0.8rem;">View</button></td>
            </tr>
            <tr>
              <td>#BW-8493</td>
              <td>2023-10-12</td>
              <td>Poly-Blend</td>
              <td>120 kg</td>
              <td><span class="badge badge-reusable">Reusable</span></td>
              <td>Sorted</td>
              <td><button class="btn-primary" style="padding: 0.3rem 0.8rem; font-size:0.8rem;">View</button></td>
            </tr>
            <tr>
              <td>#BW-8494</td>
              <td>2023-10-11</td>
              <td>Chemical Dyed</td>
              <td>80 kg</td>
              <td><span class="badge badge-hazardous">Hazardous</span></td>
              <td>Quarantine</td>
              <td><button class="btn-primary" style="padding: 0.3rem 0.8rem; font-size:0.8rem;">View</button></td>
            </tr>
            <tr>
              <td>#BW-8495</td>
              <td>2023-10-11</td>
              <td>Organic Hemp</td>
              <td>200 kg</td>
              <td><span class="badge badge-compostable">Compostable</span></td>
              <td>Dispatched</td>
              <td><button class="btn-primary" style="padding: 0.3rem 0.8rem; font-size:0.8rem;">View</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    `;
  },

  toggleAddForm() {
    const form = document.getElementById('addBatchForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  },

  submitBatch(event) {
    event.preventDefault();
    app.showToast('Batch successfully registered!', 'success');
    this.toggleAddForm();
  },

  // =========================================================================
  //  MILESTONE 2 — Classification Engine
  // =========================================================================
  renderClassification(container) {
    const demoResults = this._getDemoClassification();

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h1 class="section-title floating-title" style="font-size: 2rem; background: linear-gradient(135deg, #c084fc, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Material Classification Engine</h1>
          <p class="section-subtitle">AI-powered textile recognition, waste categorization, and recyclability assessment.</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <div class="chart-card" style="flex:1; min-width:280px;">
          <h3 style="margin-bottom:1.2rem;">🔬 Quick Classify</h3>
          <div style="display:flex; gap:0.8rem; flex-wrap:wrap; align-items:flex-end;">
            <div style="flex:1; min-width:120px;">
              <label style="display:block; color:var(--text-muted); font-size:0.85rem; margin-bottom:6px;">Batch ID</label>
              <select id="classifyBatchSelect" class="form-select" style="width:100%;">
                ${Array.from({length:10}, (_,i) => `<option value="${i+1}">Batch #${i+1}</option>`).join('')}
              </select>
            </div>
            <button class="btn-analyze" onclick="dashboard.analyzeBatch()">⚡ Analyze</button>
            <button class="btn-bulk" onclick="dashboard.bulkClassify()">🔄 Bulk Classify All</button>
          </div>
          <div id="classifyStatus" style="margin-top:0.8rem; font-size:0.85rem; color:var(--text-muted);"></div>
        </div>

        <div class="chart-card" style="flex:1; min-width:280px;">
          <h3 style="margin-bottom:1.2rem;">📷 Image Analysis</h3>
          <div class="upload-zone" style="padding:2rem; min-height:auto;" ondragover="event.preventDefault(); this.classList.add('dragover')" ondragleave="this.classList.remove('dragover')" ondrop="dashboard.handleImageDrop(event)">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🖼️</div>
            <p style="color:var(--text-muted); font-size:0.9rem;">Drop textile image here</p>
            <button class="btn-primary" style="width:auto; padding:0.5rem 1.5rem; margin-top:0.8rem; font-size:0.85rem;" onclick="document.getElementById('imageInput').click()">Browse</button>
            <input type="file" id="imageInput" accept="image/*" style="display:none;" onchange="dashboard.handleImageUpload(this.files)">
          </div>
          <div id="imageStatus" style="margin-top:0.8rem; font-size:0.85rem; color:var(--text-muted);"></div>
        </div>
      </div>

      <!-- Classification Results -->
      <div id="classificationResults"></div>
    `;

    // Show demo results immediately
    this.renderClassificationResults(demoResults);
  },

  _getDemoClassification() {
    return {
      classification: {
        material_detected: 'Cotton', confidence: 0.943,
        fiber_composition: { 'Cotton': 92.5, 'Elastane': 7.5 },
        texture: 'soft', pattern: 'twill',
        secondary_materials: [{ material: 'Polyester', confidence: 0.08 }, { material: 'Nylon', confidence: 0.05 }],
        properties: { weight_class: 'Medium Weight', recyclability_base: 0.85, market_demand_index: 0.9 }
      },
      categorization: {
        recommended_category: 'Recyclable', confidence: 0.9,
        category_description: 'Textiles suitable for fiber-to-fiber recycling',
        processing_cost: 'Medium', environmental_benefit: 'High',
        reasoning: ['Condition "Recyclable" matches category', 'Damage level acceptable (None)', 'Contamination level acceptable (None)', 'Recyclability score (85.0%) meets minimum']
      },
      recyclability: {
        recyclability_score: 82.5, grade: 'B', grade_label: 'Good - Readily Recyclable',
        reuse_potential: 'High - Suitable for direct resale or donation',
        recommendations: [
          'Prioritize for fiber-to-fiber recycling - Cotton has high recovery potential',
          'Consider upcycling partnerships for premium waste streams',
          'Pre-sort by color to maximize recycled fiber quality'
        ],
        environmental_impact: {
          carbon_saved_kg: 525.0, water_saved_liters: 25200.0,
          landfill_diverted_kg: 210.0, energy_saved_kwh: 3255.0
        }
      }
    };
  },

  async analyzeBatch() {
    const batchId = document.getElementById('classifyBatchSelect').value;
    const status = document.getElementById('classifyStatus');
    status.innerHTML = '<span style="color:#a78bfa;">⏳ Analyzing batch #' + batchId + '...</span>';

    try {
      const res = await api.post('/classify/analyze?batch_id=' + batchId);
      if (res.ok) {
        const data = await res.json();
        status.innerHTML = '<span style="color:#10b981;">✓ Analysis complete!</span>';
        this.renderClassificationResults(data);
      } else {
        throw new Error('API returned ' + res.status);
      }
    } catch (e) {
      status.innerHTML = '<span style="color:#f59e0b;">⚠ Using demo results (API: ' + e.message + ')</span>';
      this.renderClassificationResults(this._getDemoClassification());
    }
  },

  async bulkClassify() {
    const status = document.getElementById('classifyStatus');
    status.innerHTML = '<span style="color:#22d3ee;">⏳ Running bulk classification...</span>';

    try {
      const res = await api.post('/classify/bulk');
      if (res.ok) {
        const data = await res.json();
        status.innerHTML = '<span style="color:#10b981;">✓ Bulk complete! ' + data.total_analyzed + ' batches analyzed.</span>';
        if (data.results && data.results.length > 0) {
          this._renderBulkResults(data.results);
        }
      } else {
        throw new Error('API returned ' + res.status);
      }
    } catch (e) {
      status.innerHTML = '<span style="color:#f59e0b;">⚠ Demo mode (API: ' + e.message + ')</span>';
      this._renderBulkResults([
        { batch_id: 'TWB-001', material: 'Cotton', category: 'Recyclable', grade: 'A', score: 87.2 },
        { batch_id: 'TWB-002', material: 'Polyester', category: 'Reusable', grade: 'B', score: 72.1 },
        { batch_id: 'TWB-003', material: 'Denim', category: 'Upcyclable', grade: 'A', score: 89.5 },
        { batch_id: 'TWB-004', material: 'Nylon', category: 'Recyclable', grade: 'C', score: 58.3 },
        { batch_id: 'TWB-005', material: 'Mixed Fabrics', category: 'Hazardous Textile Waste', grade: 'F', score: 32.1 },
      ]);
    }
  },

  _renderBulkResults(results) {
    const container = document.getElementById('classificationResults');
    container.innerHTML = `
      <div class="classification-card full-width" style="animation-delay:0.1s;">
        <h4>📊 Bulk Classification Results (${results.length} batches)</h4>
        <div class="table-container" style="margin-top:1rem;">
          <table class="data-table">
            <thead><tr><th>Batch</th><th>Material</th><th>Category</th><th>Grade</th><th>Score</th></tr></thead>
            <tbody>
              ${results.map(r => `
                <tr>
                  <td>${r.batch_id}</td>
                  <td>${r.material}</td>
                  <td><span class="badge badge-recyclable">${r.category}</span></td>
                  <td><span class="grade-badge grade-${r.grade}" style="width:36px; height:36px; font-size:1rem; border-radius:8px;">${r.grade}</span></td>
                  <td>${r.score}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  handleImageDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
    this.handleImageUpload(event.dataTransfer.files);
  },

  async handleImageUpload(files) {
    if (!files || files.length === 0) return;
    const status = document.getElementById('imageStatus');
    status.innerHTML = '<span style="color:#a78bfa;">⏳ Analyzing image...</span>';

    try {
      const res = await api.uploadFile('/classify/image', files[0]);
      if (res.ok) {
        const data = await res.json();
        status.innerHTML = '<span style="color:#10b981;">✓ ' + data.material_detected + ' detected (' + (data.confidence * 100).toFixed(1) + '% conf)</span>';
      } else {
        throw new Error('Upload failed');
      }
    } catch (e) {
      status.innerHTML = '<span style="color:#f59e0b;">⚠ Demo: Cotton detected (94.3% conf)</span>';
    }
  },

  renderClassificationResults(data) {
    const c = data.classification;
    const cat = data.categorization;
    const r = data.recyclability;
    const confPct = (c.confidence * 100).toFixed(1);
    const circumference = 2 * Math.PI * 42;
    const offset = circumference - (r.recyclability_score / 100) * circumference;

    // Grade color map
    const gradeColors = { A: '#10b981', B: '#38bdf8', C: '#f59e0b', D: '#f97316', F: '#ef4444' };
    const gradeColor = gradeColors[r.grade] || '#9ca3af';

    const container = document.getElementById('classificationResults');
    container.innerHTML = `
      <div class="classification-grid">
        <!-- Material Analysis Card -->
        <div class="classification-card" style="animation-delay:0.1s;">
          <h4>🧪 Material Analysis</h4>
          <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
            <div style="font-size:2.5rem;">🧶</div>
            <div>
              <div style="font-family:Outfit; font-size:1.5rem; font-weight:700; color:white;">${c.material_detected}</div>
              <div style="color:var(--text-muted); font-size:0.85rem;">Confidence: ${confPct}%</div>
            </div>
          </div>
          <div class="confidence-bar"><div class="confidence-bar-fill" style="width:${confPct}%;"></div></div>
          <div style="display:flex; gap:1.5rem; margin-top:1.2rem;">
            <div><span style="color:var(--text-muted); font-size:0.8rem;">Texture</span><div style="color:white; font-weight:600; text-transform:capitalize;">${c.texture}</div></div>
            <div><span style="color:var(--text-muted); font-size:0.8rem;">Pattern</span><div style="color:white; font-weight:600; text-transform:capitalize;">${c.pattern}</div></div>
            <div><span style="color:var(--text-muted); font-size:0.8rem;">Weight</span><div style="color:white; font-weight:600;">${c.properties?.weight_class || 'Medium'}</div></div>
          </div>
        </div>

        <!-- Fiber Composition Card -->
        <div class="classification-card" style="animation-delay:0.2s;">
          <h4>🧬 Fiber Composition</h4>
          ${Object.entries(c.fiber_composition || {}).map(([fiber, pct], i) => {
            const colors = ['#10b981', '#38bdf8', '#f59e0b', '#ec4899', '#8b5cf6'];
            return `
              <div class="fiber-bar-container">
                <div class="fiber-bar-label"><span>${fiber}</span><span>${pct}%</span></div>
                <div class="fiber-bar"><div class="fiber-bar-fill" style="width:${pct}%; background:${colors[i % colors.length]};"></div></div>
              </div>
            `;
          }).join('')}
          ${(c.secondary_materials || []).length > 0 ? `
            <div style="margin-top:1rem; padding-top:0.8rem; border-top:1px solid rgba(255,255,255,0.06);">
              <div style="color:var(--text-muted); font-size:0.8rem; margin-bottom:0.5rem;">Trace Materials Detected</div>
              ${c.secondary_materials.map(s => `<span style="display:inline-block; padding:4px 10px; background:rgba(255,255,255,0.05); border-radius:20px; font-size:0.8rem; color:var(--text-muted); margin:2px 4px;">${s.material} (${(s.confidence*100).toFixed(1)}%)</span>`).join('')}
            </div>
          ` : ''}
        </div>

        <!-- Waste Category Card -->
        <div class="classification-card" style="animation-delay:0.3s;">
          <h4>🗂️ Waste Categorization</h4>
          <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
            <span class="badge badge-recyclable" style="font-size:1rem; padding:0.6rem 1.2rem;">${cat.recommended_category}</span>
            <span style="color:var(--text-muted); font-size:0.85rem;">${(cat.confidence * 100).toFixed(0)}% confidence</span>
          </div>
          <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:1rem;">${cat.category_description}</p>
          <div style="display:flex; gap:1.5rem;">
            <div><span style="color:var(--text-muted); font-size:0.8rem;">Processing Cost</span><div style="color:white; font-weight:600;">${cat.processing_cost}</div></div>
            <div><span style="color:var(--text-muted); font-size:0.8rem;">Env. Benefit</span><div style="color:#10b981; font-weight:600;">${cat.environmental_benefit}</div></div>
          </div>
          <div style="margin-top:1rem; padding-top:0.8rem; border-top:1px solid rgba(255,255,255,0.06);">
            <div style="color:var(--text-muted); font-size:0.8rem; margin-bottom:0.5rem;">Decision Reasoning</div>
            ${(cat.reasoning || []).map(r => `<div style="font-size:0.82rem; color:var(--text); padding:3px 0;">• ${r}</div>`).join('')}
          </div>
        </div>

        <!-- Recyclability Assessment Card -->
        <div class="classification-card" style="animation-delay:0.4s;">
          <h4>♻️ Recyclability Assessment</h4>
          <div style="display:flex; align-items:center; gap:2rem; margin-bottom:1rem;">
            <div class="score-circle">
              <svg viewBox="0 0 100 100">
                <circle class="bg" cx="50" cy="50" r="42"/>
                <circle class="progress" cx="50" cy="50" r="42" stroke="${gradeColor}"
                  stroke-dasharray="${circumference}" stroke-dashoffset="${offset}"/>
              </svg>
              <div class="score-value">${r.recyclability_score}</div>
            </div>
            <div>
              <div class="grade-badge grade-${r.grade}">${r.grade}</div>
              <div style="color:var(--text-muted); font-size:0.82rem; margin-top:0.5rem;">${r.grade_label}</div>
            </div>
          </div>
          <div style="color:var(--text-muted); font-size:0.8rem; margin-bottom:4px;">Reuse Potential</div>
          <div style="color:white; font-size:0.9rem; font-weight:500;">${r.reuse_potential}</div>
        </div>

        <!-- Environmental Impact Card -->
        <div class="classification-card" style="animation-delay:0.5s;">
          <h4>🌍 Environmental Impact</h4>
          ${r.environmental_impact ? `
            <div class="impact-metric">
              <div class="impact-icon">🌿</div>
              <div><div class="impact-value">${r.environmental_impact.carbon_saved_kg?.toLocaleString() || 0} kg</div><div class="impact-label">Carbon Saved</div></div>
            </div>
            <div class="impact-metric">
              <div class="impact-icon">💧</div>
              <div><div class="impact-value">${r.environmental_impact.water_saved_liters?.toLocaleString() || 0} L</div><div class="impact-label">Water Saved</div></div>
            </div>
            <div class="impact-metric">
              <div class="impact-icon">🏭</div>
              <div><div class="impact-value">${r.environmental_impact.landfill_diverted_kg?.toLocaleString() || 0} kg</div><div class="impact-label">Landfill Diverted</div></div>
            </div>
            <div class="impact-metric">
              <div class="impact-icon">⚡</div>
              <div><div class="impact-value">${r.environmental_impact.energy_saved_kwh?.toLocaleString() || 0} kWh</div><div class="impact-label">Energy Saved</div></div>
            </div>
          ` : '<p style="color:var(--text-muted);">No impact data available.</p>'}
        </div>

        <!-- Recommendations Card -->
        <div class="classification-card" style="animation-delay:0.6s;">
          <h4>💡 Recommendations</h4>
          ${(r.recommendations || []).map(rec => `<div class="rec-item">${rec}</div>`).join('')}
        </div>
      </div>
    `;
  },

  // =========================================================================
  //  MILESTONE 2 — Reports Dashboard
  // =========================================================================
  renderReports(container) {
    container.innerHTML = `
      <div class="section-header">
        <div>
          <h1 class="section-title floating-title" style="font-size: 2rem; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Waste Classification Reports</h1>
          <p class="section-subtitle">Comprehensive analytics and environmental impact summaries.</p>
        </div>
      </div>

      <!-- Summary Metrics -->
      <div class="metrics-grid" id="reportMetrics">
        <div class="metric-card" style="animation-delay:0s"><div class="metric-icon">📊</div><div class="metric-value" data-target="120">0</div><div class="metric-label">Total Analyzed</div></div>
        <div class="metric-card" style="animation-delay:0.1s"><div class="metric-icon">🏆</div><div class="metric-value">B</div><div class="metric-label">Average Grade</div></div>
        <div class="metric-card" style="animation-delay:0.2s"><div class="metric-icon">🌿</div><div class="metric-value" data-target="31312">0</div><div class="metric-label">Carbon Saved (kg)</div></div>
        <div class="metric-card" style="animation-delay:0.3s"><div class="metric-icon">💧</div><div class="metric-value" data-target="1001988">0</div><div class="metric-label">Water Saved (L)</div></div>
      </div>

      <div style="margin-bottom:2rem;">
        <button class="btn-analyze" style="padding:0.9rem 2rem; font-size:1rem;" onclick="dashboard.generateSummaryReport()">📋 Generate Full Summary Report</button>
        <span id="reportStatus" style="margin-left:1rem; font-size:0.85rem; color:var(--text-muted);"></span>
      </div>

      <div id="reportResults"></div>
    `;

    // Animate metric values
    document.querySelectorAll('#reportMetrics .metric-value[data-target]').forEach(el => {
      const target = parseInt(el.getAttribute('data-target'));
      this.animateValue(el, 0, target, 1500);
    });

    // Auto-load demo report
    this._renderReportData(this._getDemoReport());
  },

  _getDemoReport() {
    return {
      overview: { total_batches_analyzed: 120, total_weight_kg: 20500.0, average_recyclability: 0.611, overall_grade: 'C' },
      material_analysis: {
        distribution_by_count: { Cotton: 15, Polyester: 14, Denim: 18, Wool: 8, Silk: 5, Nylon: 14, Linen: 10, Rayon: 16, Acrylic: 8, 'Mixed Fabrics': 12 },
        distribution_by_weight_kg: { Cotton: 1432.5, Polyester: 3112.0, Denim: 3832.5, Wool: 590.5, Silk: 176.0, Nylon: 1912.0, Linen: 1070.0, Rayon: 2512.0, Acrylic: 950.5, 'Mixed Fabrics': 4912.0 }
      },
      category_breakdown: { Recyclable: 24, Reusable: 24, Repairable: 24, Compostable: 12, Upcyclable: 12, 'Hazardous Textile Waste': 24 },
      grade_distribution: { A: 18, B: 30, C: 36, D: 24, F: 12 },
      environmental_impact: { total_carbon_saved_kg: 31312.5, total_water_saved_liters: 1001988.0, total_landfill_diverted_kg: 12525.5 },
      recommendations: [
        'Moderate recyclability. Consider better pre-sorting equipment.',
        'Primary material stream: Denim. Consider dedicated processing line.',
        'ALERT: 24 hazardous waste batches detected.',
        'Schedule quarterly waste audits to track recyclability trends.'
      ]
    };
  },

  async generateSummaryReport() {
    const status = document.getElementById('reportStatus');
    status.innerHTML = '<span style="color:#a78bfa;">Generating report...</span>';

    try {
      const res = await api.get('/classify/summary-report');
      if (res.ok) {
        const data = await res.json();
        status.innerHTML = '<span style="color:#10b981;">Report generated!</span>';
        this._renderReportData(data);
      } else {
        throw new Error('Status ' + res.status);
      }
    } catch (e) {
      status.innerHTML = '<span style="color:#f59e0b;">Using demo report (' + e.message + ')</span>';
      this._renderReportData(this._getDemoReport());
    }
  },

  _renderReportData(data) {
    const container = document.getElementById('reportResults');
    const ov = data.overview || {};
    const gradeColors = { A: '#10b981', B: '#38bdf8', C: '#f59e0b', D: '#f97316', F: '#ef4444' };
    const catColors = ['#10b981', '#38bdf8', '#8b5cf6', '#f59e0b', '#ec4899', '#ef4444'];
    const maxCatCount = Math.max(...Object.values(data.category_breakdown || {}), 1);

    container.innerHTML = `
      <!-- Overview Section -->
      <div class="report-section" style="animation-delay:0.1s;">
        <h3>📊 Report Overview</h3>
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:1.5rem;">
          <div style="text-align:center;">
            <div style="font-family:Outfit; font-size:2rem; font-weight:800; color:white;">${ov.total_batches_analyzed || 0}</div>
            <div style="color:var(--text-muted); font-size:0.85rem;">Total Batches</div>
          </div>
          <div style="text-align:center;">
            <div style="font-family:Outfit; font-size:2rem; font-weight:800; color:white;">${(ov.total_weight_kg || 0).toLocaleString()} kg</div>
            <div style="color:var(--text-muted); font-size:0.85rem;">Total Weight</div>
          </div>
          <div style="text-align:center;">
            <div style="font-family:Outfit; font-size:2rem; font-weight:800; color:white;">${((ov.average_recyclability || 0) * 100).toFixed(1)}%</div>
            <div style="color:var(--text-muted); font-size:0.85rem;">Avg Recyclability</div>
          </div>
          <div style="text-align:center;">
            <div class="grade-badge grade-${ov.overall_grade || 'C'}" style="margin:0 auto;">${ov.overall_grade || 'C'}</div>
            <div style="color:var(--text-muted); font-size:0.85rem; margin-top:0.5rem;">Overall Grade</div>
          </div>
        </div>
      </div>

      <!-- Material Analysis Table -->
      <div class="report-section" style="animation-delay:0.2s;">
        <h3>🧬 Material Analysis</h3>
        <div class="table-container">
          <table class="data-table">
            <thead><tr><th>Material</th><th>Count</th><th>Weight (kg)</th><th>% of Total</th></tr></thead>
            <tbody>
              ${Object.entries(data.material_analysis?.distribution_by_count || {}).map(([mat, count]) => {
                const weight = data.material_analysis?.distribution_by_weight_kg?.[mat] || 0;
                const pct = ov.total_weight_kg ? ((weight / ov.total_weight_kg) * 100).toFixed(1) : 0;
                return `<tr><td>${mat}</td><td>${count}</td><td>${weight.toLocaleString()}</td><td>${pct}%</td></tr>`;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>

      <!-- Category Breakdown -->
      <div class="report-section" style="animation-delay:0.3s;">
        <h3>🗂️ Category Breakdown</h3>
        ${Object.entries(data.category_breakdown || {}).map(([cat, count], i) => `
          <div class="category-bar-container">
            <div class="category-bar-header">
              <span class="cat-name">${cat}</span>
              <span class="cat-count">${count}</span>
            </div>
            <div class="category-bar-track">
              <div class="category-bar-fill" style="width:${(count/maxCatCount)*100}%; background:${catColors[i % catColors.length]};"></div>
            </div>
          </div>
        `).join('')}
      </div>

      <!-- Grade Distribution -->
      <div class="report-section" style="animation-delay:0.4s;">
        <h3>🏆 Grade Distribution</h3>
        <div style="display:flex; gap:1.5rem; flex-wrap:wrap; justify-content:center;">
          ${Object.entries(data.grade_distribution || {}).map(([grade, count]) => `
            <div style="text-align:center;">
              <div class="grade-badge grade-${grade}" style="margin:0 auto;">${grade}</div>
              <div style="font-family:Outfit; font-size:1.3rem; font-weight:700; color:white; margin-top:0.5rem;">${count}</div>
              <div style="color:var(--text-muted); font-size:0.8rem;">batches</div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Environmental Impact -->
      <div class="report-section" style="animation-delay:0.5s;">
        <h3>🌍 Environmental Impact Totals</h3>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:1.5rem;">
          <div class="impact-metric" style="flex-direction:column; text-align:center;">
            <div class="impact-icon">🌿</div>
            <div class="impact-value">${(data.environmental_impact?.total_carbon_saved_kg || 0).toLocaleString()} kg</div>
            <div class="impact-label">Total Carbon Saved</div>
          </div>
          <div class="impact-metric" style="flex-direction:column; text-align:center;">
            <div class="impact-icon">💧</div>
            <div class="impact-value">${(data.environmental_impact?.total_water_saved_liters || 0).toLocaleString()} L</div>
            <div class="impact-label">Total Water Saved</div>
          </div>
          <div class="impact-metric" style="flex-direction:column; text-align:center;">
            <div class="impact-icon">🏭</div>
            <div class="impact-value">${(data.environmental_impact?.total_landfill_diverted_kg || 0).toLocaleString()} kg</div>
            <div class="impact-label">Landfill Diverted</div>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div class="report-section" style="animation-delay:0.6s;">
        <h3>💡 Facility Recommendations</h3>
        ${(data.recommendations || []).map(rec => `<div class="rec-item">${rec}</div>`).join('')}
      </div>
    `;
  },

  // =========================================================================
  //  Existing sections (Upload, Analytics, Profile)
  // =========================================================================
  renderUpload(container) {
    container.innerHTML = `
      <div class="section-header">
        <div>
          <h1 class="section-title">Bulk Data Upload</h1>
          <p class="section-subtitle">Upload CSV/Excel files to import multiple records.</p>
        </div>
      </div>
      
      <div class="chart-card">
        <div class="upload-zone" id="drop-zone" ondragover="event.preventDefault(); this.classList.add('dragover')" ondragleave="this.classList.remove('dragover')" ondrop="dashboard.handleDrop(event)">
          <div class="upload-icon">📄</div>
          <h3>Drag & Drop your dataset here</h3>
          <p style="color: var(--text-muted); margin: 1rem 0;">Supported formats: CSV, XLSX (Max 10MB)</p>
          <button class="btn-primary" style="width: auto; padding: 0.6rem 2rem; margin-top: 1rem;" onclick="document.getElementById('fileInput').click()">Browse Files</button>
          <input type="file" id="fileInput" style="display: none;" onchange="dashboard.handleFileUpload(this.files)">
        </div>
      </div>
    `;
  },

  handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
    const files = event.dataTransfer.files;
    this.handleFileUpload(files);
  },

  handleFileUpload(files) {
    if (files.length > 0) {
      app.showToast('Uploading ' + files[0].name + '...', 'success');
      setTimeout(() => app.showToast('Upload completed and processed successfully.', 'success'), 2000);
    }
  },

  renderAnalytics(container) {
    container.innerHTML = `
      <div class="section-header">
        <div>
          <h1 class="section-title">Deep Analytics</h1>
          <p class="section-subtitle">Comprehensive performance indicators.</p>
        </div>
      </div>
      <div class="charts-grid">
        <div class="chart-card" style="grid-column: 1 / -1; height: 500px;">
          <h3>Recyclability Index by Material Source</h3>
          <canvas id="radarChart"></canvas>
        </div>
      </div>
    `;

    const ctxRadar = document.getElementById('radarChart').getContext('2d');
    this.chartsInstance.radar = new Chart(ctxRadar, {
      type: 'radar',
      data: {
        labels: ['Durability', 'Purity', 'Color Separation', 'Chemical Load', 'Re-spinnability', 'Market Demand'],
        datasets: [{
          label: 'Cotton Benchmark',
          data: [65, 80, 90, 70, 75, 95],
          fill: true,
          backgroundColor: 'rgba(16, 185, 129, 0.2)',
          borderColor: 'rgb(16, 185, 129)',
          pointBackgroundColor: 'rgb(16, 185, 129)',
        }, {
          label: 'Polyester Blend',
          data: [90, 45, 60, 40, 50, 70],
          fill: true,
          backgroundColor: 'rgba(6, 182, 212, 0.2)',
          borderColor: 'rgb(6, 182, 212)',
          pointBackgroundColor: 'rgb(6, 182, 212)',
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });
  },

  renderProfile(container) {
    const user = api.getUser();
    container.innerHTML = `
      <div class="section-header">
        <div>
          <h1 class="section-title">User Profile</h1>
          <p class="section-subtitle">Manage your account and preferences.</p>
        </div>
      </div>
      <div class="chart-card" style="max-width: 600px;">
        <div style="display: flex; align-items: center; gap: 2rem; margin-bottom: 2rem;">
          <div style="width: 100px; height: 100px; background: linear-gradient(135deg, var(--primary), var(--accent)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3rem;">👤</div>
          <div>
            <h2 style="font-family: Outfit; margin-bottom: 0.5rem;">${user?.username || 'Guest'}</h2>
            <p style="color: var(--text-muted);">${user?.role || 'User'}</p>
          </div>
        </div>
        <button class="btn-primary" style="background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.5);" onclick="app.logout()">Secure Logout</button>
      </div>
    `;
  }
};

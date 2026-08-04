const auth = {
  renderLoginTemplate() {
    return `
      <div class="auth-container">
        <div class="auth-card">
          <h2 class="floating-title" style="text-align: center; margin-bottom: 2rem;">🧵 TWIP</h2>
          <form id="loginForm" onsubmit="auth.handleLogin(event)">
            <div class="form-group">
              <label>Username / Email</label>
              <input type="text" id="loginUsername" placeholder="Enter your username" required>
            </div>
            <div class="form-group">
              <label>Password</label>
              <input type="password" id="loginPassword" placeholder="Enter your password" required>
            </div>
            <button type="submit" class="btn-primary" id="loginBtn">Login to Dashboard</button>
            <div class="auth-toggle">
              Don't have an account? <a href="#" onclick="auth.showRegister(); return false;">Register here</a>
            </div>
          </form>
        </div>
      </div>
    `;
  },

  renderRegisterTemplate() {
    return `
      <div class="auth-container">
        <div class="auth-card">
          <h2 class="floating-title" style="text-align: center; margin-bottom: 2rem;">🧵 Join TWIP</h2>
          <form id="registerForm" onsubmit="auth.handleRegister(event)">
            <div class="form-group">
              <label>Username</label>
              <input type="text" id="regUsername" placeholder="Choose a username" required>
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" id="regEmail" placeholder="Enter your email" required>
            </div>
            <div class="form-group">
              <label>Role</label>
              <select id="regRole" class="form-select" required>
                <option value="" disabled selected>Select your role</option>
                <option value="Administrator">Administrator</option>
                <option value="Recycling Facility Operator">Recycling Facility Operator</option>
                <option value="Sustainability Manager">Sustainability Manager</option>
                <option value="Textile Manufacturer">Textile Manufacturer</option>
              </select>
            </div>
            <div class="form-group">
              <label>Password</label>
              <input type="password" id="regPassword" placeholder="Create a password" required>
            </div>
            <button type="submit" class="btn-primary" id="regBtn">Create Account</button>
            <div class="auth-toggle">
              Already have an account? <a href="#" onclick="auth.showLogin(); return false;">Login here</a>
            </div>
          </form>
        </div>
      </div>
    `;
  },

  showLogin() {
    document.getElementById('app').innerHTML = this.renderLoginTemplate();
  },

  showRegister() {
    document.getElementById('app').innerHTML = this.renderRegisterTemplate();
  },

  async handleLogin(event) {
    event.preventDefault();
    const btn = document.getElementById('loginBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="spinner" style="width: 20px; height: 20px; border-width: 2px; margin: 0 auto;"></div>';
    btn.disabled = true;

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
      const response = await api.post('/auth/login', { username, password });
      
      if (response.ok) {
        const data = await response.json();
        api.setToken(data.access_token);
        // Fetch profile with the token
        api.setUser({ username: username, role: 'User' });
        try {
          const profileRes = await api.get('/auth/profile');
          if (profileRes.ok) { const profile = await profileRes.json(); api.setUser(profile); }
        } catch(e) {}
        app.showToast('Login successful! Welcome back.', 'success');
        dashboard.render();
      } else {
        const err = await response.json();
        app.showToast(err.detail || 'Login failed. Please check your credentials.', 'error');
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    } catch (error) {
      console.warn('API not reachable. Falling back to Demo Mode.');
      setTimeout(() => {
        api.setToken('demo_token_' + Date.now());
        api.setUser({ username: username, role: 'Sustainability Manager' });
        app.showToast('Demo login successful!', 'success');
        dashboard.render();
      }, 800);
    }
  },

  async handleRegister(event) {
    event.preventDefault();
    const btn = document.getElementById('regBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="spinner" style="width: 20px; height: 20px; border-width: 2px; margin: 0 auto;"></div>';
    btn.disabled = true;

    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const role = document.getElementById('regRole').value;
    const password = document.getElementById('regPassword').value;

    try {
      const response = await api.post('/auth/register', { username, email, role, password });
      
      if (response.ok) {
        app.showToast('Registration successful! Please login.', 'success');
        this.showLogin();
      } else {
        const err = await response.json();
        app.showToast(err.detail || 'Registration failed.', 'error');
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    } catch (error) {
      console.warn('API not reachable. Simulating successful registration.');
      setTimeout(() => {
        app.showToast('Demo Registration successful! Please login.', 'success');
        this.showLogin();
      }, 800);
    }
  }
};

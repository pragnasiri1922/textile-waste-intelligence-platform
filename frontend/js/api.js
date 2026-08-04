// Auto-detect API base URL - works both when served via FastAPI (/app) and opened directly
const API_BASE = (function() {
  const loc = window.location;
  // If served by FastAPI (e.g. http://127.0.0.1:8000/app/), use same origin
  if (loc.pathname.startsWith('/app')) {
    return loc.origin + '/api';
  }
  // Fallback for direct file:// or other dev servers
  return 'http://127.0.0.1:8000/api';
})();

const api = {
  getToken() { return localStorage.getItem('twip_token'); },
  setToken(token) { localStorage.setItem('twip_token', token); },
  clearToken() { localStorage.removeItem('twip_token'); localStorage.removeItem('twip_user'); },
  getUser() { return JSON.parse(localStorage.getItem('twip_user') || 'null'); },
  setUser(user) { localStorage.setItem('twip_user', JSON.stringify(user)); },
  
  async request(endpoint, options = {}) {
    const token = this.getToken();
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
      if (response.status === 401) { 
        this.clearToken(); 
        window.location.reload(); 
      }
      return response;
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  },
  
  async get(endpoint) { return this.request(endpoint); },
  async post(endpoint, data) { return this.request(endpoint, { method: 'POST', body: JSON.stringify(data) }); },
  async put(endpoint, data) { return this.request(endpoint, { method: 'PUT', body: JSON.stringify(data) }); },
  async delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); },
  
  async uploadFile(endpoint, file) {
    const token = this.getToken();
    const formData = new FormData();
    formData.append('file', file);
    return fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      body: formData
    });
  }
};

const app = {
  init() {
    this.initParticles();
    
    // Check authentication state
    if (api.getToken()) {
      dashboard.render();
    } else {
      auth.showLogin();
    }
  },

  logout() {
    api.clearToken();
    this.showToast('Logged out successfully', 'success');
    auth.showLogin();
  },

  initParticles() {
    const container = document.getElementById('particles');
    const particleCount = 25;
    
    for (let i = 0; i < particleCount; i++) {
      const p = document.createElement('div');
      p.className = 'particle';
      
      const size = Math.random() * 30 + 10;
      p.style.width = `${size}px`;
      p.style.height = `${size}px`;
      p.style.left = `${Math.random() * 100}vw`;
      p.style.top = `${Math.random() * 100}vh`;
      p.style.opacity = Math.random() * 0.15 + 0.05;
      
      const duration = Math.random() * 20 + 15;
      const delay = Math.random() * 5;
      p.style.animation = `floatParticle ${duration}s ease-in-out ${delay}s infinite alternate`;
      
      container.appendChild(p);
    }
  },

  showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100px)';
      toast.style.transition = 'all 0.4s ease';
      setTimeout(() => toast.remove(), 400);
    }, 4000);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  app.init();
});

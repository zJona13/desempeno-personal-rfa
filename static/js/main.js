/**
 * Main JavaScript file for Sistema Integral de Evaluación
 */

// DOM ready event
document.addEventListener('DOMContentLoaded', function() {
  // Initialize toasts with auto-dismiss
  initToasts();
  
  // Initialize form validation
  initFormValidation();
  
  // Initialize responsive navigation
  initResponsiveNav();
});

/**
 * Initialize toast notifications with auto-dismiss
 */
function initToasts() {
  const toasts = document.querySelectorAll('.toast');
  
  toasts.forEach(toast => {
    // Auto dismiss after 5 seconds
    setTimeout(() => {
      toast.classList.add('fade-out');
      toast.style.opacity = '0';
      
      // Remove from DOM after animation completes
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    }, 5000);
    
    // Add close button functionality
    const closeBtn = toast.querySelector('button');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        toast.classList.add('fade-out');
        toast.style.opacity = '0';
        
        setTimeout(() => {
          if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
          }
        }, 300);
      });
    }
  });
}

/**
 * Initialize client-side form validation
 */
function initFormValidation() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    form.addEventListener('submit', function(event) {
      let isValid = true;
      
      // Check required fields
      const requiredFields = form.querySelectorAll('[required]');
      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add('border-red-500');
          
          // Add error message if not exists
          let errorMsg = field.parentNode.querySelector('.error-message');
          if (!errorMsg) {
            errorMsg = document.createElement('p');
            errorMsg.className = 'text-red-600 text-sm mt-1 error-message';
            errorMsg.textContent = 'Este campo es obligatorio';
            field.parentNode.appendChild(errorMsg);
          }
        } else {
          field.classList.remove('border-red-500');
          const errorMsg = field.parentNode.querySelector('.error-message');
          if (errorMsg) {
            errorMsg.remove();
          }
        }
      });
      
      // Email validation
      const emailFields = form.querySelectorAll('input[type="email"]');
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      
      emailFields.forEach(field => {
        if (field.value.trim() && !emailRegex.test(field.value.trim())) {
          isValid = false;
          field.classList.add('border-red-500');
          
          // Add error message if not exists
          let errorMsg = field.parentNode.querySelector('.error-message');
          if (!errorMsg) {
            errorMsg = document.createElement('p');
            errorMsg.className = 'text-red-600 text-sm mt-1 error-message';
            errorMsg.textContent = 'Por favor ingrese un correo electrónico válido';
            field.parentNode.appendChild(errorMsg);
          } else {
            errorMsg.textContent = 'Por favor ingrese un correo electrónico válido';
          }
        }
      });
      
      if (!isValid) {
        event.preventDefault();
      }
    });
    
    // Live validation on input
    const fields = form.querySelectorAll('input, select, textarea');
    fields.forEach(field => {
      field.addEventListener('input', function() {
        if (field.hasAttribute('required') && !field.value.trim()) {
          field.classList.add('border-red-500');
        } else {
          field.classList.remove('border-red-500');
          const errorMsg = field.parentNode.querySelector('.error-message');
          if (errorMsg) {
            errorMsg.remove();
          }
        }
        
        // Email validation
        if (field.type === 'email' && field.value.trim()) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(field.value.trim())) {
            field.classList.add('border-red-500');
          } else {
            field.classList.remove('border-red-500');
          }
        }
      });
    });
  });
}

/**
 * Initialize responsive navigation
 */
function initResponsiveNav() {
  const navContainer = document.querySelector('nav .container');
  
  if (navContainer) {
    // Handle overflow in navigation
    const checkNavOverflow = () => {
      const navLinks = navContainer.querySelector('.flex');
      
      if (navLinks.scrollWidth > navLinks.clientWidth) {
        navContainer.classList.add('overflow-x-auto');
      } else {
        navContainer.classList.remove('overflow-x-auto');
      }
    };
    
    // Check on load and resize
    checkNavOverflow();
    window.addEventListener('resize', checkNavOverflow);
  }
}

/**
 * Chart initialization helper
 * @param {string} canvasId - The canvas element ID
 * @param {string} type - Chart type (bar, line, pie, etc.)
 * @param {Object} data - Chart data
 * @param {Object} options - Chart options
 * @returns {Chart} - The created chart instance
 */
function createChart(canvasId, type, data, options = {}) {
  const canvas = document.getElementById(canvasId);
  
  if (!canvas) {
    console.error(`Canvas with ID "${canvasId}" not found`);
    return null;
  }
  
  // Set default options for accessibility and aesthetics
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        enabled: true,
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      x: {
        ticks: {
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
          },
        },
      },
      y: {
        ticks: {
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
          },
        },
        beginAtZero: true,
      },
    },
  };
  
  // Merge options
  const mergedOptions = Object.assign({}, defaultOptions, options);
  
  // Create and return chart
  return new Chart(canvas, {
    type: type,
    data: data,
    options: mergedOptions,
  });
}

/**
 * Debounce function to limit execution rate
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} - Debounced function
 */
function debounce(func, wait) {
  let timeout;
  
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Format date for consistent display
 * @param {Date|string} date - Date to format
 * @returns {string} - Formatted date string
 */
function formatDate(date) {
  if (!date) return '';
  
  const d = new Date(date);
  if (isNaN(d.getTime())) return '';
  
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  
  return `${day}/${month}/${year}`;
}

/**
 * Format date time for consistent display
 * @param {Date|string} date - Date to format
 * @returns {string} - Formatted date and time string
 */
function formatDateTime(date) {
  if (!date) return '';
  
  const d = new Date(date);
  if (isNaN(d.getTime())) return '';
  
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  
  return `${day}/${month}/${year} ${hours}:${minutes}`;
}
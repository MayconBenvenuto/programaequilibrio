// Programa Equilíbrio - Belz Conecta Saúde
// Main JavaScript File

// Utilitários globais
const Utils = {
    // Função para salvar dados no localStorage
    saveToStorage: function(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (e) {
            console.error('Erro ao salvar no localStorage:', e);
            return false;
        }
    },

    // Função para carregar dados do localStorage
    loadFromStorage: function(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Erro ao carregar do localStorage:', e);
            return null;
        }
    },

    // Função para formatar CNPJ
    formatCNPJ: function(value) {
        return value
            .replace(/\D/g, '')
            .replace(/(\d{2})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d)/, '$1/$2')
            .replace(/(\d{4})(\d)/, '$1-$2')
            .replace(/(-\d{2})\d+?$/, '$1');
    },

    // Função para validar email
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Função para mostrar notificação
    showNotification: function(message, type = 'info') {
        // Criar elemento de notificação
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            animation: slideInRight 0.5s ease-out;
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remover após 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    },

    // Função para confirmar ação
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    }
};

// Animações e efeitos visuais
const Animations = {
    // Animar contador
    animateCounter: function(element, target, duration = 1000) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    },

    // Fade in elemento
    fadeIn: function(element, duration = 500) {
        element.style.opacity = '0';
        element.style.display = 'block';
        
        let opacity = 0;
        const increment = 1 / (duration / 16);
        
        const timer = setInterval(() => {
            opacity += increment;
            if (opacity >= 1) {
                opacity = 1;
                clearInterval(timer);
            }
            element.style.opacity = opacity;
        }, 16);
    },

    // Slide up elemento
    slideUp: function(element, duration = 500) {
        element.style.transform = 'translateY(30px)';
        element.style.opacity = '0';
        
        let progress = 0;
        const increment = 1 / (duration / 16);
        
        const timer = setInterval(() => {
            progress += increment;
            if (progress >= 1) {
                progress = 1;
                clearInterval(timer);
            }
            
            const translateY = 30 * (1 - progress);
            element.style.transform = `translateY(${translateY}px)`;
            element.style.opacity = progress;
        }, 16);
    }
};

// Validação de formulários
const FormValidation = {
    // Validar formulário de dados da empresa
    validateCompanyForm: function(formData) {
        const errors = [];
        
        if (!formData.razao_social || formData.razao_social.trim().length < 3) {
            errors.push('Razão Social deve ter pelo menos 3 caracteres');
        }
        
        if (!formData.rh_responsavel || formData.rh_responsavel.trim().length < 3) {
            errors.push('Nome do RH Responsável deve ter pelo menos 3 caracteres');
        }
        
        if (formData.email && !Utils.isValidEmail(formData.email)) {
            errors.push('E-mail inválido');
        }
        
        return errors;
    },

    // Mostrar erros de validação
    showValidationErrors: function(errors) {
        let message = 'Por favor, corrija os seguintes erros:\n';
        errors.forEach(error => {
            message += `• ${error}\n`;
        });
        
        Utils.showNotification(message.replace(/\n/g, '<br>'), 'danger');
    }
};

// Sistema de tracking/analytics simples
const Analytics = {
    // Track evento
    trackEvent: function(category, action, label = null) {
        const event = {
            category: category,
            action: action,
            label: label,
            timestamp: new Date().toISOString(),
            page: window.location.pathname
        };
        
        // Salvar no localStorage para análise posterior
        const events = Utils.loadFromStorage('analytics_events') || [];
        events.push(event);
        
        // Manter apenas os últimos 100 eventos
        if (events.length > 100) {
            events.splice(0, events.length - 100);
        }
        
        Utils.saveToStorage('analytics_events', events);
        
        console.log('Event tracked:', event);
    },

    // Get analytics data
    getAnalytics: function() {
        return Utils.loadFromStorage('analytics_events') || [];
    }
};

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('Programa Equilíbrio - Sistema inicializado');
    
    // Track page view
    Analytics.trackEvent('pageview', 'load', window.location.pathname);
    
    // Aplicar formatação automática em campos CNPJ
    const cnpjInputs = document.querySelectorAll('input[name="cnpj"]');
    cnpjInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = Utils.formatCNPJ(e.target.value);
        });
    });
    
    // Adicionar tooltips Bootstrap em elementos com data-bs-toggle="tooltip"
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Smooth scrolling para links internos
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Adicionar classe de animação aos cards quando visíveis
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const cardObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-up');
            }
        });
    }, observerOptions);
    
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        cardObserver.observe(card);
    });
});

// Função para debug (apenas em desenvolvimento)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.ProgramaEquilibrio = {
        Utils: Utils,
        Animations: Animations,
        FormValidation: FormValidation,
        Analytics: Analytics
    };
    
    console.log('Debug mode enabled. Access via window.ProgramaEquilibrio');
}

// Service Worker registration (para futuras funcionalidades PWA)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Registrar service worker quando disponível
        // navigator.serviceWorker.register('/sw.js');
    });
}

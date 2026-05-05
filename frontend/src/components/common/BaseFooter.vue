<template>
  <footer class="footer" role="contentinfo" aria-label="Application footer">
    <div class="footer-content">
      <div class="footer-section">
        <div class="footer-brand">
          <div class="brand-info">
            <span class="powered-by">{{ $t('footer.powered_by') }}</span>
            <span class="footer-brand-link">Istinye University Software Project Management Students</span>
          </div>
        </div>
      </div>

      <div class="footer-section">
        <div class="footer-info">
          <span class="version">v{{ version }}</span>
          <span class="separator">•</span>
          <span class="copyright">{{ $t('footer.copyright', { year: currentYear }) }}</span>
        </div>
      </div>

      <div class="footer-section">
        <div class="footer-links">
          <span class="footer-link">Industry Maintenance Platform</span>
          <span class="separator">•</span>
          <span class="footer-link">{{ $t('footer.report_bug') }}</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { appConfig } from '@/config/app'

// Utilizziamo la versione dalla configurazione
const version = appConfig.version

// Anno corrente per il copyright
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  width: 100%;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  padding: 1rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: center;
}

.footer-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.footer-brand-logo {
  height: 24px;
  width: auto;
}

.brand-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.powered-by {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 400;
}

.footer-brand-link {
  color: #1976d2;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.8rem;
  transition: color 0.2s ease;
}

.footer-brand-link:hover {
  color: #0d47a1;
}

.footer-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.version {
  font-size: 0.7rem;
  color: #6c757d;
  font-weight: 400;
}

.copyright {
  font-size: 0.7rem;
  color: #6c757d;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.footer-link {
  color: #6c757d;
  text-decoration: none;
  font-size: 0.7rem;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: #495057;
}

.separator {
  color: #adb5bd;
  font-size: 0.7rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .footer-content {
    padding: 0 1rem;
    gap: 0.5rem;
  }
  
  .footer-brand {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .brand-info {
    flex-direction: row;
    gap: 0.25rem;
  }
  
  .footer-info,
  .footer-links {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .separator {
    display: none;
  }
}

@media (max-width: 480px) {
  .footer {
    padding: 0.75rem 0;
  }
  
  .footer-brand-logo {
    height: 20px;
  }
  
  .powered-by,
  .footer-brand-link {
    font-size: 0.75rem;
  }
}
</style> 
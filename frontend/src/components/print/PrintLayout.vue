<template>
  <div class="print-layout" :class="layoutClass">
    <!-- Print header -->
    <div v-if="options.includeHeader" class="print-header">
      <div class="header-content">
        <div class="header-left">
          <img v-if="logo" :src="logo" alt="Logo" class="header-logo" />
          <h1 class="header-title">{{ options.headerText || 'Industry Maintenance Platform' }}</h1>
        </div>
        <div class="header-right">
          <div class="header-meta">
            <span class="meta-item">{{ formatDate(new Date()) }}</span>
            <span v-if="pageInfo" class="meta-item">Page {{ pageInfo.current }} of {{ pageInfo.total }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="print-content">
      <slot />
    </div>

    <!-- Print footer -->
    <div v-if="options.includeFooter" class="print-footer">
      <div class="footer-content">
        <div class="footer-left">
          <span class="footer-text">{{ formatFooterText(options.footerText) }}</span>
        </div>
        <div class="footer-right">
          <span class="footer-qr" v-if="qrCode">
            <img :src="qrCode" alt="QR Code" class="qr-image" />
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import i18n from '../../locales/loader-final.js'

const props = defineProps({
  options: {
    type: Object,
    default: () => ({
      orientation: 'portrait',
      paperSize: 'a4',
      margin: 'normal',
      includeHeader: true,
      includeFooter: true,
      headerText: 'Industry Maintenance Platform',
      footerText: 'Generated on {{date}}'
    })
  },
  pageInfo: {
    type: Object,
    default: null
  },
  logo: {
    type: String,
    default: null
  },
  qrCode: {
    type: String,
    default: null
  }
})

const layoutClass = computed(() => ({
  [`orientation-${props.options.orientation}`]: true,
  [`paper-${props.options.paperSize}`]: true,
  [`margin-${props.options.margin}`]: true
}))

const formatDate = (date) => {
  const locale = i18n.global.locale.value;
  const dateLocale = locale === 'it' ? 'it-IT' : 'en-US';
  return date.toLocaleDateString(dateLocale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatFooterText = (text) => {
  if (!text) return ''
  
  return text
    .replace('{{date}}', formatDate(new Date()))
    .replace('{{page}}', props.pageInfo?.current || '1')
    .replace('{{total}}', props.pageInfo?.total || '1')
}
</script>

<style scoped>
/* Base print styles */
.print-layout {
  background: white;
  color: black;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.4;
  page-break-inside: avoid;
}

/* Orientations */
.orientation-portrait {
  width: 210mm;
  min-height: 297mm;
}

.orientation-landscape {
  width: 297mm;
  min-height: 210mm;
}

/* Paper sizes */
.paper-a4 {
  width: 210mm;
  min-height: 297mm;
}

.paper-a3 {
  width: 297mm;
  min-height: 420mm;
}

.paper-letter {
  width: 8.5in;
  min-height: 11in;
}

/* Margins */
.margin-normal {
  padding: 20mm;
}

.margin-narrow {
  padding: 10mm;
}

.margin-wide {
  padding: 30mm;
}

/* Header */
.print-header {
  border-bottom: 2px solid #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-logo {
  height: 40px;
  width: auto;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.header-right {
  text-align: right;
}

.header-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.meta-item {
  font-size: 12px;
  color: #666;
}

/* Content */
.print-content {
  flex: 1;
  min-height: 200mm;
}

/* Footer */
.print-footer {
  border-top: 1px solid #ccc;
  margin-top: 20px;
  padding-top: 10px;
  font-size: 10px;
  color: #666;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  font-size: 10px;
}

.footer-qr {
  display: flex;
  align-items: center;
}

.qr-image {
  width: 30px;
  height: 30px;
}

/* Print styles */
@media print {
  .print-layout {
    margin: 0;
    padding: 0;
    box-shadow: none;
    background: white;
  }
  
  .print-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: white;
    z-index: 1000;
  }
  
  .print-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    z-index: 1000;
  }
  
  .print-content {
    margin-top: 60px;
    margin-bottom: 40px;
  }
  
  /* Hide elements not needed for printing */
  .no-print {
    display: none !important;
  }
  
  /* Force page break */
  .page-break {
    page-break-before: always;
  }
  
  /* Avoid page break */
  .no-break {
    page-break-inside: avoid;
  }
}

/* Preview styles */
@media screen {
  .print-layout {
    border: 1px solid #ddd;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 20px auto;
  }
}
</style> 
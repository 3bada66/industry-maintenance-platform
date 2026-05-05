export const appConfig = {
  version: '1.0.0',

  name: 'Industry Maintenance Platform',

  description: 'Industrial Asset, Risk, Management & Technical Monitoring Platform',

  copyright: {
    company: 'Obada Kharaz & Team',
    year: '2026',
    url: ''
  },

  links: {
    website: '',
    github: '',
    issues: '',
    license: ''
  },

  api: {
    baseUrl: '/api',
    timeout: 30000
  },

  pagination: {
    defaultPageSize: 25,
    pageSizeOptions: [10, 25, 50, 100]
  },

  upload: {
    maxFileSize: 10 * 1024 * 1024,
    allowedTypes: ['image/*', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  }
}

export default appConfig

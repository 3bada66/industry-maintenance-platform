import { createI18n } from 'vue-i18n'

import enCommon from './en/common.json'
import enMenu from './en/menu.json'
import enDashboard from './en/dashboard.json'
import enAssets from './en/assets.json'
import enAssetTypes from './en/assettypes.json'
import enAssetStatuses from './en/assetstatuses.json'
import enContacts from './en/contacts.json'
import enFooter from './en/footer.json'
import enLogin from './en/login.json'
import enManufacturers from './en/manufacturers.json'
import enSuppliers from './en/suppliers.json'
import enSites from './en/sites.json'
import enAreas from './en/areas.json'
import enLocations from './en/locations.json'
import enPcap from './en/pcap.json'
import enSetup from './en/setup.json'
import enAuditlog from './en/auditlog.json'
import enProfile from './en/profile.json'
import enNetworkmap from './en/networkMap.json'
import enPrint from './en/print.json'
import enRoles from './en/roles.json'
import enUsers from './en/users.json'
import enGlobalsearch from './en/globalsearch.json'

const flattenObject = (obj, prefix = '') => {
  const flattened = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const newKey = prefix ? `${prefix}.${key}` : key
      if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
        Object.assign(flattened, flattenObject(obj[key], newKey))
      } else {
        flattened[newKey] = obj[key]
      }
    }
  }
  return flattened
}

const messages = {
  en: flattenObject({
    common: enCommon,
    dashboard: enDashboard,
    assets: enAssets,
    assettypes: enAssetTypes,
    assetstatuses: enAssetStatuses,
    contacts: enContacts,
    footer: enFooter,
    menu: enMenu,
    login: enLogin,
    manufacturers: enManufacturers,
    suppliers: enSuppliers,
    sites: enSites,
    areas: enAreas,
    locations: enLocations,
    pcap: enPcap,
    setup: enSetup,
    auditlog: enAuditlog,
    profile: enProfile,
    networkmap: enNetworkmap,
    print: enPrint,
    roles: enRoles,
    users: enUsers,
    globalsearch: enGlobalsearch
  })
}

const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages,
  legacy: false,
  globalInjection: true,
  silentTranslationWarn: true,
  silentFallbackWarn: true,
  missingWarn: false,
  fallbackWarn: false
})

export function setLanguage() { return false }

export default i18n

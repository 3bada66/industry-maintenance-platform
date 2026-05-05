import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'

export function usePermissions() {
  const authStore = useAuthStore()

  // Ottieni i permessi effettivi dell'utente corrente (inclusa ereditarietà)
  const userPermissions = computed(() => {
    const user = authStore.user
    const permissions = user?.role?.effective_permissions || user?.role?.permissions || {}
    return permissions
  })

  // Ottieni i permessi diretti (senza ereditarietà)
  const directPermissions = computed(() => {
    const user = authStore.user
    return user?.role?.permissions || {}
  })

  // Controlla se l'utente ha un livello minimo di permesso per una sezione
  const hasPermission = (section, minLevel = 1) => {
    const userLevel = userPermissions.value[section] || 0
    return userLevel >= minLevel
  }

  // Controlla se l'utente può leggere una sezione
  const canRead = (section) => hasPermission(section, 1)

  // Controlla se l'utente può scrivere una sezione
  const canWrite = (section) => hasPermission(section, 2)

  // Controlla se l'utente può eliminare una sezione
  const canDelete = (section) => hasPermission(section, 3)

  // Controlla se l'utente può fare operazioni massive
  const canBulkOperate = (section) => hasPermission(section, 4)

  // Controlla se l'utente è admin (ha tutti i permessi)
  const isAdmin = computed(() => {
    const user = authStore.user
    return user?.role?.name === 'admin'
  })

  // Ottieni il livello di permesso per una sezione
  const getPermissionLevel = (section) => {
    return userPermissions.value[section] || 0
  }

  // Ottieni il livello di permesso diretto (senza ereditarietà)
  const getDirectPermissionLevel = (section) => {
    return directPermissions.value[section] || 0
  }

  // Ottieni tutte le sezioni per cui l'utente ha almeno permesso di lettura
  const accessibleSections = computed(() => {
    const sections = []
    for (const [section, level] of Object.entries(userPermissions.value)) {
      if (level >= 1) {
        sections.push(section)
      }
    }
    return sections
  })

  // Verifica se un permesso è ereditato
  const isInheritedPermission = (section) => {
    const directLevel = getDirectPermissionLevel(section)
    const effectiveLevel = getPermissionLevel(section)
    return effectiveLevel > directLevel
  }

  // Ottieni informazioni dettagliate sui permessi
  const getPermissionInfo = (section) => {
    const directLevel = getDirectPermissionLevel(section)
    const effectiveLevel = getPermissionLevel(section)
    const inherited = isInheritedPermission(section)
    
    return {
      section,
      directLevel,
      effectiveLevel,
      inherited,
      canRead: effectiveLevel >= 1,
      canWrite: effectiveLevel >= 2,
      canDelete: effectiveLevel >= 3,
      canBulkOperate: effectiveLevel >= 4
    }
  }

  // Ottieni tutti i permessi con informazioni dettagliate
  const allPermissionsInfo = computed(() => {
    const allSections = [
      'users', 'roles', 'assets', 'locations', 'sites', 'areas',
      'suppliers', 'manufacturers', 'contacts', 'audit_logs'
    ]
    
    return allSections.map(section => getPermissionInfo(section))
  })

  // Forza il refresh dei permessi dell'utente
  const refreshUserPermissions = async () => {
    try {
      await authStore.fetchUser()
      console.log('🔄 Permessi utente aggiornati:', userPermissions.value)
    } catch (error) {
      console.error('❌ Errore durante l\'aggiornamento dei permessi:', error)
    }
  }

  // Verifica se l'utente può gestire i permessi
  const canManagePermissions = computed(() => {
    return canWrite('roles') || isAdmin.value
  })

  // Verifica se l'utente può gestire gli utenti
  const canManageUsers = computed(() => {
    return canWrite('users') || isAdmin.value
  })

  return {
    userPermissions,
    directPermissions,
    hasPermission,
    canRead,
    canWrite,
    canDelete,
    canBulkOperate,
    isAdmin,
    getPermissionLevel,
    getDirectPermissionLevel,
    accessibleSections,
    isInheritedPermission,
    getPermissionInfo,
    allPermissionsInfo,
    canManagePermissions,
    canManageUsers,
    refreshUserPermissions
  }
} 
// auth.js
// Store per la gestione dell'autenticazione
// Utilizza defineStore per creare lo store
// Utilizza ref per creare le variabili reactive
// Utilizza router per navigare tra le pagine
// Utilizza api per effettuare le richieste all'API
// Utilizza pinia-plugin-persistedstate per salvare lo stato nel localStorage

import { defineStore } from 'pinia'
import { ref } from 'vue'
import router from '../router'
import api from '../api/api'

export const useAuthStore = defineStore('auth', () => {

let refreshIntervalId = null
let lastActivity = Date.now()
const activityHandler = () => { lastActivity = Date.now() }
let activityListenersAttached = false

function setupActivityListeners() {
  if (activityListenersAttached) return
  ;['click', 'mousemove', 'keydown'].forEach(event => {
    window.addEventListener(event, activityHandler)
  })
  activityListenersAttached = true
}

function removeActivityListeners() {
  ;['click', 'mousemove', 'keydown'].forEach(event => {
    window.removeEventListener(event, activityHandler)
  })
  activityListenersAttached = false
}

function startTokenRefresh(intervalMinutes = 5) {
  if (refreshIntervalId !== null) return // già avviato

  setupActivityListeners()
  refreshIntervalId = setInterval(async () => {
    const minutesSinceLastActivity = (Date.now() - lastActivity) / 1000 / 60
    if (!isAuthenticated.value || minutesSinceLastActivity > 10) return

    try {
      await api.refresh()
          //console.log('[AUTH] Token refresh eseguito')
  } catch (err) {
    // console.log(err)
    console.warn('[AUTH] Token refresh fallito')
      logout()
    }
  }, intervalMinutes * 60 * 1000)
}

function stopTokenRefresh() {
  if (refreshIntervalId !== null) {
    clearInterval(refreshIntervalId)
    refreshIntervalId = null
  }
}


  const user = ref(null)
  const isAuthenticated = ref(false)

async function login(email, password) {
  try {
    await api.login(email, password)
    await fetchUser()
    isAuthenticated.value = true
    startTokenRefresh()
    router.push('/')
  } catch (error) {
    throw error
  }
}

  async function fetchUser() {
    try {
      const response = await api.getCurrentUser()
      user.value = response.data
      isAuthenticated.value = true
    } catch (error) {
      logout()
    }
  }

async function logout() {
  try {
    await api.logout()
  } catch (e) {
    // continue with local logout even if API call fails
  }
  user.value = null
  isAuthenticated.value = false
  stopTokenRefresh()
  removeActivityListeners()
  router.push('/login')
}
  return { user, isAuthenticated, login, logout, fetchUser,startTokenRefresh,stopTokenRefresh }
}, {
  persist: true   
}
)

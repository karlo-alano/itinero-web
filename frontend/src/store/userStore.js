import { defineStore } from 'pinia'
import { supabase } from '@/lib/supabase'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const profile = ref(null)
  const loading = ref(false)

  // Initialize auth state
  const initializeAuth = async () => {
    try {
      const { data: { session }, error } = await supabase.auth.getSession()
      if (session?.user && !error) {
        user.value = session.user
        await loadProfile(session.user.id)
      }
    } catch (error) {
      console.error('Error initializing auth:', error)
    }
  }

  // Load user profile from custom users table
  const loadProfile = async (userId) => {
    try {
      const { data, error } = await supabase
        .from('users')
        .select('*')
        .eq('id', userId)
        .single()

      if (error && error.code !== 'PGRST116') { // PGRST116 = no rows returned
        console.error('Error loading profile:', error)
        return
      }

      profile.value = data || null
    } catch (error) {
      console.error('Error loading profile:', error)
    }
  }

  // Sign up - creates auth user + profile in users table
  const signUp = async (email, password, username) => {
    loading.value = true
    try {
      // Create auth user
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email,
        password
      })

      if (authError) throw authError

      // Create profile in users table
      const { data: profileData, error: profileError } = await supabase
        .from('users')
        .insert([{
          id: authData.user.id,
          user_name: username,
          email: email
        }])
        .select()
        .single()

      if (profileError) throw profileError

      user.value = authData.user
      profile.value = profileData

      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  // Sign in - loads existing user
  const signIn = async (email, password) => {
    loading.value = true
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      })

      if (error) throw error

      user.value = data.user
      await loadProfile(data.user.id)

      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  // Sign out
  const signOut = async () => {
    try {
      await supabase.auth.signOut()
      user.value = null
      profile.value = null
    } catch (error) {
      console.error('Error signing out:', error)
    }
  }

  // Update profile
  const updateProfile = async (updates) => {
    if (!user.value || !profile.value) return { success: false, error: 'Not authenticated' }

    try {
      const { data, error } = await supabase
        .from('users')
        .update(updates)
        .eq('id', user.value.id)
        .select()
        .single()

      if (error) throw error

      profile.value = data
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  // Listen for auth state changes
  supabase.auth.onAuthStateChange(async (event, session) => {
    console.log('Auth state changed:', event, session?.user?.email)

    user.value = session?.user ?? null

    if (session?.user) {
      await loadProfile(session.user.id)
    } else {
      profile.value = null
    }
  })

  return {
    // State
    user,
    profile,
    loading,

    // Methods
    initializeAuth,
    signUp,
    signIn,
    signOut,
    updateProfile
  }
})

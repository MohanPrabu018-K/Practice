import { create } from 'zustand'

export const useAuth = create((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('token') || null,
  login: (tkn, usr) => {
    localStorage.setItem('token', tkn)
    localStorage.setItem('user', JSON.stringify(usr))
    set({ user: usr, token: tkn })
  },
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    set({ user: null, token: null })
  },
}))

export const useTheme = create((set) => ({
  dark: localStorage.getItem('theme') !== 'light',
  toggle: () => set(s => {
    const next = !s.dark
    localStorage.setItem('theme', next ? 'dark' : 'light')
    return { dark: next }
  }),
}))

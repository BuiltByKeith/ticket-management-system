import { useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import { login, logout } from '../api/authApi'

const useAuth = () => {
  const { setAuth, clearAuth, user } = useAuthStore()
  const navigate = useNavigate()

  const handleLogin = async (credentials) => {
    const response = await login(credentials)
    const { user, tokens } = response.data.data

    setAuth(user, tokens.access, tokens.refresh)

    if (user.role === 'admin') {
      navigate('/admin')
    } else if (user.role === 'developer') {
      navigate('/developer')
    } else {
      navigate('/login')
    }
  }

  const handleLogout = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token')
      await logout(refresh)
    } finally {
      // Use finally so this always runs whether logout API succeeds or fails
      clearAuth()
      navigate('/login')
    }
  }

  return { handleLogin, handleLogout, user }
}

export default useAuth
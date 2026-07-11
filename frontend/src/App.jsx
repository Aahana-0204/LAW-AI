import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Navbar from './components/layout/Navbar'
import { AuthProvider } from './context/AuthContext'
import ChatPage from './pages/ChatPage'
import ExpertsPage from './pages/ExpertsPage'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import UploadPage from './pages/UploadPage'
import GeneratePage from './pages/GeneratePage'

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen">
          <Navbar />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/experts" element={<ExpertsPage />} />
            <Route path="/documents" element={<UploadPage />} />
            <Route path="/generate" element={<GeneratePage />} />
          </Routes>
        </div>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: '#1a1a28',
              color: '#f3f4f6',
              border: '1px solid #2a2a45',
            },
            success: {
              iconTheme: { primary: '#f59e0b', secondary: '#1a1a28' },
            },
          }}
        />
      </Router>
    </AuthProvider>
  )
}

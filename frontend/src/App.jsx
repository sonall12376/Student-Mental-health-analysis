import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Brain, LogOut, ClipboardList, History as HistoryIcon, User } from 'lucide-react';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import AssessmentForm from './pages/AssessmentForm';
import Results from './pages/Results';
import History from './pages/History';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [studentName, setStudentName] = useState('');

  // Check login state on component mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const name = localStorage.getItem('name');
    if (token) {
      setIsLoggedIn(true);
      setStudentName(name || '');
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    localStorage.removeItem('name');
    localStorage.removeItem('last_result');
    localStorage.removeItem('last_assessment_input');
    setIsLoggedIn(false);
    setStudentName('');
    window.location.href = '/';
  };

  return (
    <Router>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-brand-500 selection:text-white">
        
        {/* Navigation Navbar */}
        <header className="w-full bg-slate-950/80 border-b border-slate-900/60 sticky top-0 backdrop-blur-md z-50">
          <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2.5 hover:opacity-90 transition-opacity">
              <div className="bg-gradient-to-tr from-brand-600 to-brand-400 p-2 rounded-xl shadow-lg shadow-brand-500/10">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold tracking-tight bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent font-sans">
                MindEase
              </span>
            </Link>

            {/* Menu Links */}
            <nav className="flex items-center gap-6">
              {isLoggedIn ? (
                <>
                  <Link to="/assessment" className="text-sm font-medium text-slate-400 hover:text-white transition-colors flex items-center gap-1.5">
                    <ClipboardList className="w-4 h-4" />
                    <span className="hidden sm:inline">Take Test</span>
                  </Link>
                  <Link to="/history" className="text-sm font-medium text-slate-400 hover:text-white transition-colors flex items-center gap-1.5">
                    <HistoryIcon className="w-4 h-4" />
                    <span className="hidden sm:inline">History</span>
                  </Link>
                  
                  <div className="h-4 w-px bg-slate-800" />
                  
                  {/* Student Badge & Logout */}
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-semibold px-3 py-1 bg-slate-900 border border-slate-800 rounded-full flex items-center gap-1.5 text-slate-300">
                      <User className="w-3.5 h-3.5 text-brand-400" />
                      {studentName.split(' ')[0]}
                    </span>
                    <button
                      onClick={handleLogout}
                      className="p-1.5 rounded-xl border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-rose-400 bg-slate-950/40 transition-colors"
                      title="Log Out"
                    >
                      <LogOut className="w-4 h-4" />
                    </button>
                  </div>
                </>
              ) : (
                <div className="flex items-center gap-4">
                  <Link to="/login" className="text-sm font-medium text-slate-400 hover:text-white transition-colors">
                    Sign In
                  </Link>
                  <Link 
                    to="/register" 
                    className="px-4 py-2 text-xs font-semibold rounded-lg bg-gradient-to-tr from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white shadow-md shadow-brand-500/10 transition-all hover:-translate-y-0.5"
                  >
                    Register
                  </Link>
                </div>
              )}
            </nav>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-grow flex flex-col justify-center">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected Routes (simplified checks inside pages or via check fallback) */}
            <Route path="/assessment" element={<AssessmentForm />} />
            <Route path="/results" element={<Results />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>

        {/* Global Footer */}
        <footer className="w-full bg-slate-950 border-t border-slate-900/60 py-6 text-center text-[10px] sm:text-xs text-slate-500">
          <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-3">
            <span>© {new Date().getFullYear()} MindEase Project. Built with React + FastAPI + XGBoost.</span>
            <div className="flex gap-4">
              <span>Explainable AI (SHAP)</span>
              <span>Secure JWT Auth</span>
              <span>Atlas Support</span>
            </div>
          </div>
        </footer>

      </div>
    </Router>
  );
}

export default App;

import React, { useState } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import API from '../services/api';
import { Lock, User, AlertCircle } from 'lucide-react';

function Login() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const tokenExpired = searchParams.get('expired') === 'true';

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await API.post('/auth/login', {
        username,
        password,
      });

      // Save token and student details in storage
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('username', response.data.username);
      localStorage.setItem('name', response.data.name);

      // Force page reload to update main Navbar context, and redirect
      window.location.href = '/assessment';
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Login failed. Please check your credentials or backend server status.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-grow flex items-center justify-center py-12 px-4 relative">
      <div className="absolute top-1/4 left-1/3 w-[300px] h-[300px] rounded-full bg-brand-500/5 blur-[100px] pointer-events-none" />

      <div className="w-full max-w-md p-8 rounded-2xl bg-slate-900/40 border border-slate-900 backdrop-blur-md z-10 shadow-xl">
        <h2 className="text-3xl font-bold text-center mb-2 tracking-tight">Welcome Back</h2>
        <p className="text-slate-400 text-center text-sm mb-8">Sign in to assess your well-being</p>

        {tokenExpired && (
          <div className="mb-6 p-4 bg-amber-500/10 border border-amber-500/20 text-amber-400 text-sm rounded-xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>Session expired. Please sign in again.</span>
          </div>
        )}

        {error && (
          <div className="mb-6 p-4 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm rounded-xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Username
            </label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-500">
                <User className="w-4 h-4" />
              </span>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 placeholder-slate-600 focus:outline-none transition-colors text-sm"
                placeholder="Enter username"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Password
            </label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-500">
                <Lock className="w-4 h-4" />
              </span>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 placeholder-slate-600 focus:outline-none transition-colors text-sm"
                placeholder="Enter password"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white font-medium shadow-lg shadow-brand-500/15 hover:shadow-brand-500/25 transition-all disabled:opacity-50 text-sm flex items-center justify-center"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="mt-8 text-center text-xs text-slate-500">
          Don't have an account?{' '}
          <Link to="/register" className="text-brand-400 hover:text-brand-300 font-medium transition-colors">
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Login;

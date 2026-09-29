import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, Sparkles, HeartHandshake, Eye, ArrowRight, ShieldCheck } from 'lucide-react';

function Home() {
  const isLoggedIn = !!localStorage.getItem('access_token');
  const studentName = localStorage.getItem('name') || '';

  return (
    <div className="flex-1 flex flex-col items-center justify-center py-12 px-4 relative">
      
      {/* Background glowing gradients */}
      <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full bg-brand-500/10 blur-[150px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] rounded-full bg-emerald-500/5 blur-[150px] pointer-events-none" />

      {/* Hero Header */}
      <div className="text-center max-w-3xl z-10 flex flex-col items-center mb-16">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs font-medium text-slate-300 mb-6 hover:border-slate-700 transition-colors">
          <Sparkles className="w-3.5 h-3.5 text-brand-400" />
          <span>Explainable AI-Based Student Support</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-6 leading-tight">
          Your Mental Well-being, <br />
          <span className="bg-gradient-to-r from-brand-400 via-violet-400 to-emerald-400 bg-clip-text text-transparent">
            Demystified by AI
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-400 max-w-xl mb-8 leading-relaxed">
          MindEase helps you assess your depression risk, provides transparent visual explanations of your personal risk drivers, and delivers targeted mental health support recommendations.
        </p>

        {isLoggedIn ? (
          <div className="flex flex-col items-center gap-4">
            <p className="text-sm text-slate-300">Welcome back, <span className="font-semibold text-brand-400">{studentName}</span>!</p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Link
                to="/assessment"
                className="px-6 py-3 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white font-medium shadow-lg shadow-brand-500/20 hover:shadow-brand-500/30 transition-all transform hover:-translate-y-0.5 flex items-center gap-2"
              >
                Take Assessment <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/history"
                className="px-6 py-3 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 hover:border-slate-700 text-slate-200 font-medium transition-all transform hover:-translate-y-0.5"
              >
                View History
              </Link>
            </div>
          </div>
        ) : (
          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              to="/register"
              className="px-6 py-3 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white font-medium shadow-lg shadow-brand-500/20 hover:shadow-brand-500/30 transition-all transform hover:-translate-y-0.5 flex items-center gap-2"
            >
              Get Started <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/login"
              className="px-6 py-3 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 hover:border-slate-700 text-slate-300 font-medium transition-all transform hover:-translate-y-0.5"
            >
              Sign In
            </Link>
          </div>
        )}
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl text-left z-10">
        {/* Card 1 */}
        <div className="p-6 rounded-2xl bg-slate-900/30 border border-slate-900 backdrop-blur-md hover:border-slate-800 transition-all duration-350">
          <div className="w-10 h-10 rounded-xl bg-brand-500/10 flex items-center justify-center border border-brand-500/20 mb-4">
            <Brain className="w-5 h-5 text-brand-400" />
          </div>
          <h3 className="text-base font-semibold text-white mb-2">Depression Risk Prediction</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Provide key data on academic load, sleeping patterns, financial concerns, and lifestyle habits to predict mental health vulnerability.
          </p>
        </div>

        {/* Card 2 */}
        <div className="p-6 rounded-2xl bg-slate-900/30 border border-slate-900 backdrop-blur-md hover:border-slate-800 transition-all duration-350">
          <div className="w-10 h-10 rounded-xl bg-violet-500/10 flex items-center justify-center border border-violet-500/20 mb-4">
            <Eye className="w-5 h-5 text-violet-400" />
          </div>
          <h3 className="text-base font-semibold text-white mb-2">SHAP Explanations</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            See *why* the prediction was made. Understand exactly which daily habits are driving your stress and which are protecting your wellness.
          </p>
        </div>

        {/* Card 3 */}
        <div className="p-6 rounded-2xl bg-slate-900/30 border border-slate-900 backdrop-blur-md hover:border-slate-800 transition-all duration-350">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center border border-emerald-500/20 mb-4">
            <HeartHandshake className="w-5 h-5 text-emerald-400" />
          </div>
          <h3 className="text-base font-semibold text-white mb-2">Tailored Wellness Support</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Receive actionable, rule-based lifestyle and academic recommendations tailored to address your specific stress indicators.
          </p>
        </div>
      </div>

    </div>
  );
}

export default Home;

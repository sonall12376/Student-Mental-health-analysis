import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { CheckCircle, AlertTriangle, ShieldCheck, RefreshCw, BarChart2, HeartHandshake } from 'lucide-react';

function Results() {
  const navigate = useNavigate();
  
  // Retrieve the calculation result from localStorage
  const resultData = localStorage.getItem('last_result');
  if (!resultData) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
        <AlertTriangle className="w-12 h-12 text-amber-500 mb-4" />
        <h3 className="text-xl font-bold mb-2">No Results Found</h3>
        <p className="text-slate-400 max-w-sm mb-6">Please complete the depression assessment form first.</p>
        <Link to="/assessment" className="px-5 py-2.5 bg-brand-600 hover:bg-brand-500 rounded-xl text-white font-medium transition-colors">
          Go to Assessment
        </Link>
      </div>
    );
  }

  const {
    depression_probability,
    risk_level,
    top_factors,
    recommendations,
    timestamp
  } = JSON.parse(resultData);

  const probabilityPct = Math.round(depression_probability * 100);

  // Styling based on risk level
  const getRiskStyles = () => {
    switch (risk_level) {
      case 'High':
        return {
          bg: 'bg-rose-500/10 border-rose-500/20',
          text: 'text-rose-400',
          indicator: 'bg-rose-500',
          badge: 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
        };
      case 'Moderate':
        return {
          bg: 'bg-amber-500/10 border-amber-500/20',
          text: 'text-amber-400',
          indicator: 'bg-amber-500',
          badge: 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
        };
      default:
        return {
          bg: 'bg-emerald-500/10 border-emerald-500/20',
          text: 'text-emerald-400',
          indicator: 'bg-emerald-500',
          badge: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
        };
    }
  };

  const riskStyle = getRiskStyles();

  return (
    <div className="flex-grow py-12 px-4 relative max-w-5xl mx-auto w-full">
      <div className="absolute top-1/4 right-5 w-[300px] h-[300px] rounded-full bg-brand-500/5 blur-[100px] pointer-events-none" />

      {/* Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 z-10 relative">
        
        {/* Left Column: Risk Card */}
        <div className="md:col-span-1 flex flex-col gap-6">
          
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-900 backdrop-blur-md shadow-xl flex flex-col items-center text-center">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-6">Risk Assessment Output</h3>
            
            {/* Probability Gauge Circle */}
            <div className="relative w-40 h-40 flex items-center justify-center mb-6">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  className="stroke-slate-950 fill-none"
                  strokeWidth="8"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  className={`fill-none transition-all duration-1000 ease-out`}
                  stroke={risk_level === 'High' ? '#f43f5e' : risk_level === 'Moderate' ? '#f59e0b' : '#10b981'}
                  strokeWidth="8"
                  strokeDasharray="264"
                  strokeDashoffset={264 - (264 * probabilityPct) / 100}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-3xl font-extrabold text-white">{probabilityPct}%</span>
                <span className="text-slate-500 text-xs mt-0.5">Depression Score</span>
              </div>
            </div>

            <div className="space-y-4 w-full">
              <div className="flex justify-between items-center px-4 py-2.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-xs text-slate-400 font-semibold">Vulnerability Rating:</span>
                <span className={`text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider ${riskStyle.badge}`}>
                  {risk_level} Risk
                </span>
              </div>

              <div className="text-xs text-slate-500 italic mt-4">
                Assessed: {new Date(timestamp).toLocaleString()}
              </div>
            </div>
            
            <button
              onClick={() => navigate('/assessment')}
              className="mt-8 w-full py-3 bg-slate-950 border border-slate-800 hover:border-slate-700 hover:bg-slate-900 rounded-xl text-slate-200 text-sm font-semibold transition-all flex items-center justify-center gap-2"
            >
              <RefreshCw className="w-4 h-4" /> Retake Test
            </button>
          </div>
        </div>

        {/* Right Columns: SHAP factors & Recommendations */}
        <div className="md:col-span-2 flex flex-col gap-6">
          
          {/* SHAP Explanation Card */}
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-900 backdrop-blur-md shadow-xl">
            <div className="flex items-center gap-2 mb-6">
              <BarChart2 className="w-5 h-5 text-violet-400" />
              <h3 className="text-lg font-bold text-white">Why the model predicted this</h3>
            </div>

            <p className="text-slate-400 text-sm mb-6 leading-relaxed">
              These are the top 5 lifestyle, academic, and clinical factors that contributed to your risk score. 
              <span className="text-rose-400 font-semibold"> Red indicators</span> show risk drivers (factors increasing risk). 
              <span className="text-emerald-400 font-semibold"> Green indicators</span> show protective factors (buffers reducing risk).
            </p>

            <div className="space-y-5">
              {top_factors.map((factor) => {
                const isRisk = factor.shap_value > 0;
                // Normalize SHAP value for display width (typically values range between -2 and 2 log odds)
                const magnitude = Math.min(Math.max((Math.abs(factor.shap_value) / 1.5) * 100, 10), 100);

                return (
                  <div key={factor.feature} className="p-4 rounded-xl bg-slate-950/60 border border-slate-850">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs font-bold text-slate-300">
                        {factor.feature.replace(/Degree_/, 'Program: ')}
                      </span>
                      <span className={`text-xs font-semibold ${isRisk ? 'text-rose-400' : 'text-emerald-400'}`}>
                        {isRisk ? '+' : ''}{factor.shap_value.toFixed(2)} SHAP
                      </span>
                    </div>

                    {/* Progress Bar */}
                    <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden mb-3 relative">
                      <div
                        className={`h-full rounded-full transition-all duration-1000 ${
                          isRisk
                            ? 'bg-gradient-to-r from-rose-600 to-rose-400'
                            : 'bg-gradient-to-r from-emerald-600 to-emerald-400'
                        }`}
                        style={{ width: `${magnitude}%` }}
                      />
                    </div>

                    <p className="text-slate-400 text-xs leading-relaxed">
                      {factor.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Recommendations Card */}
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-900 backdrop-blur-md shadow-xl">
            <div className="flex items-center gap-2 mb-6">
              <HeartHandshake className="w-5 h-5 text-emerald-400" />
              <h3 className="text-lg font-bold text-white">Personalized Wellness Roadmap</h3>
            </div>

            <div className="space-y-4">
              {recommendations.map((rec, index) => {
                const isCritical = rec.startsWith("CRITICAL:");
                return (
                  <div 
                    key={index} 
                    className={`p-4 rounded-xl flex gap-3 items-start border ${
                      isCritical
                        ? 'bg-rose-500/10 border-rose-500/25 text-rose-200'
                        : 'bg-slate-950/60 border-slate-850 text-slate-300'
                    }`}
                  >
                    <CheckCircle className={`w-4 h-4 mt-0.5 flex-shrink-0 ${isCritical ? 'text-rose-400' : 'text-brand-400'}`} />
                    <p className="text-xs sm:text-sm leading-relaxed">{rec}</p>
                  </div>
                );
              })}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default Results;

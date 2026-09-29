import React, { useEffect, useState } from 'react';
import API from '../services/api';
import { Calendar, ChevronDown, ChevronUp, AlertCircle, Sparkles, AlertTriangle, FileText } from 'lucide-react';

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await API.get('/history');
        setHistory(response.data);
      } catch (err) {
        setError('Failed to load assessment history. Ensure you are signed in and backend is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'High': return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
      case 'Moderate': return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
      default: return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex justify-center items-center py-20">
        <div className="w-8 h-8 rounded-full border-2 border-brand-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="flex-grow py-12 px-4 relative max-w-4xl mx-auto w-full">
      <div className="absolute top-1/4 left-1/4 w-[300px] h-[300px] rounded-full bg-brand-500/5 blur-[100px] pointer-events-none" />

      <div className="w-full p-8 rounded-2xl bg-slate-900/40 border border-slate-900 backdrop-blur-md z-10 shadow-xl">
        
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="p-2 bg-brand-500/10 border border-brand-500/20 text-brand-400 rounded-xl">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-2xl font-bold tracking-tight font-sans">Assessment Logs</h2>
            <p className="text-slate-400 text-sm">Review your past evaluations and mental health trajectory</p>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm rounded-xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}

        {history.length === 0 ? (
          <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl">
            <AlertTriangle className="w-8 h-8 text-slate-500 mx-auto mb-3" />
            <h3 className="text-base font-semibold text-slate-300 mb-1">No Records Found</h3>
            <p className="text-slate-500 text-xs max-w-sm mx-auto mb-4">You have not completed any depression risk assessments yet.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {history.map((record) => {
              const isExpanded = expandedId === record.assessment_id;
              const dateStr = new Date(record.timestamp).toLocaleDateString(undefined, {
                year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
              });
              const probPct = Math.round(record.depression_probability * 100);

              return (
                <div key={record.assessment_id} className="border border-slate-900 hover:border-slate-800 bg-slate-950/40 rounded-xl overflow-hidden transition-all">
                  
                  {/* Summary Bar */}
                  <div 
                    onClick={() => toggleExpand(record.assessment_id)}
                    className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-950 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <Calendar className="w-4 h-4 text-slate-500" />
                      <span className="text-xs sm:text-sm font-semibold text-slate-200">{dateStr}</span>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-slate-500">Score:</span>
                        <span className="text-xs sm:text-sm font-bold text-white">{probPct}%</span>
                      </div>
                      <span className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full border ${getRiskColor(record.risk_level)}`}>
                        {record.risk_level}
                      </span>
                      {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
                    </div>
                  </div>

                  {/* Expanded Attributions & Tips */}
                  {isExpanded && (
                    <div className="p-4 bg-slate-950/80 border-t border-slate-900 space-y-6">
                      
                      {/* Top Attributions */}
                      <div>
                        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1">
                          <Sparkles className="w-3.5 h-3.5 text-violet-400" /> Top Driving Factors
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          {record.top_factors.map((factor) => {
                            const isRisk = factor.shap_value > 0;
                            return (
                              <div key={factor.feature} className="p-3 bg-slate-900/40 border border-slate-900 rounded-lg">
                                <div className="flex justify-between items-center mb-1 text-[10px] font-bold">
                                  <span className="text-slate-300">{factor.feature.replace(/Degree_/, 'Program: ')}</span>
                                  <span className={isRisk ? 'text-rose-400' : 'text-emerald-400'}>
                                    {isRisk ? '+' : ''}{factor.shap_value.toFixed(2)}
                                  </span>
                                </div>
                                <p className="text-[11px] text-slate-400 leading-relaxed">{factor.description}</p>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* Top Recommendations */}
                      <div>
                        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">
                          Personalized Tips Checklist
                        </h4>
                        <div className="space-y-2">
                          {record.recommendations.map((rec, i) => (
                            <div key={i} className="p-3 bg-slate-900/40 border border-slate-900 rounded-lg text-xs text-slate-300 leading-relaxed">
                              {rec}
                            </div>
                          ))}
                        </div>
                      </div>

                    </div>
                  )}

                </div>
              );
            })}
          </div>
        )}

      </div>
    </div>
  );
}

export default History;

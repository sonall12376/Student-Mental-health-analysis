import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import { ClipboardList, AlertCircle, ArrowRight, ArrowLeft } from 'lucide-react';

function AssessmentForm() {
  const navigate = useNavigate();

  // Load baseline profile defaults from localStorage
  const defaultGender = localStorage.getItem('gender') || 'Male';
  const defaultAge = parseInt(localStorage.getItem('age') || '21');

  // Form states grouped logically
  const [formData, setFormData] = useState({
    gender: defaultGender,
    age: defaultAge,
    degree: 'BCA',
    cgpa: 7.5,
    academic_pressure: 3,
    study_satisfaction: 3,
    sleep_duration: '7-8 hours',
    dietary_habits: 'Moderate',
    work_study_hours: 6,
    financial_stress: 3,
    family_history_of_mental_illness: 'No',
    have_you_ever_had_suicidal_thoughts: 'No',
  });

  const [step, setStep] = useState(1); // 3-step wizard
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const nextStep = () => setStep((s) => Math.min(s + 1, 3));
  const prevStep = () => setStep((s) => Math.max(s - 1, 1));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // POST assessment questionnaire to FastAPI /predict
      const response = await API.post('/predict', formData);
      
      // Store results in localStorage so the results page can retrieve and render them
      localStorage.setItem('last_result', JSON.stringify(response.data));
      localStorage.setItem('last_assessment_input', JSON.stringify(formData));
      
      navigate('/results');
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Error submitting assessment. Check backend logs or credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Degree List
  const degrees = [
    "Class 12", "BCA", "B.Tech", "B.Sc", "B.Com", "BA", "B.Ed", "B.Arch", "B.Pharm", 
    "BBA", "BE", "BHM", "LLB", "M.Tech", "MSc", "MCA", "MBA", "MA", "M.Com", 
    "M.Ed", "M.Pharm", "LLM", "MBBS", "MD", "ME", "MHM", "PhD", "Other Degree"
  ];

  // Sleep list
  const sleepOptions = [
    "Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours", "Irregular Sleep"
  ];

  // Diet list
  const dietOptions = [
    "Healthy", "Moderate", "Unhealthy", "Irregular Diet"
  ];

  return (
    <div className="flex-grow flex items-center justify-center py-12 px-4 relative">
      <div className="absolute top-1/3 left-1/4 w-[400px] h-[400px] rounded-full bg-brand-500/5 blur-[120px] pointer-events-none" />

      <div className="w-full max-w-2xl p-8 rounded-2xl bg-slate-900/40 border border-slate-900 backdrop-blur-md z-10 shadow-xl">
        
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="p-2 bg-brand-500/10 border border-brand-500/20 text-brand-400 rounded-xl">
            <ClipboardList className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-2xl font-bold tracking-tight">Depression Risk Assessment</h2>
            <p className="text-slate-400 text-sm">Please answer honestly. Your responses are confidential.</p>
          </div>
        </div>

        {/* Progress indicator */}
        <div className="mb-8">
          <div className="flex justify-between text-xs text-slate-400 font-semibold mb-2">
            <span>Progress</span>
            <span>Step {step} of 3</span>
          </div>
          <div className="h-1.5 w-full bg-slate-950 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-brand-600 to-brand-400 transition-all duration-300"
              style={{ width: `${(step / 3) * 100}%` }}
            />
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm rounded-xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* STEP 1: Personal & Degree Information */}
          {step === 1 && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-white border-b border-slate-800 pb-2">Part 1: Demographics & Course</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Age
                  </label>
                  <input
                    type="number"
                    min="18"
                    max="60"
                    value={formData.age}
                    onChange={(e) => handleChange('age', parseInt(e.target.value))}
                    className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 focus:outline-none transition-colors text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Gender
                  </label>
                  <select
                    value={formData.gender}
                    onChange={(e) => handleChange('gender', e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 focus:outline-none transition-colors text-sm"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Degree Major
                  </label>
                  <select
                    value={formData.degree}
                    onChange={(e) => handleChange('degree', e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 focus:outline-none transition-colors text-sm"
                  >
                    {degrees.map((d) => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Current Cumulative GPA (CGPA)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0.0"
                    max="10.0"
                    value={formData.cgpa}
                    onChange={(e) => handleChange('cgpa', parseFloat(e.target.value))}
                    className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 focus:outline-none transition-colors text-sm"
                    placeholder="e.g. 7.85"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: Academic & Financial Stressors */}
          {step === 2 && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-white border-b border-slate-800 pb-2">Part 2: Workload & Stress Metrics</h3>

              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Academic Pressure (0 - Low, 5 - Extreme)
                    </label>
                    <span className="text-sm font-bold text-brand-400">{formData.academic_pressure}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="5"
                    value={formData.academic_pressure}
                    onChange={(e) => handleChange('academic_pressure', parseInt(e.target.value))}
                    className="w-full accent-brand-500 h-1.5 bg-slate-950 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Study Satisfaction (0 - None, 5 - High)
                    </label>
                    <span className="text-sm font-bold text-brand-400">{formData.study_satisfaction}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="5"
                    value={formData.study_satisfaction}
                    onChange={(e) => handleChange('study_satisfaction', parseInt(e.target.value))}
                    className="w-full accent-brand-500 h-1.5 bg-slate-950 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Financial Stress (1 - Minimal, 5 - High)
                    </label>
                    <span className="text-sm font-bold text-brand-400">{formData.financial_stress}</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={formData.financial_stress}
                    onChange={(e) => handleChange('financial_stress', parseInt(e.target.value))}
                    className="w-full accent-brand-500 h-1.5 bg-slate-950 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Daily Work & Study Hours (0 - 12 hours)
                    </label>
                    <span className="text-sm font-bold text-brand-400">{formData.work_study_hours} hrs</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="12"
                    value={formData.work_study_hours}
                    onChange={(e) => handleChange('work_study_hours', parseInt(e.target.value))}
                    className="w-full accent-brand-500 h-1.5 bg-slate-950 rounded-lg appearance-none cursor-pointer"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: Lifestyle Habits & Clinical Screener */}
          {step === 3 && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-white border-b border-slate-800 pb-2">Part 3: Habits & History</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Sleep Duration
                  </label>
                  <select
                    value={formData.sleep_duration}
                    onChange={(e) => handleChange('sleep_duration', e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 focus:outline-none transition-colors text-sm"
                  >
                    {sleepOptions.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Dietary Habits
                  </label>
                  <select
                    value={formData.dietary_habits}
                    onChange={(e) => handleChange('dietary_habits', e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 focus:border-brand-500 rounded-xl text-slate-100 focus:outline-none transition-colors text-sm"
                  >
                    {dietOptions.map((d) => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
                    Family History of Mental Illness
                  </label>
                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => handleChange('family_history_of_mental_illness', 'Yes')}
                      className={`flex-grow py-3 rounded-xl border text-sm font-semibold transition-all ${
                        formData.family_history_of_mental_illness === 'Yes'
                          ? 'bg-brand-500/10 border-brand-500 text-brand-400'
                          : 'border-slate-800 text-slate-400 bg-slate-950/50 hover:bg-slate-950'
                      }`}
                    >
                      Yes
                    </button>
                    <button
                      type="button"
                      onClick={() => handleChange('family_history_of_mental_illness', 'No')}
                      className={`flex-grow py-3 rounded-xl border text-sm font-semibold transition-all ${
                        formData.family_history_of_mental_illness === 'No'
                          ? 'bg-brand-500/10 border-brand-500 text-brand-400'
                          : 'border-slate-800 text-slate-400 bg-slate-950/50 hover:bg-slate-950'
                      }`}
                    >
                      No
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
                    Have you ever had suicidal thoughts?
                  </label>
                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => handleChange('have_you_ever_had_suicidal_thoughts', 'Yes')}
                      className={`flex-grow py-3 rounded-xl border text-sm font-semibold transition-all ${
                        formData.have_you_ever_had_suicidal_thoughts === 'Yes'
                          ? 'bg-rose-500/10 border-rose-500 text-rose-400'
                          : 'border-slate-800 text-slate-400 bg-slate-950/50 hover:bg-slate-950'
                      }`}
                    >
                      Yes
                    </button>
                    <button
                      type="button"
                      onClick={() => handleChange('have_you_ever_had_suicidal_thoughts', 'No')}
                      className={`flex-grow py-3 rounded-xl border text-sm font-semibold transition-all ${
                        formData.have_you_ever_had_suicidal_thoughts === 'No'
                          ? 'bg-brand-500/10 border-brand-500 text-brand-400'
                          : 'border-slate-800 text-slate-400 bg-slate-950/50 hover:bg-slate-950'
                      }`}
                    >
                      No
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex gap-4 pt-8 border-t border-slate-900">
            {step > 1 && (
              <button
                type="button"
                onClick={prevStep}
                className="px-6 py-3 rounded-xl border border-slate-800 hover:border-slate-700 text-slate-300 font-medium transition-colors flex items-center gap-2"
              >
                <ArrowLeft className="w-4 h-4" /> Back
              </button>
            )}
            
            {step < 3 ? (
              <button
                type="button"
                onClick={nextStep}
                className="ml-auto px-6 py-3 rounded-xl bg-slate-850 hover:bg-slate-800 border border-slate-850 hover:border-slate-700 text-brand-400 font-medium transition-colors flex items-center gap-2"
              >
                Next <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={loading}
                className="ml-auto px-6 py-3 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white font-medium shadow-lg shadow-brand-500/15 hover:shadow-brand-500/25 transition-all disabled:opacity-50 flex items-center gap-2"
              >
                {loading ? 'Analyzing Profile...' : 'Submit Assessment'}
              </button>
            )}
          </div>

        </form>
      </div>
    </div>
  );
}

export default AssessmentForm;

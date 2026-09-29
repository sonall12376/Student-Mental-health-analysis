import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap

# Set style for premium dark mode aesthetics
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'figure.facecolor': '#0f172a',  # slate-900 background
    'axes.facecolor': '#1e293b',    # slate-800 axes
    'axes.edgecolor': '#334155',    # slate-700 grid lines
    'grid.color': '#334155',
    'xtick.color': '#cbd5e1',       # slate-300 tick text
    'ytick.color': '#cbd5e1',
    'text.color': '#f8fafc',        # slate-50 text
    'axes.labelcolor': '#cbd5e1',
    'axes.titlecolor': '#f8fafc',
})

def main():
    print("Starting Phase 5: Explainable AI with SHAP...")
    
    # 1. Setup paths
    model_path = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\backend\models\best_model.joblib"
    data_path = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\data_clean\X_test.csv"
    plots_dir = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\notebooks\plots"
    os.makedirs(plots_dir, exist_ok=True)
    
    # 2. Load model and data
    print(f"Loading champion model from: {model_path}")
    model = joblib.load(model_path)
    
    print(f"Loading test features from: {data_path}")
    X_test = pd.read_csv(data_path)
    
    # 3. Initialize SHAP Explainer
    # TreeExplainer is specifically optimized for tree-based models like XGBoost.
    print("Calculating SHAP values using TreeExplainer...")
    explainer = shap.TreeExplainer(model)
    
    # Compute Shapley values for all test set rows
    # This might take a few seconds
    shap_values = explainer(X_test)
    
    # 4. Plot 1: Global Feature Importance (Bar Plot)
    # This plots the mean absolute SHAP value for each feature.
    print("Generating shap_feature_importance.png...")
    plt.figure(figsize=(10, 6))
    shap.plots.bar(shap_values, max_display=12, show=False)
    plt.title("SHAP Global Feature Importance", fontsize=14, fontweight="bold", pad=12)
    plt.gcf().patch.set_facecolor('#0f172a')
    for ax in plt.gcf().axes:
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='#cbd5e1')
        ax.xaxis.label.set_color('#cbd5e1')
        ax.yaxis.label.set_color('#cbd5e1')
        # Fix text colors inside the plot
        for text in ax.texts:
            text.set_color('#cbd5e1')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "shap_feature_importance.png"), dpi=150, facecolor='#0f172a')
    plt.close()

    # 5. Plot 2: SHAP Summary Plot (Beeswarm)
    # This shows feature importance combined with directional impact.
    print("Generating shap_summary_beeswarm.png...")
    plt.figure(figsize=(11, 7))
    shap.plots.beeswarm(shap_values, max_display=12, show=False)
    plt.title("SHAP Summary Plot (Feature Impact Distribution)", fontsize=14, fontweight="bold", pad=12)
    plt.gcf().patch.set_facecolor('#0f172a')
    for ax in plt.gcf().axes:
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='#cbd5e1')
        ax.xaxis.label.set_color('#cbd5e1')
        ax.yaxis.label.set_color('#cbd5e1')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "shap_summary_beeswarm.png"), dpi=150, facecolor='#0f172a')
    plt.close()

    # 6. Plot 3: Individual Prediction Explanation (Waterfall Plot)
    # Let's find an interesting student in the test set (e.g. index 0)
    print("Generating shap_individual_waterfall.png...")
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values[0], max_display=10, show=False)
    plt.title("Individual Prediction Explanation (Sample Student)", fontsize=14, fontweight="bold", pad=12)
    plt.gcf().patch.set_facecolor('#0f172a')
    for ax in plt.gcf().axes:
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='#cbd5e1')
        ax.xaxis.label.set_color('#cbd5e1')
        ax.yaxis.label.set_color('#cbd5e1')
        for text in ax.texts:
            text.set_color('#cbd5e1')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "shap_individual_waterfall.png"), dpi=150, facecolor='#0f172a')
    plt.close()
    
    # 7. Print Individual SHAP Values for API design
    # Let's show how we will format local SHAP values as JSON to send to the React frontend
    print("\n--- Example Individual SHAP Attributions (Row 0) ---")
    row_idx = 0
    # shap_values[row_idx].values represents the Shapley values for that row.
    # shap_values[row_idx].data represents the raw feature values for that row.
    features = X_test.columns.tolist()
    shap_vals = shap_values[row_idx].values.tolist()
    feat_vals = shap_values[row_idx].data.tolist()
    
    # Create list of dictionaries
    attributions = []
    for f, sv, fv in zip(features, shap_vals, feat_vals):
        attributions.append({
            "feature": f,
            "feature_value": fv,
            "shap_value": sv
        })
        
    # Sort by absolute SHAP value to find top drivers
    attributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    
    # Filter: Top 5 contributing factors
    print(f"Prediction Probability (Log Odds): {float(np.sum(shap_vals) + explainer.expected_value):.4f}")
    print("Top 5 Attributions (JSON-ready structure):")
    import json
    print(json.dumps(attributions[:5], indent=2))
    
    print("\nPhase 5 complete!")

if __name__ == "__main__":
    main()

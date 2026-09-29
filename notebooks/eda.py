import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for premium aesthetics
sns.set_theme(style="darkgrid")
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
    print("Starting Phase 3: Exploratory Data Analysis...")
    
    # 1. Setup paths
    csv_path = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\data_clean\student_data_clean.csv"
    plots_dir = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\notebooks\plots"
    os.makedirs(plots_dir, exist_ok=True)
    
    # 2. Load dataset
    df = pd.read_csv(csv_path)
    
    # Custom color palette (brand-like violet and turquoise/emerald)
    colors = ["#10b981", "#8b5cf6"] # emerald-500, brand-500
    
    # ==========================================
    # Plot 1: Histograms of Age & CGPA
    # ==========================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.histplot(data=df, x='Age', kde=True, ax=axes[0], color='#a78bfa', bins=20)
    axes[0].set_title('Distribution of Student Age', fontsize=14, fontweight='bold', pad=12)
    axes[0].set_xlabel('Age (Years)')
    axes[0].set_ylabel('Student Count')
    
    sns.histplot(data=df, x='CGPA', kde=True, ax=axes[1], color='#34d399', bins=25)
    axes[1].set_title('Distribution of Student CGPA', fontsize=14, fontweight='bold', pad=12)
    axes[1].set_xlabel('CGPA (0.0 to 10.0)')
    axes[1].set_ylabel('Student Count')
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '1_histograms_age_cgpa.png'), dpi=150, facecolor='#0f172a')
    plt.close()
    print("Generated 1_histograms_age_cgpa.png")

    # ==========================================
    # Plot 2: Count plot of Depression (Target Class)
    # ==========================================
    plt.figure(figsize=(7, 5))
    ax = sns.countplot(data=df, x='Depression', palette=colors)
    plt.title('Depression Class Distribution (Target Variable)', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Depression Status (0 = Not Depressed, 1 = Depressed)')
    plt.ylabel('Student Count')
    
    # Add count labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points', color='#cbd5e1')
                    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '2_count_plot_depression.png'), dpi=150, facecolor='#0f172a')
    plt.close()
    print("Generated 2_count_plot_depression.png")

    # ==========================================
    # Plot 3: Categorical Count plots by Target
    # ==========================================
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Sleep duration vs Depression
    sleep_order = ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours", "Irregular Sleep"]
    sns.countplot(data=df, x='Sleep.Duration', hue='Depression', order=sleep_order, ax=axes[0], palette=colors)
    axes[0].set_title('Depression Status by Sleep Duration', fontsize=14, fontweight='bold', pad=12)
    axes[0].set_xlabel('Sleep Duration per Night')
    axes[0].set_ylabel('Student Count')
    axes[0].legend(title='Depression', labels=['Not Depressed', 'Depressed'], facecolor='#1e293b', edgecolor='#334155')
    
    # Dietary Habits vs Depression
    diet_order = ["Healthy", "Moderate", "Unhealthy", "Irregular Diet"]
    sns.countplot(data=df, x='Dietary.Habits', hue='Depression', order=diet_order, ax=axes[1], palette=colors)
    axes[1].set_title('Depression Status by Dietary Habits', fontsize=14, fontweight='bold', pad=12)
    axes[1].set_xlabel('Diet Quality')
    axes[1].set_ylabel('Student Count')
    axes[1].legend(title='Depression', labels=['Not Depressed', 'Depressed'], facecolor='#1e293b', edgecolor='#334155')
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '3_count_plots_sleep_diet.png'), dpi=150, facecolor='#0f172a')
    plt.close()
    print("Generated 3_count_plots_sleep_diet.png")

    # ==========================================
    # Plot 4: Box plots of CGPA & Study/Work Hours vs Target
    # ==========================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.boxplot(data=df, x='Depression', y='CGPA', ax=axes[0], palette=colors)
    axes[0].set_title('Student CGPA vs. Depression', fontsize=14, fontweight='bold', pad=12)
    axes[0].set_xlabel('Depression Status (0 = Not Depressed, 1 = Depressed)')
    axes[0].set_ylabel('Cumulative GPA')
    
    sns.boxplot(data=df, x='Depression', y='Work.Study.Hours', ax=axes[1], palette=colors)
    axes[1].set_title('Daily Work/Study Hours vs. Depression', fontsize=14, fontweight='bold', pad=12)
    axes[1].set_xlabel('Depression Status (0 = Not Depressed, 1 = Depressed)')
    axes[1].set_ylabel('Hours Spent per Day')
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '4_box_plots_work_cgpa.png'), dpi=150, facecolor='#0f172a')
    plt.close()
    print("Generated 4_box_plots_work_cgpa.png")

    # ==========================================
    # Plot 5: Correlation Heatmap
    # ==========================================
    # Prepare a DataFrame with only the core numeric & ordinal features (same mappings as Phase 2)
    corr_df = df.copy()
    
    # Drops non-numeric/high-cardinality features we excluded or one-hot encoded
    corr_df = corr_df.drop(columns=["id", "Job.Satisfaction", "Degree"])
    
    # Re-apply mappings for correlation computation
    sleep_map = {"7-8 hours": 3, "More than 8 hours": 4, "5-6 hours": 2, "Less than 5 hours": 1, "Irregular Sleep": 0}
    diet_map = {"Healthy": 3, "Moderate": 2, "Unhealthy": 1, "Irregular Diet": 0}
    gender_map = {"Male": 1, "Female": 0}
    yes_no_map = {"Yes": 1, "No": 0}
    
    corr_df["Sleep.Duration"] = corr_df["Sleep.Duration"].map(sleep_map).fillna(2)
    corr_df["Dietary.Habits"] = corr_df["Dietary.Habits"].map(diet_map).fillna(2)
    corr_df["Gender"] = corr_df["Gender"].map(gender_map).fillna(0)
    corr_df["Family.History.of.Mental.Illness"] = corr_df["Family.History.of.Mental.Illness"].map(yes_no_map).fillna(0)
    corr_df["Have.you.ever.had.suicidal.thoughts.."] = corr_df["Have.you.ever.had.suicidal.thoughts.."].map(yes_no_map).fillna(0)
    
    # Calculate Pearson correlation
    corr_matrix = corr_df.corr()
    
    # Create mask for upper triangle to improve readability (optional, but looks premium!)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        corr_matrix, 
        mask=mask, 
        annot=True, 
        fmt=".2f", 
        cmap='coolwarm', 
        vmin=-1, 
        vmax=1, 
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": .8}
    )
    plt.title('Correlation Matrix of Student Stress & Risk Factors', fontsize=15, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '5_correlation_heatmap.png'), dpi=150, facecolor='#0f172a')
    plt.close()
    print("Generated 5_correlation_heatmap.png")
    print("Phase 3 complete!")

if __name__ == "__main__":
    main()

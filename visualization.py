"""
Visualization functions for fairness analysis
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("⚠️  Seaborn not available, using matplotlib styling only")


def create_fairness_dashboard(df):
    """Create comprehensive fairness visualization dashboard"""
    
    # Set style based on available libraries
    if SEABORN_AVAILABLE:
        plt.style.use('seaborn-v0_8')
    else:
        plt.style.use('ggplot')
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Recidivism Rates by Race
    recidivism_rates = df.groupby('race')['two_year_recid'].mean().sort_values()
    bars = axes[0,0].bar(recidivism_rates.index, recidivism_rates.values, 
                        color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    axes[0,0].set_title('Recidivism Rates by Race', fontsize=14, fontweight='bold')
    axes[0,0].set_ylabel('Recidivism Rate')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[0,0].text(bar.get_x() + bar.get_width()/2., height,
                      f'{height:.3f}', ha='center', va='bottom')
    
    # Plot 2: Risk Score Distribution
    caucasian_scores = df[df['race'] == 'Caucasian']['decile_score']
    african_american_scores = df[df['race'] == 'African-American']['decile_score']
    
    axes[0,1].hist([caucasian_scores, african_american_scores], 
                   bins=10, alpha=0.7, label=['Caucasian', 'African-American'],
                   color=['#1f77b4', '#ff7f0e'])
    axes[0,1].set_title('Risk Score Distribution by Race', fontsize=14, fontweight='bold')
    axes[0,1].set_xlabel('Decile Score')
    axes[0,1].set_ylabel('Frequency')
    axes[0,1].legend()
    
    # Plot 3: False Positive Analysis
    fp_rates = calculate_false_positive_rates(df)
    bars_fp = axes[1,0].bar(fp_rates.index, fp_rates.values, 
                           color=['#1f77b4', '#ff7f0e'])
    axes[1,0].set_title('False Positive Rates by Race', fontsize=14, fontweight='bold')
    axes[1,0].set_ylabel('False Positive Rate')
    
    # Add value labels on bars
    for bar in bars_fp:
        height = bar.get_height()
        axes[1,0].text(bar.get_x() + bar.get_width()/2., height,
                      f'{height:.3f}', ha='center', va='bottom')
    
    # Plot 4: Sample Size Comparison
    sample_sizes = df['race'].value_counts()
    axes[1,1].pie(sample_sizes.values, labels=sample_sizes.index, autopct='%1.1f%%',
                  colors=['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728'])
    axes[1,1].set_title('Dataset Composition by Race', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('reports/images/compas_fairness_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()


def calculate_false_positive_rates(df):
    """Calculate false positive rates by race group"""
    fp_rates = {}
    for race in ['Caucasian', 'African-American']:
        subgroup = df[df['race'] == race]
        # Using decile_score > 5 as prediction of high risk
        high_risk = subgroup[subgroup['decile_score'] > 5]
        if len(high_risk) > 0:
            false_positives = len(high_risk[high_risk['two_year_recid'] == 0])
            fp_rates[race] = false_positives / len(high_risk)
        else:
            fp_rates[race] = 0
    return pd.Series(fp_rates)


if __name__ == "__main__":
    from data_loader import load_compas_data
    df = load_compas_data()
    create_fairness_dashboard(df)
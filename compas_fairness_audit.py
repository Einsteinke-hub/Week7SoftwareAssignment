# compas_robust_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def setup_environment():
    """Create required directories"""
    folders = ['data/processed', 'reports/images']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    print("✅ Environment setup complete")

def load_and_clean_compas_data():
    """Load and thoroughly clean COMPAS dataset"""
    print("📥 Downloading COMPAS dataset...")
    url = "https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv"
    df = pd.read_csv(url)
    
    print("🔧 Preprocessing data...")
    # Apply ProPublica's filtering criteria
    df = df[
        (df.days_b_screening_arrest <= 30) & 
        (df.days_b_screening_arrest >= -30) &
        (df.is_recid != -1) &
        (df.c_charge_degree != 'O') &
        (df.score_text != 'N/A')
    ].copy()
    
    # Create binary race variable
    df['race_binary'] = df['race'].map({'Caucasian': 1, 'African-American': 0})
    
    # Remove rows with NA values in critical columns
    critical_columns = ['two_year_recid', 'race_binary', 'decile_score']
    initial_count = len(df)
    df = df.dropna(subset=critical_columns)
    removed_count = initial_count - len(df)
    
    # Ensure data types are correct
    df['two_year_recid'] = df['two_year_recid'].astype(int)
    df['race_binary'] = df['race_binary'].astype(int)
    df['decile_score'] = df['decile_score'].astype(int)
    
    print(f"🔍 Data cleaning report:")
    print(f"   Initial records: {initial_count}")
    print(f"   Removed due to NA: {removed_count}")
    print(f"   Final clean records: {len(df)}")
    
    # Save processed data
    df.to_csv('data/processed/compas_cleaned.csv', index=False)
    
    print("📊 Race distribution:")
    print(df['race'].value_counts())
    
    return df

def calculate_comprehensive_fairness_metrics(df):
    """Calculate comprehensive fairness metrics"""
    caucasian = df[df['race'] == 'Caucasian']
    african_american = df[df['race'] == 'African-American']
    
    print(f"\n📊 DATASET SUMMARY:")
    print(f"   Caucasian defendants: {len(caucasian)}")
    print(f"   African-American defendants: {len(african_american)}")
    
    # Base rates (actual recidivism)
    br_caucasian = caucasian['two_year_recid'].mean()
    br_african_american = african_american['two_year_recid'].mean()
    
    # Statistical Parity Difference
    statistical_parity_diff = br_african_american - br_caucasian
    
    # Disparate Impact
    disparate_impact = br_african_american / br_caucasian if br_caucasian > 0 else 1
    
    # False positive rates (using decile_score > 5 as prediction of high risk)
    fp_caucasian = len(caucasian[(caucasian['decile_score'] > 5) & (caucasian['two_year_recid'] == 0)]) / len(caucasian)
    fp_african_american = len(african_american[(african_american['decile_score'] > 5) & (african_american['two_year_recid'] == 0)]) / len(african_american)
    
    # False negative rates
    fn_caucasian = len(caucasian[(caucasian['decile_score'] <= 5) & (caucasian['two_year_recid'] == 1)]) / len(caucasian)
    fn_african_american = len(african_american[(african_american['decile_score'] <= 5) & (african_american['two_year_recid'] == 1)]) / len(african_american)
    
    # Equal Opportunity Difference (False Negative Rate difference)
    equal_opportunity_diff = fn_african_american - fn_caucasian
    
    print("\n🎯 FAIRNESS METRICS:")
    print(f"   Base Rate - Caucasian: {br_caucasian:.3f}")
    print(f"   Base Rate - African-American: {br_african_american:.3f}")
    print(f"   Statistical Parity Difference: {statistical_parity_diff:.3f}")
    print(f"   Disparate Impact Ratio: {disparate_impact:.3f}")
    print(f"   False Positive Rate - Caucasian: {fp_caucasian:.3f}")
    print(f"   False Positive Rate - African-American: {fp_african_american:.3f}")
    print(f"   False Negative Rate - Caucasian: {fn_caucasian:.3f}")
    print(f"   False Negative Rate - African-American: {fn_african_american:.3f}")
    print(f"   Equal Opportunity Difference: {equal_opportunity_diff:.3f}")
    
    return {
        'statistical_parity_diff': statistical_parity_diff,
        'disparate_impact': disparate_impact,
        'base_rates': (br_caucasian, br_african_american),
        'fp_rates': (fp_caucasian, fp_african_american),
        'fn_rates': (fn_caucasian, fn_african_american),
        'equal_opportunity_diff': equal_opportunity_diff
    }

def create_detailed_visualizations(df, metrics):
    """Create detailed fairness visualizations"""
    plt.figure(figsize=(16, 12))
    
    # Plot 1: Base Rates
    plt.subplot(2, 3, 1)
    races = ['Caucasian', 'African-American']
    base_rates = metrics['base_rates']
    bars = plt.bar(races, base_rates, color=['blue', 'orange'], alpha=0.7)
    plt.title('Actual Recidivism Rates', fontweight='bold')
    plt.ylabel('Recidivism Rate')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    # Plot 2: False Positive Rates
    plt.subplot(2, 3, 2)
    fp_rates = metrics['fp_rates']
    bars = plt.bar(races, fp_rates, color=['blue', 'orange'], alpha=0.7)
    plt.title('False Positive Rates', fontweight='bold')
    plt.ylabel('False Positive Rate')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    # Plot 3: False Negative Rates
    plt.subplot(2, 3, 3)
    fn_rates = metrics['fn_rates']
    bars = plt.bar(races, fn_rates, color=['blue', 'orange'], alpha=0.7)
    plt.title('False Negative Rates', fontweight='bold')
    plt.ylabel('False Negative Rate')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    # Plot 4: Risk Score Distribution
    plt.subplot(2, 3, 4)
    caucasian_scores = df[df['race'] == 'Caucasian']['decile_score']
    african_american_scores = df[df['race'] == 'African-American']['decile_score']
    plt.hist([caucasian_scores, african_american_scores], 
             bins=10, alpha=0.7, label=['Caucasian', 'African-American'],
             color=['blue', 'orange'])
    plt.title('Risk Score Distribution', fontweight='bold')
    plt.xlabel('Decile Score')
    plt.ylabel('Frequency')
    plt.legend()
    
    # Plot 5: Fairness Metrics
    plt.subplot(2, 3, 5)
    fairness_metrics = ['Statistical Parity', 'Disparate Impact', 'Equal Opportunity']
    values = [
        metrics['statistical_parity_diff'],
        metrics['disparate_impact'] - 1,  # Center around 0
        metrics['equal_opportunity_diff']
    ]
    colors = ['red' if abs(x) > 0.1 else 'green' for x in values]
    bars = plt.bar(fairness_metrics, values, color=colors, alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.title('Fairness Metrics (Difference from Fair)', fontweight='bold')
    plt.ylabel('Difference from Fair Value')
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    # Plot 6: Sample Composition
    plt.subplot(2, 3, 6)
    sample_sizes = df['race'].value_counts()
    plt.pie(sample_sizes.values, labels=sample_sizes.index, autopct='%1.1f%%',
            colors=['orange', 'blue'])
    plt.title('Dataset Composition', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('reports/images/comprehensive_fairness_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_fairness_report(metrics):
    """Generate a summary fairness report"""
    print("\n" + "="*60)
    print("📋 FAIRNESS ASSESSMENT REPORT")
    print("="*60)
    
    # Disparate Impact Assessment
    di = metrics['disparate_impact']
    if di < 0.8:
        di_assessment = "❌ UNFAIR (Strong adverse impact)"
    elif di < 0.9:
        di_assessment = "⚠️  MARGINAL (Moderate adverse impact)"
    else:
        di_assessment = "✅ FAIR (Within acceptable range)"
    
    # Statistical Parity Assessment
    sp = abs(metrics['statistical_parity_diff'])
    if sp > 0.1:
        sp_assessment = "❌ UNFAIR (Large difference)"
    elif sp > 0.05:
        sp_assessment = "⚠️  MARGINAL (Moderate difference)"
    else:
        sp_assessment = "✅ FAIR (Small difference)"
    
    # Equal Opportunity Assessment
    eo = abs(metrics['equal_opportunity_diff'])
    if eo > 0.1:
        eo_assessment = "❌ UNFAIR (Large FNR difference)"
    elif eo > 0.05:
        eo_assessment = "⚠️  MARGINAL (Moderate FNR difference)"
    else:
        eo_assessment = "✅ FAIR (Small FNR difference)"
    
    print(f"Disparate Impact Ratio: {di:.3f} - {di_assessment}")
    print(f"Statistical Parity Difference: {metrics['statistical_parity_diff']:.3f} - {sp_assessment}")
    print(f"Equal Opportunity Difference: {metrics['equal_opportunity_diff']:.3f} - {eo_assessment}")
    
    print("\n💡 RECOMMENDATIONS:")
    if di < 0.8 or sp > 0.1:
        print("• Consider implementing bias mitigation techniques")
        print("• Review feature selection to remove proxy variables")
        print("• Use fairness-aware algorithms")
    else:
        print("• System shows acceptable fairness levels")
        print("• Continue monitoring for drift over time")

def main():
    """Main execution function"""
    print("🚀 Starting COMPAS Fairness Audit...")
    
    # Setup environment
    setup_environment()
    
    # Load and clean data
    df = load_and_clean_compas_data()
    
    # Calculate comprehensive metrics
    metrics = calculate_comprehensive_fairness_metrics(df)
    
    # Create visualizations
    create_detailed_visualizations(df, metrics)
    
    # Generate report
    generate_fairness_report(metrics)
    
    print("\n✅ Analysis complete! Check reports/images/ for visualizations")

if __name__ == "__main__":
    main()
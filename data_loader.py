"""
Data loading and preprocessing utilities
"""

import pandas as pd
import os


def load_compas_data():
    """Load and preprocess COMPAS dataset"""
    
    # Create directories if they don't exist
    os.makedirs('data/processed', exist_ok=True)
    
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
    df = df[df['race_binary'].notna()]
    
    # Save processed data
    df.to_csv('data/processed/compas_cleaned.csv', index=False)
    
    print(f"✅ Data saved: {len(df)} records processed")
    print(f"📊 Race distribution:")
    print(df['race'].value_counts())
    
    return df


if __name__ == "__main__":
    data = load_compas_data()
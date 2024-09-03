import pandas as pd
import numpy as np

def time_signature_features(time_signature):
    # Common time signatures
    common_sigs = [4, 3, 2, 6, 5, 7]
    features = {f'is_{sig}_4': int(time_signature == sig) for sig in common_sigs}
    
    # Additional features
    features['is_simple_meter'] = int(time_signature in [2, 3, 4])
    features['is_compound_meter'] = int(time_signature in [6, 9, 12])
    features['is_complex_meter'] = int(not (features['is_simple_meter'] or features['is_compound_meter']))
    
    # Categorize the "feel" of the time signature
    if time_signature in [2, 4, 2/2, 4/4]:
        features['metric_feel'] = 'Duple'
    elif time_signature in [3, 9, 3/4, 9/8]:
        features['metric_feel'] = 'Triple'
    elif time_signature in [5, 7, 5/4, 7/4]:
        features['metric_feel'] = 'Irregular'
    else:
        features['metric_feel'] = 'Other'
    
    # Measure complexity (higher number = more complex)
    features['time_sig_complexity'] = time_signature if time_signature > 1 else 1/time_signature
    
    return features

# Assuming df is your DataFrame and 'time_signature' is your column name
df = pd.read_csv('your_music_data.csv')

# Apply the function to create new features
time_sig_features = df['time_signature'].apply(time_signature_features).apply(pd.Series)

# Concatenate new features with the original DataFrame
df = pd.concat([df, time_sig_features], axis=1)

# Create 'beats per bar' feature (assuming 'tempo' is in BPM)
df['beats_per_bar'] = df['tempo'] * df['time_signature'] / 60

# One-hot encode the 'metric_feel' feature
metric_feel_dummies = pd.get_dummies(df['metric_feel'], prefix='metric_feel')
df = pd.concat([df, metric_feel_dummies], axis=1)

# Save the updated dataset
df.to_csv('enhanced_music_data_with_time_sig.csv', index=False)

print("Enhanced dataset with comprehensive time signature features created and saved.")
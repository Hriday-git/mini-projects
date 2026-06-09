import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("wildlife_tracking_copy.csv")

# Convert datetime columns
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True, errors='coerce')
df['episode_start_time'] = pd.to_datetime(df['episode_start_time'], dayfirst=True, errors='coerce')
df['episode_end_time'] = pd.to_datetime(df['episode_end_time'], dayfirst=True, errors='coerce')

# -------------------------------
# STEP 1: Update year to 2024
# -------------------------------
df['timestamp'] = df['timestamp'].apply(lambda x: x.replace(year=2024))
df['episode_start_time'] = df['episode_start_time'].apply(lambda x: x.replace(year=2024))
df['episode_end_time'] = df['episode_end_time'].apply(lambda x: x.replace(year=2024))

# -------------------------------
# STEP 2: FIX behavior_duration_hours
# -------------------------------
df['behavior_duration_hours'] = (
    (df['episode_end_time'] - df['episode_start_time']).dt.total_seconds() / 3600
).round(2)

# Fix unrealistic 0 values for active motion
df.loc[
    (df['motion_type'].isin(['Running', 'Grazing'])) & 
    (df['behavior_duration_hours'] <= 0),
    'behavior_duration_hours'
] = np.random.uniform(0.2, 2.0)

# -------------------------------
# STEP 3: EXPAND DATA
# -------------------------------
original_df = df.copy()
new_rows = []

EXPANSION_FACTOR = 20

for _, row in original_df.iterrows():
    base_time = row['timestamp']
    
    for i in range(1, EXPANSION_FACTOR + 1):
        new_row = row.copy()
        
        # Time progression
        new_time = base_time + pd.Timedelta(minutes=5*i)
        new_row['timestamp'] = new_time
        
        # Episode timing
        start_time = new_time
        end_time = start_time + pd.Timedelta(minutes=np.random.randint(5, 120))
        
        new_row['episode_start_time'] = start_time
        new_row['episode_end_time'] = end_time
        
        # Duration calculation
        duration = (end_time - start_time).total_seconds() / 3600
        new_row['behavior_duration_hours'] = round(duration, 2)
        
        # Heart rate variation
        new_row['heart_rate'] = max(40, row['heart_rate'] + np.random.randint(-3, 4))
        
        # Temperature variation
        new_row['temperature'] = round(row['temperature'] + np.random.uniform(-0.3, 0.3), 2)
        
        # GPS variation
        new_row['latitude'] = row['latitude'] + np.random.uniform(-0.0003, 0.0003)
        new_row['longitude'] = row['longitude'] + np.random.uniform(-0.0003, 0.0003)
        
        # Motion consistency
        if new_row['motion_type'] == 'Stationary':
            new_row['motion'] = 'No'
        else:
            new_row['motion'] = 'Yes'
        
        # Location logic
        if new_row['heart_rate'] > 110:
            new_row['location'] = 'Distorted'
        else:
            new_row['location'] = 'OK'
        
        new_rows.append(new_row)

# Create dataframe
new_df = pd.DataFrame(new_rows)

# Combine
final_df = pd.concat([original_df, new_df], ignore_index=True)

# Sort by time
final_df = final_df.sort_values(by='timestamp').reset_index(drop=True)

# Save
final_df.to_csv("wildlife_tracking_2024_expanded.csv", index=False)

print("Dataset processed successfully")
print("Total rows:", len(final_df))
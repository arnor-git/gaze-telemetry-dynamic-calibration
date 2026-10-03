# -*- coding: utf-8 -*-


from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import datetime
import json
import  os
from scipy.spatial import ConvexHull
from matplotlib.path import Path
import matplotlib.patches as patches
from datetime import datetime
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os
import re
import shutil
from collections import defaultdict

source_folder = "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/portugal_dataset/"
destination_folder = "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/triplets/"

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

def extract_subject_id(filename):
    name = os.path.splitext(filename)[0]
    subject_id = re.sub(r'\d+$', '', name)
    return subject_id

# Map Subject IDs to their files
subject_files = defaultdict(list)
for file in os.listdir(source_folder):
    if file.endswith(".csv"):
        sid = extract_subject_id(file)
        subject_files[sid].append(file)

# Identify subjects with exactly 3 files and move them
moved_count = 0
print(f"{'Subject ID':<20} | {'Status'}")


for subject, files in subject_files.items():
    if len(files) == 3:
        for f in files:
            source_path = os.path.join(source_folder, f)
            dest_path = os.path.join(destination_folder, f)
            shutil.move(source_path, dest_path)

        print(f"{subject:<20} | Moved 3 files")
        moved_count += 1
    else:
        print(f"{subject:<20} | Skipped ({len(files)} files)")

print(f"Done! Moved {moved_count} subjects to {destination_folder}")

import os
import pandas as pd


folders_map = {
    '/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/triplets_po/':
    '/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/processed_portugal_data/',

    '/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/triplets_ro/':
    '/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/processed_romania_data/'
}

for input_folder, output_folder in folders_map.items():
    if not os.path.exists(input_folder):
        print(f"Skipping: Input folder {input_folder} not found.")
        continue

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files_to_process = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    print(f"\n--- Processing {len(files_to_process)} files from: {input_folder} ---")

    for filename in files_to_process:
        file_path = os.path.join(input_folder, filename)

        try:
            # 2. Load Data
            # sep=None with engine='python' automatically detects if it's ';' or ','
            L1df = pd.read_csv(file_path, sep=None, engine='python')

            # 3. Separating the columns
            # We use .str.strip and .split to extract coordinates
            L1df[['EyeTracker-x', 'EyeTracker-y']] = L1df['EyeTracker'].str.strip("()").str.split(",", expand=True).astype(float)
            L1df[['obj_x', 'obj_y']] = L1df['GameObjectPos (Screen Coordinates)'].str.strip("()").str.split(",", expand=True).astype(float)

            # 4. Clean data
            initial_row_count = len(L1df)

            # Drop rows where EyeTracker coordinates are missing
            df = L1df.dropna(subset=['EyeTracker-x', 'EyeTracker-y']).copy()

            # Drop original string-tuple columns
            df = df.drop(columns=['EyeTracker', 'GameObjectPos (Screen Coordinates)'])
            df = df.reset_index(drop=True)

            # 5. Save processed file
            output_path = os.path.join(output_folder, filename)
            df.to_csv(output_path, index=False)

            rows_removed = initial_row_count - len(df)
            print(f"   Processed: {filename} | Rows Removed: {rows_removed}")

        except Exception as e:
            print(f"   Error processing {filename}: {e}")

print("\nAll things completed!")

import os
import shutil

source_folders = {
    "pt": "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/processed_portugal_data",
    "ro": "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/processed_romania_data"
}
merged_folder = "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/merged_pilot_data/"

if not os.path.exists(merged_folder):
    os.makedirs(merged_folder)
    print(f"Created folder: {merged_folder}")

print(f"{'Original Filename':<55} | {'Cleaned Filename'}")


for prefix, folder_path in source_folders.items():
    if not os.path.exists(folder_path):
        print(f"Skipping {folder_path}: Folder not found.")
        continue

    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for filename in files:
        # 1. Clean the filename by removing "Copy of " if it exists
        clean_name = filename.replace("Copy of ", "")

        # 2. Construct the standardized name: e.g., pt_Stimulus_S1.csv
        new_filename = f"{prefix}_{clean_name}"

        source_file = os.path.join(folder_path, filename)
        destination_file = os.path.join(merged_folder, new_filename)

        # 3. Copy and rename
        shutil.copy2(source_file, destination_file)
        print(f"{filename:<55} | {new_filename}")


print(f"Done! All files cleaned and merged into: {merged_folder}")

"""

```
# This is formatted as code
```

# FInal Version"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

merged_data_path = "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/merged_pilot_data"
all_fixation_stats = []
all_reaction_times = []

files = [f for f in os.listdir(merged_data_path) if f.endswith('.csv')]
print(f"Total files found: {len(files)}")

for f in files:
    f_lower = f.lower()
    country = "Portugal" if f_lower.startswith('pt_') else "Romania"
    full_path = os.path.join(merged_data_path, f)

    try:
        df = pd.read_csv(full_path, sep=None, engine='python', on_bad_lines='skip')
        df.columns = [str(col).strip() for col in df.columns]

        # A. GAZE VELOCITY (Fixation Threshold)
        if 'Timestamp' in df.columns and 'EyeTracker-x' in df.columns:
            time_sec = df['Timestamp'].diff() / 1000.0
            time_sec = time_sec.where(time_sec > 0.001, np.nan)
            dist = np.sqrt(df['EyeTracker-x'].diff()**2 + df['EyeTracker-y'].diff()**2)
            velocity = dist / time_sec
            velocity = velocity.replace([np.inf, -np.inf], np.nan).dropna()

            if not velocity.empty:
                v_clean = velocity[velocity <= np.percentile(velocity, 99)]
                all_fixation_stats.append({
                    'Country': country,
                    'fixation_threshold': np.percentile(v_clean, 75)
                })

        # B. REACTION TIMES
        if 'ObjectState' in df.columns and 'ObjectName' in df.columns:
            appearances = df[df['ObjectState'] == 'Appear']
            clicks = df[df['ObjectName'] == 'Mouse Click']

            for _, app in appearances.iterrows():
                valid_clicks = clicks[(clicks['Timestamp'] > app['Timestamp']) &
                                      (clicks['Timestamp'] < app['Timestamp'] + 15000)] # 15s scan window
                if not valid_clicks.empty:
                    rt = valid_clicks.iloc[0]['Timestamp'] - app['Timestamp']
                    all_reaction_times.append({'Country': country, 'RT': rt})

    except Exception as e:
        print(f"Error processing {f}: {e}")

# --- 3. Results & Visualization ---
fix_df = pd.DataFrame(all_fixation_stats)
rt_df = pd.DataFrame(all_reaction_times)

if not fix_df.empty and not rt_df.empty:
    # Final Parameter Calculations
    final_fixation_threshold = fix_df['fixation_threshold'].median()
    rt_min = np.percentile(rt_df['RT'], 5)
    rt_max = np.percentile(rt_df['RT'], 95)

    print("FINAL VALIDATED PARAMETERS")
    print(f"1. FIXATION THRESHOLD:   {final_fixation_threshold:.2f} px/s")
    print(f"2. MIN REACTION TIME:    {rt_min:.2f} ms")
    print(f"3. MAX REACTION TIME:    {rt_max:.2f} ms")


    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    # Box Plot for Fixation Thresholds (Gaze Stability)
    sns.boxplot(x='Country', y='fixation_threshold', data=fix_df, palette='Set2', ax=ax[0])
    ax[0].axhline(final_fixation_threshold, color='red', linestyle='--', label='Global Median')
    ax[0].set_title('Fixation Threshold Distribution')
    ax[0].set_ylabel('Velocity (px/s)')
    ax[0].legend()

    # Box Plot for Reaction Times
    sns.boxplot(x='Country', y='RT', data=rt_df, palette='Set3', ax=ax[1])
    ax[1].axhline(rt_min, color='blue', linestyle='--', label='5th Pct (Min RT)')
    ax[1].axhline(rt_max, color='orange', linestyle='--', label='95th Pct (Max RT)')
    ax[1].set_title('Reaction Time (RT) Distribution')
    ax[1].set_ylabel('Time (ms)')
    ax[1].set_yscale('log') # Log scale helps see the 366ms vs 8000ms better
    ax[1].legend()

    plt.tight_layout()
    plt.show()

else:
    print("No data processed. Check folder contents.")

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- Configuration ---
merged_data_path = "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/merged_pilot_data"
global_velocities = []
individual_thresholds = []

files = [f for f in os.listdir(merged_data_path) if f.endswith('.csv')]

# --- 1. Data Collection & Dynamic Calculation ---
for f in files:
    try:
        df = pd.read_csv(os.path.join(merged_data_path, f), sep=None, engine='python')
        df.columns = [str(col).strip() for col in df.columns]

        if 'Timestamp' in df.columns and 'EyeTracker-x' in df.columns:
            time_diff = df['Timestamp'].diff() / 1000.0
            time_diff = time_diff.where(time_diff > 0.001, np.nan)
            dist = np.sqrt(df['EyeTracker-x'].diff()**2 + df['EyeTracker-y'].diff()**2)
            velocity = (dist / time_diff).dropna()

            # Filter noise for threshold calculation
            v_clean = velocity[velocity <= np.percentile(velocity, 99)]

            # Store the 75th percentile for this file
            individual_thresholds.append(np.percentile(v_clean, 75))

            # Store all velocities for the histogram
            global_velocities.extend(velocity[velocity <= 2000].tolist())
    except:
        continue

# CALCULATE DYNAMIC THRESHOLD (Median of all file thresholds)
dynamic_final_threshold = np.median(individual_thresholds)

# --- 2. Plotting ---
plt.figure(figsize=(12, 7))

# Create the histogram
plt.hist(global_velocities, bins=100, color='#5D99C6', edgecolor='#2C3E50', alpha=0.8)

# Add the vertical lines using the dynamic value
plt.axvline(30, color='red', linestyle='--', linewidth=2, label='Static Threshold (30 px/s)')
plt.axvline(dynamic_final_threshold, color='green', linestyle='-', linewidth=2,
            label=f'Dynamic Generalized Median ({dynamic_final_threshold:.2f} px/s)')

#plt.title('Figure 2. Distribution of gaze velocities (in pixels/second)', fontsize=14, pad=20, y=-0.15)
plt.xlabel('Velocity (pixels/second)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right')
plt.xlim(0, 1400)

plt.tight_layout()
plt.show()

print(f"The dynamically calculated threshold is: {dynamic_final_threshold:.2f} px/s")

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML

merged_data_path = "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/merged_pilot_data"
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FIXATION_THRESHOLD = final_fixation_threshold
RT_MIN, RT_MAX = 522, 5000

all_results = []

files = sorted([f for f in os.listdir(merged_data_path) if f.endswith('.csv')])

print(f" Analysis on {len(files)} files...")

for f in files:
    full_path = os.path.join(merged_data_path, f)
    country = "Portugal" if f.lower().startswith('pt_') else "Romania"

    try:
        # Load data
        df = pd.read_csv(full_path, sep=None, engine='python')
        df.columns = [str(col).strip() for col in df.columns]

        # 1. Gaze Patterns
        time_diff = df['Timestamp'].diff() / 1000.0
        time_diff = time_diff.where(time_diff > 0.001, np.nan)
        velocity = np.sqrt(df['EyeTracker-x'].diff()**2 + df['EyeTracker-y'].diff()**2) / time_diff
        velocity_clean = velocity.fillna(0).replace([np.inf, -np.inf], 0)

        fix_pct = (velocity_clean <= FIXATION_THRESHOLD).mean() * 100

        # 2. Performance Logic
        hit_rate, avg_rt, total_objs = 0, 0, 0
        if 'ObjectState' in df.columns:
            apps = df[df['ObjectState'] == 'Appear']
            clicks = df[df['ObjectName'] == 'Mouse Click']
            total_objs = len(apps)

            rts = []
            for _, app in apps.iterrows():
                valid = clicks[(clicks['Timestamp'] > app['Timestamp'] + RT_MIN) &
                               (clicks['Timestamp'] < app['Timestamp'] + RT_MAX)]
                if not valid.empty:
                    rts.append(valid.iloc[0]['Timestamp'] - app['Timestamp'])

            if total_objs > 0:
                hit_rate = (len(rts) / total_objs) * 100
                avg_rt = np.mean(rts) if rts else 0

        # 3. Spatial Usage
        x_range = df['EyeTracker-x'].max() - df['EyeTracker-x'].min()
        y_range = df['EyeTracker-y'].max() - df['EyeTracker-y'].min()
        usage = (x_range * y_range) / (SCREEN_WIDTH * SCREEN_HEIGHT) * 100

        all_results.append({
            'Filename': f,
            'Country': country,
            'Hits %': round(hit_rate, 1),
            'RT (ms)': round(avg_rt, 0),
            'Fixation %': round(fix_pct, 1),
            'Screen %': round(usage, 1),
            'Objects': f"{len(rts)}/{total_objs}"
        })

    except Exception:
        continue

results_df = pd.DataFrame(all_results)

plt.figure(figsize=(16, 5))

# Plot A: Hit Rate vs Fixation Stability
plt.subplot(1, 2, 1)
sns.scatterplot(data=results_df, x='Fixation %', y='Hits %', hue='Country', style='Country', s=100)
plt.title('Gaze Stability vs. Task Success')
plt.grid(True, alpha=0.2)

# Plot B: Reaction Time Distribution
plt.subplot(1, 2, 2)
sns.kdeplot(data=results_df[results_df['RT (ms)'] > 0], x='RT (ms)', hue='Country', fill=True)
plt.title('Reaction Time Density (Portugal vs Romania)')

plt.tight_layout()
plt.show()

# FULL DATA TABLE (Styled for direct viewing)
print("\n" + "FULL INDIVIDUAL FILE RESULTS".center(90))
print(f"{'Filename':<50} | {'Hits %':<8} | {'RT (ms)':<8} | {'Fix %':<8} | {'Usage %':<8} | {'Objects'}")

for _, row in results_df.iterrows():
    # Highlight low success files in simple text logic
    status = "!" if row['Hits %'] < 50 else " "
    print(f"{row['Filename'][:49]:<50} | {row['Hits %']:<8} | {row['RT (ms)']:<8} | {row['Fixation %']:<8} | {row['Screen %']:<8} | {row['Objects']} {status}")

print(f"Summary: Processed {len(results_df)} files.")


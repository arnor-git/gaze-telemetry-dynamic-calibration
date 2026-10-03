for this import os

readme_content = """# Time Series Eye Tracking Analysis - Pilot 3 Data

This project processes, cleans, and analyzes eye-tracking and interaction time series data from pilot study experiments conducted across schools in **Portugal (pt)** and **Romania (ro)**.

## Project Pipeline

1. **Data Segregation & Identification** (`oHbmcuqbko-v`)
   - Scans source datasets to group files belonging to identical subjects.
   - Identifies subjects containing structured triplets of session files for consistent comparison.

2. **Data Cleaning & Normalization** (`xMeuYwLllBdD`)
   - Parses raw CSV files (detecting semi-colon and comma separators automatically).
   - Extracts screen coordinates from text formatted strings like `EyeTracker` and `GameObjectPos (Screen Coordinates)` into coordinate float values: `EyeTracker-x`, `EyeTracker-y`, `obj_x`, `obj_y`.
   - Standardizes the structure by removing invalid or missing gaze coordinates.

3. **Subject Merging & Standardization** (`BaiIjLD0lboN`)
   - Aggregates and merges processed datasets from regional folders into a unified `merged_pilot_data/` repository.
   - Normalizes filenames with clear geographic prefixes (`pt_` and `ro_`) for seamless comparative analysis.

4. **Dynamic Gaze Parameter Calibration** (`YOrTioeBC-Cp`, `6tQcG9SglQkV`)
   - **Dynamic Fixation Velocity Threshold**: Calculates instantaneous gaze velocity vectors. Rather than relying on a static assumption (e.g. 30 px/s), it computes a **dynamic generalized median threshold** of **483.70 px/s** across all sessions.
   - **Reaction Time Boundaries**: Sets realistic action observation windows (Min RT: ~382 ms, Max RT: ~13,564 ms) to analyze when a user registered and successfully reacted to targets.

5. **Task Success & Engagement Metrics** (`5AEzUWMkI3EW`)
   - Evaluates cognitive success rate (`Hits %`) using physical button actions mapped to visual stimulus appearances.
   - Measures gaze stability (`Fixation %`) and spatial explorer rates (`Screen Coverage %`).
   - Generates visualizations mapping gaze stability to overall task success metrics.

## Verified Thresholds
- **Fixation Threshold**: 483.70 px/s
- **Target Scan Bounds**: 522 ms to 5000 ms
"""

# Save path
output_dir = "/content/drive/MyDrive/Time Series Analysis-Pilot 3 Data/"
os.makedirs(output_dir, exist_ok=True)
readme_path = os.path.join(output_dir, "README.md")

with open(readme_path, "w") as f:
    f.write(readme_content)

print(f"README.md successfully written to: {readme_path}")

import pandas as pd
import numpy as np

# Load your CSV file
df = pd.read_csv('../data/players_stats_cleaned.csv')

# Show the number of missing values per column

df['id'] = range(1, len(df) + 1)

# Save updated table if needed
df.to_csv('../data/players_stats_cleaned.csv', index=False)

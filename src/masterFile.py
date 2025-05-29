import pandas as pd
import numpy as np
import sqlite3 as sql

# Load all the cleaned data files
advanced = pd.read_csv('../data/advanced_stats_cleaned.csv')
all_nba = pd.read_csv('../data/all_NBA_sel.csv')
all_star = pd.read_csv('../data/all_star_sel.csv')
asg_mvp = pd.read_csv('../data/asg_MVP.csv')
dpoy = pd.read_csv('../data/DPOY.csv')
finals_mvp = pd.read_csv('../data/finals_MVP.csv')
mvp = pd.read_csv('../data/MVP.csv')
players = pd.read_csv('../data/players_data.csv')
stats = pd.read_csv('../data/players_stats_cleaned.csv')

# merge tables advanced, stat, and players based on id
stats_adv = stats.merge(advanced, on=['id'], how='left')
master = stats_adv.merge(players, on=['id'], how='left')
master = master.drop(columns=['player_url'])

# merge all_nba, all_star, asg_mvp, dpoy, finals_mvp, mvp
master = master.merge(all_nba, left_on='name', right_on='player', how='left')
master = master.merge(all_star, left_on='name', right_on='player', how='left')
master = master.merge(asg_mvp, left_on='name', right_on='player', how='left')
master = master.merge(dpoy, left_on='name', right_on='player',
                      how='left', suffixes=('', '_dpoy'))
master = master.drop(columns=['player'])
master = master.merge(finals_mvp, left_on='name',
                      right_on='player', how='left')
master = master.merge(mvp, left_on='name', right_on='player',
                      how='left', suffixes=('', '_mvp'))
master = master.drop(columns=['player'])

# drop duplicate columns
master = master.drop(columns=[
    'name_x', 'name_y', 'player_x', 'player_y',
    'league_x', 'league_y', 'games_y', 'league', 'league_dpoy', 'player_mvp', 'player_dpoy'
])

# rename columns
master = master.rename(
    columns={'games_x': 'games', 'total_selections': 'asg_selections'})

# fill certain columns with 0
cols_to_fill = [
    '1st', '2nd', '3rd', 'asg_selections', 'asg_mvp_count', 'dpoy_count', 'finals_mvp_count', 'mvp_count'
]

for col in cols_to_fill:
    master[col] = master[col].fillna(0.0).astype(float)


# dealing with stats that are none/null (remove the people who are not in the hall of fame, played before 1975, and have null stats)
hof_mask = master['hof'] == 1

non_hof_ok_mask = (master['hof'] == 0) & (
    (master['start_year'] >= 1975) | (master.notna().all(axis=1)))

final_mask = hof_mask | non_hof_ok_mask

master = master[final_mask]

# handle the rest of the null stats by assigning the median value to the null values based on the position
null_stat_cols = [
    'fg3', 'fg3_pct', 'fg3a_per_fga_pct',
    'orb', 'drb', 'stl', 'blk',
    'tov', 'orb_pct', 'drb_pct',
    'trb_pct', 'ast_pct', 'stl_pct',
    'blk_pct', 'tov_pct', 'usg_pct',
    'obpm', 'dbpm', 'bpm', 'vorp'
]

# Create two subsets for HoF and non-HoF
hof_df = master[master['hof'] == 1]
non_hof_df = master[master['hof'] == 0]

# Impute for HoF group (by position)
hof_imputed = hof_df.copy()
hof_imputed[null_stat_cols] = hof_df.groupby('pos')[null_stat_cols].transform(
    lambda x: x.fillna(x.median())
)

# Impute for non-HoF group (by position)
non_hof_imputed = non_hof_df.copy()
non_hof_imputed[null_stat_cols] = non_hof_df.groupby('pos')[null_stat_cols].transform(
    lambda x: x.fillna(x.median())
)

# Combine the two subsets back into one DataFrame
master = pd.concat([hof_imputed, non_hof_imputed], axis=0).sort_index()


# move to csv
master.to_csv('../data/master.csv', index=False)

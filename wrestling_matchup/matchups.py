import pandas as pd

def fixed_weight_classes_matchup(home_df, away_df, weight_classes):
    home_df['WeightClass'] = pd.cut(home_df['weight'], bins=weight_classes, labels=False)
    away_df['WeightClass'] = pd.cut(away_df['weight'], bins=weight_classes, labels=False)
    
    matchups = []
    for weight_class in home_df['WeightClass'].unique():
        home_group = home_df[home_df['WeightClass'] == weight_class]
        away_group = away_df[away_df['WeightClass'] == weight_class]

        # Ensure both groups have wrestlers in the weight class
        if not home_group.empty and not away_group.empty:
            sorted_home = home_group.sort_values(['age','experience'])
            sorted_away = away_group.sort_values(['age','experience'])
            pairs = list(zip(sorted_home['name'], sorted_away['name']))
            matchups.extend(pairs)

    return matchups


def maddison_system_matchup(home_df, away_df):
    sorted_home = home_df.sort_values('weight').reset_index(drop=True)
    sorted_away = away_df.sort_values('weight').reset_index(drop=True)
    
    # Make sure to only pair across the two sorted dataframes
    matchups = []
    for home, away in zip(sorted_home['name'], sorted_away['name']):
        matchups.append((home, away))

    return matchups

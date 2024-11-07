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
            # Sort by weight, then age, then experience
            sorted_home = home_group.sort_values(by=['weight', 'age', 'experience']).reset_index(drop=True)
            sorted_away = away_group.sort_values(by=['weight', 'age', 'experience']).reset_index(drop=True)
            
            # Handle cases where there are more home or away wrestlers
            min_length = min(len(sorted_home), len(sorted_away))
            
            # Pair the wrestlers by the sorted order
            pairs = list(zip(sorted_home['name'][:min_length], sorted_away['name'][:min_length]))
            matchups.extend(pairs)

    return matchups


def maddison_system_matchup(home_df, away_df):
    # Sort by weight for the Madison system
    sorted_home = home_df.sort_values('weight').reset_index(drop=True)
    sorted_away = away_df.sort_values('weight').reset_index(drop=True)
    
    matchups = []
    # Pair wrestlers in order of sorted weights
    for home, away in zip(sorted_home['name'], sorted_away['name']):
        matchups.append((home, away))

    return matchups

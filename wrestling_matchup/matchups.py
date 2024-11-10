import pandas as pd

def fixed_weight_classes_matchup(home_df, away_df, weight_classes):
    # Assign weight classes based on weight bins
    home_df['WeightClass'] = pd.cut(home_df['weight'], bins=weight_classes, labels=False)
    away_df['WeightClass'] = pd.cut(away_df['weight'], bins=weight_classes, labels=False)

    matchups = []
    
    for weight_class in home_df['WeightClass'].unique():
        home_group = home_df[home_df['WeightClass'] == weight_class]
        away_group = away_df[away_df['WeightClass'] == weight_class]

        # Ensure both groups have wrestlers in the weight class
        if not home_group.empty and not away_group.empty:
            # For each home wrestler, find the closest away wrestler based on all fields
            for _, home_row in home_group.iterrows():
                # Calculate the absolute differences between home and away wrestlers for weight, age, and experience
                away_group['weight_diff'] = abs(away_group['weight'] - home_row['weight'])
                away_group['age_diff'] = abs(away_group['age'] - home_row['age'])
                away_group['experience_diff'] = abs(away_group['experience'] - home_row['experience'])
                
                # Calculate the total difference (a sum of the differences)
                away_group['total_diff'] = away_group['weight_diff'] + away_group['age_diff'] + away_group['experience_diff']
                
                # Find the away wrestler with the smallest total difference
                closest_match = away_group.loc[away_group['total_diff'].idxmin()]
                
                # Pair home and away wrestlers and add to matchups
                matchups.append((home_row['name'], closest_match['name']))

                # Remove the away wrestler from the pool to avoid rematching
                away_group = away_group.drop(closest_match.name)

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

import pandas as pd

def fixed_weight_classes_matchup(home_wrestlers, away_wrestlers, weight_classes):
    matchups = []
    
    # Define stricter thresholds
    MAX_AGE_DIFF = 3      # Max age difference allowed (in years)
    MAX_WEIGHT_DIFF = 3   # Max weight difference allowed (in kg)
    
    # Iterate over DataFrame rows using iterrows
    for _, home_wrestler in home_wrestlers.iterrows():
        closest_match = None
        min_weight_diff = float('inf')
        min_age_diff = float('inf')
        
        for _, away_wrestler in away_wrestlers.iterrows():
            weight_diff = abs(home_wrestler['weight'] - away_wrestler['weight'])
            age_diff = abs(home_wrestler['age'] - away_wrestler['age'])
            exp_diff = abs(home_wrestler.get('experience', 0) - away_wrestler.get('experience', 0))
            
            # Skip matchups with age differences greater than the allowed limit
            if age_diff > MAX_AGE_DIFF or weight_diff > MAX_WEIGHT_DIFF:
                continue
            
            # Prioritize weight closeness, followed by age (within max allowed difference), and then experience
            if (weight_diff < min_weight_diff) or \
               (weight_diff == min_weight_diff and age_diff < min_age_diff) or \
               (weight_diff == min_weight_diff and age_diff == min_age_diff and exp_diff < exp_diff):
                min_weight_diff = weight_diff
                min_age_diff = age_diff
                closest_match = away_wrestler
        
        # Add to matchups if a suitable match was found
        if closest_match is not None:
            matchups.append((home_wrestler['name'], closest_match['name']))
            away_wrestlers = away_wrestlers[away_wrestlers['name'] != closest_match['name']]  # Remove matched wrestler

    return matchups



def maddison_system_matchup(home_df, away_df, max_weight_diff=5):
    # Sort by weight for the Madison system
    sorted_home = home_df.sort_values('weight').reset_index(drop=True)
    sorted_away = away_df.sort_values('weight').reset_index(drop=True)
    
    matchups = []
    used_away = []  # Track used away wrestlers
    
    # Iterate through home wrestlers to find the best possible match
    for home_index, home_row in sorted_home.iterrows():
        home_name = home_row['name']
        home_weight = home_row['weight']
        
        closest_away = None
        min_weight_diff = float('inf')
        
        # Find the closest away wrestler by weight
        for away_index, away_row in sorted_away.iterrows():
            if away_index not in used_away:  # Ensure the away wrestler is not already matched
                away_name = away_row['name']
                away_weight = away_row['weight']
                
                weight_diff = abs(home_weight - away_weight)
                
                # Only consider the away wrestler if the weight difference is within the threshold
                if weight_diff < min_weight_diff and weight_diff <= max_weight_diff:
                    closest_away = away_name
                    min_weight_diff = weight_diff
                    closest_away_index = away_index
        
        # If a valid match is found, add it to matchups
        if closest_away:
            matchups.append((home_name, closest_away))
            used_away.append(closest_away_index)  # Mark the away wrestler as used
    
    return matchups

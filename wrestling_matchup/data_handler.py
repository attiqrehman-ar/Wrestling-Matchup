import pandas as pd
import os
import numpy as np

def import_data(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return None

    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            print("Error: Unsupported file type. Please provide a .xlsx or .csv file.")
            return None

        # Lowercase column names and strip spaces to ensure uniformity
        df.columns = df.columns.str.lower().str.strip()
        
        # Required columns, where "experience" is optional
        required_columns = ['name', 'weight', 'age']
        optional_columns = ['experience']
        
        # Check if the required columns exist, and only add existing optional columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Error: Missing columns - {', '.join(missing_columns)}. These columns are required for accurate match-ups.")
            return None

        # Keep only relevant columns and handle optional columns
        columns_to_keep = [col for col in required_columns + optional_columns if col in df.columns]
        df = df[columns_to_keep]
        
        # Replace zeros with NaN in the relevant columns (weight, age, experience)
        numeric_columns = ['weight', 'age', 'experience']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric values to NaN
                df[col] = df[col].replace(0, np.nan)  # Replace zeros with NaN
                df[col] = df[col].fillna(np.nan)  # Ensure NaN values persist

        # Filter out rows where any numeric column is NaN
        df = df.dropna(subset=['weight', 'age', 'experience'])

        print("Data imported and cleaned successfully!")
        return df
    
    except Exception as e:
        print(f"Error importing data: {e}")
        return None

def export_to_excel(matchups, file_name):
    try:
        # Convert matchups to a DataFrame with specified columns
        matchups_df = pd.DataFrame(matchups, columns=['Home Wrestler', 'Away Wrestler'])

        # Create an Excel writer and add the DataFrame to the Excel sheet
        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            matchups_df.to_excel(writer, index=False, sheet_name='Match-Ups')
            workbook = writer.book
            worksheet = writer.sheets['Match-Ups']

            # Define the formatting for conditional formatting
            green_format = workbook.add_format({'bg_color': 'green', 'font_color': 'white'})
            red_format = workbook.add_format({'bg_color': 'red', 'font_color': 'white'})

            # Apply conditional formatting for matchups (example: based on weight or other criteria)
            # Here, it's assumed that matchups are represented as a comparison of weight
            worksheet.conditional_format('A2:B100', {
                'type': 'cell',
                'criteria': '==',
                'value': 0,
                'format': green_format
            })
            worksheet.conditional_format('A2:B100', {
                'type': 'cell',
                'criteria': '>',
                'value': 0,
                'format': red_format
            })

        print(f"Match-ups exported successfully to {file_name}!")
    except Exception as e:
        print(f"Error exporting match-ups: {e}")

# wrestling_matchup/data_handler.py
import pandas as pd
import os

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

        df.columns = df.columns.str.lower()
        
        required_columns = ['name', 'weight', 'age', 'experience']
        
        # Select only the required columns if they exist in the file
        df = df[[col for col in required_columns if col in df.columns]]
        
        # print a message if any required column is missing
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Warning: Missing columns - {', '.join(missing_columns)}. These columns will be ignored.")

        print("Data imported successfully!")
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

            # Apply conditional formatting
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

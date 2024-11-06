# wrestling_matchup/cli.py
from wrestling_matchup.data_handler import import_data, export_to_excel
from wrestling_matchup.matchups import fixed_weight_classes_matchup, maddison_system_matchup

def run_cli():
    print("Welcome to the Wrestling Match-Up Program!")
    print("1. Import Data")
    print("2. Create Match-Ups (Fixed Weight Classes)")
    print("3. Create Match-Ups (Maddison System)")
    print("4. Export Match-Ups to Excel")
    print("5. Exit")

    wrestlers_data = None
    matchups = []

    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            file_path = input("Enter the path to the Excel or CSV file: ")
            wrestlers_data = import_data(file_path)

        elif choice == '2':
            if wrestlers_data is not None:
                weight_classes = [0, 50, 60, 70, 80, 90]  # Define weight classes
                matchups = fixed_weight_classes_matchup(wrestlers_data, weight_classes)
                print("Match-Ups (Fixed Weight Classes):")
                for matchup in matchups:
                    print(matchup)
            else:
                print("Please import the data first.")

        elif choice == '3':
            if wrestlers_data is not None:
                matchups = maddison_system_matchup(wrestlers_data)
                print("Match-Ups (Maddison System):")
                for matchup in matchups:
                    print(matchup)
            else:
                print("Please import the data first.")

        elif choice == '4':
            if matchups:
                export_file = input("Enter the export file name (e.g., matchups.xlsx): ")
                export_to_excel(matchups, export_file)
            else:
                print("Please create match-ups first.")

        elif choice == '5':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

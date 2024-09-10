import pytesseract
import pandas as pd

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'F:\Programas\Tesseract-OCR\tesseract.exe'


def save_to_excel(data, excel_filename):
    # Create a new Excel writer object
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        # Iterate over each team in the dictionary
        for team, players in data.items():
            # Truncate team name if it exceeds 31 characters
            if len(team) > 31:
                truncated_team_name = team[:31]
            else:
                truncated_team_name = team
            # Prepare the data for the DataFrame
            df_data = []
            for player, stats in players.items():
                df_data.append([player] + stats)

            # Create a DataFrame with the appropriate columns
            df = pd.DataFrame(df_data, columns=['Player', 'M', 'PTS', 'TL', 'T2'])

            # Convert the 'PTS' column to numeric
            df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')

            # Write the DataFrame to a new sheet with the team name
            df.to_excel(writer, sheet_name=truncated_team_name, index=False)





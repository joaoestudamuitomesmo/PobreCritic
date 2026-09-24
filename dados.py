import kagglehub
import pandas as pd
import os

def coisar():
    # 1. Download the latest version of the dataset
    path = kagglehub.dataset_download("brunovr/metacritic-videogames-data")
    
    # 2. Automatically find the CSV file in the downloaded folder
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the downloaded dataset.")
        return
        
    # 3. Load the first CSV file found
    target_file = os.path.join(path, csv_files[0])
    print(f"Loading file: {csv_files[0]}...")
    
    df = pd.read_csv(target_file)
    print("First 5 records:\n", df.head(15))

# Run the function
coisar()
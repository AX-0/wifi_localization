import sys
import os
import pandas as pd

# python csv_combine.py "C:\Users\alanx\OneDrive - The University of Sydney (Students)\Thesis\Deep Learning\wifi_localization\data\csv"

def combine_csv_round(base_directory):
    # Iterate over all subdirectories within the base directory
    for subdir in os.listdir(base_directory):
        subdir_path = os.path.join(base_directory, subdir)
        
        if os.path.isdir(subdir_path):  # Check if it's a directory
            frames = []  # List to store dataframes
            print(f"Processing subdirectory: {subdir_path}")
            
            # Find all CSV files in this subdirectory
            for file in os.listdir(subdir_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(subdir_path, file)
                    df = pd.read_csv(file_path)
                    frames.append(df)
            
            # Check if there are any data frames to concatenate
            if frames:
                combined_df = pd.concat(frames, ignore_index=True)
                combined_file_path = os.path.join(subdir_path, 'combined.csv')
                combined_df.to_csv(combined_file_path, index=False)
                print(f"Combined CSV saved to {combined_file_path}")
            else:
                print(f"No CSV files found in {subdir_path}")
                
def combine_csv_mode(directory, filename):
    frames = []
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        combined_csv_path = os.path.join(subdir_path, 'combined.csv')
        if os.path.exists(combined_csv_path):
            df = pd.read_csv(combined_csv_path)
            frames.append(df)
    if frames:
        overall_combined_df = pd.concat(frames, ignore_index=True)
        overall_combined_file_path = os.path.join(directory, filename)
        overall_combined_df.to_csv(overall_combined_file_path, index=False)
        print(f"Final combined CSV saved to {overall_combined_file_path}")
        

def combine_final_csv_files(base_path, output_directory, output_filename='ultimate_combined.csv'):
    # List to store DataFrames
    frames = []

    # Map of directories to their respective CSV files
    csv_files = {
        'still': 'still.csv',
        'still_with_receiver': 'still_with_receiver.csv'
    }

    # Iterate over the csv_files dictionary and read the specified CSV files
    for directory, filename in csv_files.items():
        csv_path = os.path.join(base_path, directory, filename)
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            frames.append(df)
        else:
            print(f"No {filename} found in {csv_path}")

    # Concatenate all collected DataFrames
    if frames:
        combined_df = pd.concat(frames, ignore_index=True)
        output_file_path = os.path.join(base_path, output_directory, output_filename)
        combined_df.to_csv(output_file_path, index=False)
        print(f"All CSV files have been combined into {output_file_path}")
    else:
        print("No CSV files were combined.")

# Base path to your directories
base_path = sys.argv[1]

print(base_path)

# Directory names under the base path
directories = ['still', 'still_with_receiver']

# Combine CSV files in each directory
for directory in directories:
    directory_path = os.path.join(base_path, directory)
    combine_csv_round(directory_path)
    
# Combine all combined CSVs in each main directory
for directory in directories:
    dir_path = os.path.join(base_path, directory)
    combine_csv_mode(dir_path, f"{directory}.csv")

combine_final_csv_files(base_path, output_directory='.')
import sys
import os
import pandas as pd

from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.cluster import DBSCAN
import hdbscan

# python csv_combine.py "C:\Users\alanx\OneDrive - The University of Sydney (Students)\Thesis\Deep Learning\wifi_localization\data\csv"
# python3 csv_combine.py /home/alan-xie/Documents/Thesis/wifi_localization/data/csv
# python3.10 csv_combine.py /home/alan-xie/Desktop/wifi_localization/data/csv

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
                    if 'combined' in file:
                        continue
                    
                    print(f"processing file: {file}")
                    file_path = os.path.join(subdir_path, file)
                    df = pd.read_csv(file_path)

                    ##############################################################
                    variances = df.var()

                    low_variance_cols = variances[variances < 5e-3].index.tolist()

                    # df.drop(low_variance_cols, axis=1, inplace=True)
                    
                    # df.drop(['rssi3', 'nr', 'num_tones', 'bandWidth', 'noise_floor', 'err_info', 'channel', 'csi_len', 'rate', 'payload_length', 'block_length'], axis=1, inplace=True)
                    # df.drop('timestamps', axis=1, inplace=True)
                    # print(df.head())
                    
                    # df = df[df['nc'] == 1]
                    
                    df_nc1 = df.loc[df['nc'] == 1].copy()
                    df_nc2 = df.loc[df['nc'] == 2].copy()

                    
                    if not df_nc1.empty:
                        ant1_amplitude = df_nc1[['subcarriers', 'ant1_amplitude']].values
                        ant1_dbscan = hdbscan.HDBSCAN(min_samples=2*df_nc1.shape[1], core_dist_n_jobs=-1)
                        ant1_dbscan.fit(ant1_amplitude)
                        df_nc1['ant1_amplitude_cluster'] = ant1_dbscan.labels_
                        
                        ant2_amplitude = df_nc1[['subcarriers', 'ant2_amplitude']].values
                        ant2_dbscan = hdbscan.HDBSCAN(min_samples=2*df_nc1.shape[1], core_dist_n_jobs=-1)
                        ant2_dbscan.fit(ant2_amplitude)
                        df_nc1['ant2_amplitude_cluster'] = ant2_dbscan.labels_
                        
                        df_nc1.drop(df_nc1[df_nc1.ant1_amplitude_cluster < 0].index, inplace=True)
                        df_nc1.drop(df_nc1[df_nc1.ant2_amplitude_cluster < 0].index, inplace=True)
                        
                    if not df_nc1.empty:
                        features_to_scale = ['ant1_amplitude', 'ant2_amplitude', 'ant1_phase', 'ant2_phase', 'rssi', 'rssi1', 'rssi2']
                        scaler = StandardScaler()

                        df_nc1[features_to_scale] = scaler.fit_transform(df_nc1[features_to_scale])
                        
                        
                        
                    if not df_nc2.empty:
                        ant1_amplitude = df_nc2[['subcarriers', 'ant1_amplitude']].values
                        ant1_dbscan = hdbscan.HDBSCAN(min_samples=2*df_nc2.shape[1], core_dist_n_jobs=-1)
                        ant1_dbscan.fit(ant1_amplitude)
                        df_nc2['ant1_amplitude_cluster'] = ant1_dbscan.labels_
                        
                        ant2_amplitude = df_nc2[['subcarriers', 'ant2_amplitude']].values
                        ant2_dbscan = hdbscan.HDBSCAN(min_samples=2*df_nc2.shape[1], core_dist_n_jobs=-1)
                        ant2_dbscan.fit(ant2_amplitude)
                        df_nc2['ant2_amplitude_cluster'] = ant2_dbscan.labels_
                        
                        df_nc2.drop(df_nc2[df_nc2.ant1_amplitude_cluster < 0].index, inplace=True)
                        df_nc2.drop(df_nc2[df_nc2.ant2_amplitude_cluster < 0].index, inplace=True)
                        
                    # if not df_nc2.empty:
                    #     features_to_scale = ['ant1_amplitude', 'ant2_amplitude', 'ant1_phase', 'ant2_phase', 'rssi', 'rssi1', 'rssi2']
                    #     scaler = StandardScaler()

                    #     df_nc2[features_to_scale] = scaler.fit_transform(df_nc2[features_to_scale])
                    ##############################################################
    
                    frames.append(df_nc1)
                    frames.append(df_nc2)
            
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
directories = ['still'] #, 'still_with_receiver']

# Combine CSV files in each directory
# for directory in directories:
#     directory_path = os.path.join(base_path, directory)
#     combine_csv_round(directory_path)
    
# Combine all combined CSVs in each main directory
for directory in directories:
    dir_path = os.path.join(base_path, directory)
    combine_csv_mode(dir_path, f"{directory}.csv")

# combine_final_csv_files(base_path, output_directory='.')
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
import hdbscan

def apply_dbscan(data_path, output_directory):
    data = pd.read_csv(data_path)
    
    variances = data.var()

    low_variance_cols = variances[variances < 5e-3].index.tolist()

    data.drop(low_variance_cols, axis=1, inplace=True)
    data.drop(['csi_len', 'rate', 'payload_length', 'block_length'], axis=1, inplace=True)
    data.drop('timestamps', axis=1, inplace=True)
    
    features_to_scale = ['ant1_phase', 'ant2_phase', 'rssi', 'rssi1', 'rssi2']
    scaler = StandardScaler()

    data[features_to_scale] = scaler.fit_transform(data[features_to_scale])
    
    amplitudes = data[['subcarriers', 'ant1_amplitude']].values
    dbscan = hdbscan.HDBSCAN(min_samples=10, core_dist_n_jobs=-1)
    
    dbscan.fit(amplitudes)
    
    data.drop(data[data.cluster < 0].index, inplace=True)
    

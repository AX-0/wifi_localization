# Indoor Device-Free Localization Using Wi-Fi Signals

## Overview
This is my honours thesis project of my Bachelor of Engineering (Software) degree at the University of Sydney.

This project focuses on enhancing indoor device-free localization using Wi-Fi Channel State Information (CSI) and Deep Neural Networks (DNNs). The approach aims to utilize the existing Wi-Fi infrastructure to accurately predict the location of individuals or objects in indoor environments without requiring additional hardware or wearable devices.

## File Structure of Data
![alt text](file_structure.png)

## Project Structure
The design of this project is divided into four main stages:
1. **Data Collection**
2. **Data Translation and Labeling**
3. **Data Preprocessing**
4. **Neural Network Model Training**
![alt text](overview_flowchart.png)

### 1. Data Collection
- **Environment:** Data were collected in a controlled lab environment, structured with rows of desks, computers, and other objects to create a realistic indoor space.
- **Setup:** Two Wi-Fi-enabled devices were used—one as the sender and the other as the receiver. 
- **Scenarios:** Data were collected in two scenarios: 
  1. With a stationary receiver.
  2. With the receiver carried by the collector.
- **Rounds:** Data were gathered at 32 specific points, with ten rounds of collection for robustness. Each data point generated a .DAT file, storing 1000 Wi-Fi packets captured using the Atheros CSI Tool.

### 2. Data Translation and Labeling
- csi2csv -> convert.m
- data_processing -> csv_combine_XXX.py
- **Conversion:** Raw CSI data collected in .DAT format were converted into .CSV format using custom MATLAB scripts.
- **Labeling:** Each data file was labeled with its corresponding coordinates and an indicator for whether the data was collected with or without the receiver being carried.

### 3. Data Preprocessing
![alt text](preprocessing_flowchart.png)
- **Standardization:** Using Scikit-learn’s StandardScaler, features were standardized to improve model performance.
- **Amplitude Denoising:** Two methods were used to preprocess amplitude data:
  - **Method 1:** Applied Hierarchical Density-Based Spatial Clustering of Applications with Noise (HDBSCAN) to remove noise and identify clusters.
  - **Method 2:** Combined Savitzky-Golay filtering for noise smoothing with HDBSCAN for clustering, enhancing data clarity.
- **Dimensionality Reduction:** Principal Component Analysis (PCA) was used to reduce dimensionality and retain essential features for model input.

### 4. Neural Network Model Training
- **Architecture:** The DNN model consists of an input layer, four fully connected hidden layers (with 512, 1024, 512, and 1024 neurons), and an output layer predicting the x and y coordinates.
- **Activation Function:** ReLU activation is used for non-linearity in hidden layers.
- **Optimizer:** The Adam optimizer is employed for efficient training, with Mean Absolute Error (MAE) and a custom Euclidean Distance Loss as evaluation metrics.
- **Training Strategy:** The data is split into 60% training, 20% validation, and 20% testing sets. Early stopping and model checkpointing are implemented to optimize training and prevent overfitting.
- **Computational Setup:** Training was performed on a GPU to expedite computations, but the large dataset still led to long training times.

## Results Summary
- **Method 1:** Utilized only HDBSCAN, resulting in higher noise and lower accuracy metrics.
- **Method 2:** Combined Savitzky-Golay filtering with HDBSCAN, significantly reducing noise and improving accuracy.

## Future Enhancements
For potential improvements, consider integrating the Angle of Arrival (AoA) approach with Deep Convolutional Neural Networks (DCNN) and exploring adaptive filtering methods for NC2 data.

## References
- Atheros CSI Tool: [Link](https://wands.sg/research/wifi/AtherosCSI/)
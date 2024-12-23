# -*- coding: utf-8 -*-
"""earthquake_cnn_lstm.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Dlq7IGdXAZ_ZuYa1NkXTHEmbDhHvKAyc
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, LSTM, Flatten
from tensorflow.keras.optimizers import Adam
import seaborn as sns
import matplotlib.pyplot as plt

file_path = '/content/Earthquakes.csv' #kaggle dataset (https://www.kaggle.com/datasets/ankitd7752/indian-subcontinent-earthquake-data-2000-to-2024)
earthquakes = pd.read_csv(file_path) #loading data
earthquakes = earthquakes.dropna() #dropping null values

#heatmap of the data
plt.figure(figsize=(10, 6))
sns.scatterplot(x='depth', y='mag', hue='mag', palette='viridis', data=earthquakes)
plt.title('Magnitude vs Depth of Earthquakes')
plt.xlabel('Depth (km)')
plt.ylabel('Magnitude')
plt.show()

# Training
X = earthquakes[['depth', 'latitude', 'longitude']]  # Example features, adjust as necessary
y = earthquakes['mag']  # Target variable
scaler = StandardScaler() #feature scaling
X_scaled = scaler.fit_transform(X)

X_scaled = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1) #reshaping data for CNN
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42) #splitting the data

def CNN(X_train, X_test, y_train, y_test):
  model = Sequential()
  model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1), padding='same')) #1D CNN
  model.add(MaxPooling1D(pool_size=1)) #maxpooling layer
  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dense(1))  # Output layer for regression
  model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mae']) #compiling the model
  history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test)) #model training
  cnn_test_loss, cnn_test_mae = model.evaluate(X_test, y_test)
  return cnn_test_loss, cnn_test_mae

def CNN_LSTM(X_train, X_test, y_train, y_test):
  model = Sequential()
  model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1), padding='same')) #1D CNN
  model.add(MaxPooling1D(pool_size=1)) #maxpooling layer
  #model.add(Flatten()) #flatten the output
  model.add(LSTM(50, return_sequences=False)) #LSTM layer
  model.add(Dense(128, activation='relu')) #fully connected layers
  model.add(Dense(1))  # Output layer for regression
  model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mae']) #compile output
  history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test)) #train model
  cnn_lstm_test_loss, cnn_lstm_test_mae = model.evaluate(X_test, y_test)
  return cnn_lstm_test_loss, cnn_lstm_test_mae

cnn_test_loss, cnn_test_mae= CNN(X_train, X_test, y_train, y_test)
cnn_lstm_test_loss, cnn_lstm_test_mae= CNN_LSTM(X_train, X_test, y_train, y_test)

print(f'CNN model Test Loss: {cnn_test_loss}')
print(f'CNN Test MAE: {cnn_test_mae}')
print(f'CNN-LSTM model Test Loss: {cnn_lstm_test_loss}')
print(f'CNN-LSTM Test MAE: {cnn_lstm_test_mae}')
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

# Dummy dataset (RGB averages)
X = np.array([
    [200,180,170], # fair
    [210,190,180],
    [150,120,100], # medium
    [130,100,80],
    [80,60,50],    # dark
    [60,40,30]
])

y = np.array([0,0,1,1,2,2])

X = X / 255.0

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

model = Sequential([
    Dense(16, activation='relu', input_shape=(3,)),
    Dense(8, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=50)

model.save("model/skin_tone_model.h5")
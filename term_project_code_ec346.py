# -*- coding: utf-8 -*-
"""TERM PROJECT CODE - EC346

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19hzvrRak0RDFpr7coKVyzAWFMKqe9DLQ

### **Imported libraries**
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix, precision_score, f1_score, precision_recall_curve, roc_curve, roc_auc_score, auc
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical
from skimage import io, color, transform
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import seaborn as sns

"""### ***Base Model 1*** : *K-Nearest Neighbours (KNN)*"""

image_folder = '/content/drive/MyDrive/DatasetForUseKNN'

# Function to load and preprocess images
def load_and_preprocess_images(folder_path):
    images = []
    labels = []

    for label in ['Bleeding', 'NonBleeding']:                                   # Labeling 2 classes as Bleeding/NonBleeding using CamelCase
        for i in range(1, 1310):                                                # There are 1309 images per class
            image_path = f"{folder_path}/Images_{label}/img- ({i}).png"
            img = io.imread(image_path)
            img_gray = color.rgb2gray(img)
            img_resized = transform.resize(img_gray, (8, 8), anti_aliasing=True)

            images.append(img_resized.flatten())
            labels.append(label)

    return np.array(images), np.array(labels)

# Load and preprocess your image data
X_custom, y_custom = load_and_preprocess_images(image_folder)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_custom, y_custom, test_size=0.2, random_state=42)

# Initialize the KNN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=3)

# Train the classifier
knn_classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = knn_classifier.predict(X_test)

# Evaluate the KNN performance
KNN_accuracy = accuracy_score(y_test, y_pred)
print(f"KNN Accuracy: {KNN_accuracy:.2f}")

# Example: Predict a new image
# A separate .png file has been uploaded in the session storage in Google Colab from the dataset for prediction
new_image_path = '/content/img- (1113).png'
new_img = io.imread(new_image_path)
new_img_gray = color.rgb2gray(new_img)
new_img_resized = transform.resize(new_img_gray, (8, 8), anti_aliasing=True)
new_image_flatten = new_img_resized.flatten().reshape(1, -1)

# Make a prediction on the new image
prediction = knn_classifier.predict(new_image_flatten)
print(f"Predicted class: {prediction[0]}")

# Visualize the new image
plt.figure(figsize=(4, 4))
plt.imshow(new_img_resized, cmap=plt.cm.gray_r, interpolation='nearest')
plt.title(f"Predicted Class: {prediction[0]}")
plt.show()

"""### ***Base Model 2*** : *Support Vector Machine (SVM)*"""

image_folder = '/content/drive/MyDrive/DatasetForUseKNN'

# Function to load and preprocess images
def load_and_preprocess_images(folder_path):
    images = []
    labels = []

    for label in ['Bleeding', 'NonBleeding']:                                    # Labeling 2 classes as Bleeding/NonBleeding using CamelCase
        for i in range(1, 1310):                                                 # There are 1309 images per class
            image_path = f"{folder_path}/Images_{label}/img- ({i}).png"
            img = io.imread(image_path)
            img_gray = color.rgb2gray(img)
            img_resized = transform.resize(img_gray, (8, 8), anti_aliasing=True)

            images.append(img_resized.flatten())
            labels.append(label)

    return np.array(images), np.array(labels)

# Load and preprocess your image data
X_custom, y_custom = load_and_preprocess_images(image_folder)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_custom, y_custom, test_size=0.2, random_state=42)

# Flatten the image data for SVM
X_train_flatten = X_train.reshape(X_train.shape[0], -1)
X_test_flatten = X_test.reshape(X_test.shape[0], -1)

# Initialize the SVM classifier
svm_classifier = SVC(kernel='rbf', C=10.0, gamma='scale')  # You can experiment with different kernels and C values

# Train the classifier
svm_classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = svm_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f" SVM Accuracy: {accuracy:.2f}")

# Example: Predict a new image
# A separate .png file has been uploaded in the session storage in Google Colab from the dataset for prediction
new_image_path = '/content/img- (1113).png'
new_img = io.imread(new_image_path)
new_img_gray = color.rgb2gray(new_img)
new_img_resized = transform.resize(new_img_gray, (8, 8), anti_aliasing=True)
new_image_flatten = new_img_resized.flatten().reshape(1, -1)

# Make a prediction on the new image
prediction = svm_classifier.predict(new_image_flatten)
print(f"Predicted class: {prediction[0]}")

# Visualize the new image
plt.figure(figsize=(4, 4))
plt.imshow(new_img_resized, cmap=plt.cm.gray_r, interpolation='nearest')
plt.title(f"Predicted class: {prediction[0]}")
plt.show()

"""### *Base Model 3* : *Convolutional Neural Network (CNN)*"""

image_folder = '/content/drive/MyDrive/DatasetForUseKNN'

# Function to load and preprocess images
def load_and_preprocess_images(folder_path):
    images = []
    labels = []

    for label in range(2):                                                      # Assuming you have 2 classes (bleeding and non-bleeding)
        for i in range(1, 1310):                                                # Assuming you have 1309 images per class
            if label == 0:
              wlabel = "Bleeding"
            else:
              wlabel = "NonBleeding"
            image_path = f"{folder_path}/Images_{wlabel}/img- ({i}).png"
            img = image.load_img(image_path, target_size=(64, 64))              # Resize images to a consistent size
            img_array = image.img_to_array(img)
            images.append(img_array)
            labels.append(label)

    return np.array(images), np.array(labels)

# Load and preprocess your image data
X, y = load_and_preprocess_images(image_folder)

# FEATURE EXTRACTION for CNN
# Convert labels to categorical (one-hot encoding)
y_categorical = to_categorical(y, num_classes=2)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

# Build the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(2, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Data augmentation to generate more training samples
datagen = ImageDataGenerator(rotation_range=20, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
datagen.fit(X_train)

# Train the model
model.fit_generator(datagen.flow(X_train, y_train, batch_size=32), epochs=10, validation_data=(X_test, y_test))

# Evaluate the model on the test set
y_pred = np.argmax(model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)
accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Example: Predict a new image
# A separate .png file has been uploaded in the session storage in Google Colab from the dataset for prediction
new_image_path = '/content/img- (1113).png'
new_img = image.load_img(new_image_path, target_size=(64, 64))
new_img_array = image.img_to_array(new_img)
new_img_array = np.expand_dims(new_img_array, axis=0)
new_img_array /= 255.0  # Normalize pixel values
prediction = model.predict(new_img_array)
predicted_class = np.argmax(prediction[0])
print(type(predicted_class))
if predicted_class == 0:
  predicted_class = 'Bleeding'
if predicted_class == 1:
  predicted_class = 'Non-Bleeding'

# Visualize the new image
plt.imshow(new_img)
plt.title(f"Predicted class: {predicted_class}")
plt.show()

"""### ***Base Model 4*** : *Decision Trees (DT)*"""

image_folder = '/content/drive/MyDrive/DatasetForUseKNN'

# Function to load and preprocess images
def load_and_preprocess_images(folder_path):
    images = []
    labels = []

    for label in ['Bleeding', 'NonBleeding']:                                   # Labeling 2 classes as Bleeding/NonBleeding using CamelCase
        for i in range(1, 1310):                                                # There are 1309 images per class
            image_path = f"{folder_path}/Images_{label}/img- ({i}).png"
            img = io.imread(image_path)
            img_gray = color.rgb2gray(img)
            img_resized = transform.resize(img_gray, (8, 8), anti_aliasing=True)

            images.append(img_resized.flatten())
            labels.append(label)

    return np.array(images), np.array(labels)

# Load and preprocess your image data
X_custom, y_custom = load_and_preprocess_images(image_folder)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_custom, y_custom, test_size=0.2, random_state=42)

# Initialize the Decision Tree classifier
dt_classifier = DecisionTreeClassifier(random_state=42)

# Train the classifier
dt_classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = dt_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Example: Predict a new image
# A separate .png file has been uploaded in the session storage in Google Colab from the dataset for prediction
new_image_path = '/content/img- (1113).png'
new_img = io.imread(new_image_path)
new_img_gray = color.rgb2gray(new_img)
new_img_resized = transform.resize(new_img_gray, (8, 8), anti_aliasing=True)
new_image_flatten = new_img_resized.flatten().reshape(1, -1)

# Make a prediction on the new image
prediction = dt_classifier.predict(new_image_flatten)
print(f"Predicted class: {prediction[0]}")

# Visualize the new image
plt.figure(figsize=(4, 4))
plt.imshow(new_img_resized, cmap=plt.cm.gray_r, interpolation='nearest')
plt.title(f"Predicted class: {prediction[0]}")
plt.show()

image_folder = '/content/drive/MyDrive/DatasetForUseKNN'

# Function to load and preprocess images
def load_and_preprocess_images(folder_path):
    images = []
    labels = []

    for label in range(2):
      if label == 0:
        wlabel = "Bleeding"
      else:
        wlabel = 'NonBleeding'                                                  # Assuming you have 2 classes (bleeding and non-bleeding)
      for i in range(1, 1310):
            image_path = f"{folder_path}/Images_{wlabel}/img- ({i}).png"
            img = io.imread(image_path)
            img_gray = color.rgb2gray(img)
            img_resized = transform.resize(img_gray, (8, 8), anti_aliasing=True)

            images.append(img_resized.flatten())
            labels.append(label)

    return np.array(images), np.array(labels)

# Load and preprocess your image data
X_custom, y_custom = load_and_preprocess_images(image_folder)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_custom, y_custom, test_size=0.2, random_state=42)

# Convert labels to categorical (one-hot encoding)
y_train_categorical = to_categorical(y_train, num_classes=2)
y_test_categorical = to_categorical(y_test, num_classes=2)

# Train KNN model
knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train, y_train)

# Train SVM model
svm_model = SVC(kernel='rbf', C=1.0, gamma='scale')
svm_model.fit(X_train, y_train)

# Train CNN model
cnn_model = Sequential()
cnn_model.add(Flatten(input_shape=(8, 8)))
cnn_model.add(Dense(128, activation='relu'))
cnn_model.add(Dense(2, activation='softmax'))
cnn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
cnn_X_train = X_train.reshape(-1, 8, 8)
cnn_X_test = X_test.reshape(-1, 8, 8)
cnn_model.fit(cnn_X_train, y_train_categorical, epochs=10, batch_size=32)

# Train Decision Tree model
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Make predictions using each model
knn_predictions = knn_model.predict(X_test)
svm_predictions = svm_model.predict(X_test)
cnn_predictions = np.argmax(cnn_model.predict(cnn_X_test), axis=1)
dt_predictions = dt_model.predict(X_test)

# Combine predictions using simple averaging
ensemble_predictions = np.round((knn_predictions + svm_predictions + cnn_predictions + dt_predictions) / 4)

# Evaluate the ensemble performance
# Accuracy
ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
print(f"Ensemble Accuracy: {ensemble_accuracy:.2f}")

# Precision
ensemble_precision = precision_score(y_test, ensemble_predictions)
print(f"Ensemble Precision: {ensemble_precision:.2f}")

# Recall
ensemble_recall = recall_score(y_test, ensemble_predictions)
print(f"Ensemble Recall: {ensemble_recall:.2f}")

# F1 Score
ensemble_f1_score = f1_score(y_test, ensemble_predictions)
print(f"Ensemble F1 Score: {ensemble_f1_score:.2f}")

# Confusion Matrix
ensemble_ConfusionMatrix = confusion_matrix(y_test, ensemble_predictions)
fig, ax = plt.subplots(figsize=(6,6))         # Sample figsize in inches
sns.set(font_scale=1.6)
sns.heatmap(ensemble_ConfusionMatrix, annot=True, ax=ax)
print(f"Ensemble Confusion Matrix:\n{ensemble_ConfusionMatrix}")

# PLOTTING GRAPHS

# ROC Curve
plt.figure(figsize=(8, 6))

fpr, tpr, _ = roc_curve(y_test, ensemble_predictions)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'Ensemble (AUC = {roc_auc:.2f})', linestyle='--')

plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

# Precision-Recall Curve
plt.figure(figsize=(8, 6))

precision, recall, _ = precision_recall_curve(y_test, ensemble_predictions)
pr_auc = auc(recall, precision)
plt.plot(recall, precision, label=f'Ensemble (AUC = {pr_auc:.2f})', linestyle='--')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc='lower left')
plt.show()
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import os
import pickle

# Load and preprocess the dataset
def load_images(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, (64, 64))  # Resize to 64x64
            img = cv2.GaussianBlur(img, (5, 5), 0)  # Reduce noise
            img = cv2.Canny(img, 100, 200)  # Edge detection
            images.append(img.flatten())  # Flatten to 1D
            labels.append(label)
    return images, labels

# Paths to "pointing up" and "pointing down" datasets
up_folder = os.path.join(os.getcwd(), 'up_images')
down_folder = os.path.join(os.getcwd(), 'down_images')

# Load the images
up_images, up_labels = load_images(up_folder, 1)  # Label '1' for pointing up
down_images, down_labels = load_images(down_folder, 0)  # Label '0' for pointing down

# Combine datasets
X = np.array(up_images + down_images)
y = np.array(up_labels + down_labels)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple SVM classifier
clf = SVC(kernel='linear', probability=True)
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

#Save model for access later
model = 'pointing_detection.pkl'
with open(model, 'wb') as file:
    pickle.dump(clf, file)
    

# Test on a new image
def classify_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (64, 64))
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Canny(img, 100, 200)
    img_flatten = img.flatten().reshape(1, -1)
    prediction = clf.predict(img_flatten)
    return "Pointing Up" if prediction == 1 else "Pointing Down"

# Example test
test_image_path = os.path.join(os.getcwd(),'test_images')
for item in os.listdir(test_image_path):
    image_path = os.path.join(test_image_path, item)
    print(classify_image(image_path), item)


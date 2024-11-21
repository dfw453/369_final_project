import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
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
neutral_folder = os.path.join(os.getcwd(), 'neutral_images')

# Load the images
up_images, up_labels = load_images(up_folder, 1)  # Label '1' for pointing up
down_images, down_labels = load_images(down_folder, 0)  # Label '0' for pointing down
neutral_images, neutral_labels = load_images(neutral_folder, 2)

# Combine datasets
X = np.array(up_images + down_images + neutral_images)
y = np.array(up_labels + down_labels + neutral_labels)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 0, stratify = y)

# Train a simple SVM classifier
clf = SVC(kernel = 'linear', probability=True)
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

#Save model for access later
model = 'pointing_detection_svm.pkl'
with open(model, 'wb') as file:
    pickle.dump(clf, file)

# Evaluating optimal number of neighbors
# for i in range(1, 30):
#     clf2 = KNeighborsClassifier(n_neighbors = i)
#     clf2.fit(X_train, y_train)
#     y_pred2 = clf2.predict(X_test)
#     print(f'Accuracy: {accuracy_score(y_test, y_pred2):.2f}', i)

# Training K- Nearest Neighbors Model
clf2 = KNeighborsClassifier(n_neighbors = 23)
clf2.fit(X_train, y_train)
y_pred2 = clf2.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred2):.2f}")
with open('pointing_detection_knn.pkl', 'wb') as file:
    pickle.dump(clf2, file)

# Training AdaBoost classifier
base_model = DecisionTreeClassifier(max_depth = 1)
adaboost = AdaBoostClassifier(base_model, n_estimators = 100, learning_rate = 1, random_state = 0)
adaboost.fit(X_train, y_train)
y_pred3 = adaboost.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred3):.2f}")
with open('pointing_detection_adaboost.pkl', 'wb') as file:
    pickle.dump(adaboost, file)

# Training MLP Classifier
X_train = X_train / 255.0
X_test = X_test / 255.0
mlp = MLPClassifier(hidden_layer_sizes = (64,32), activation = 'relu', solver = 'adam', max_iter = 500, random_state = 0)
mlp.fit(X_train, y_train)
y_pred4 = mlp.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred4):.2f}")
with open('pointing_detection_mlp.pkl', 'wb') as file:
    pickle.dump(mlp, file)

# Test on a new image
def classify_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (64, 64))
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Canny(img, 100, 200)
    img_flatten = img.flatten().reshape(1, -1)
    prediction = adaboost.predict(img_flatten)
    if prediction == 1:
        return 'Pointing up'
    elif prediction == 2:
        return 'Neutral'
    return 'Pointing Down'

# Example test
test_image_path = os.path.join(os.getcwd(),'test_images')
for item in os.listdir(test_image_path):
    image_path = os.path.join(test_image_path, item)
    print(classify_image(image_path), item)


# def preprocess_frame(frame):
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
#     frame = cv2.resize(frame, (64, 64))  # Resize to 64x64
#     frame = cv2.GaussianBlur(frame, (5, 5), 0)  # Blur to reduce noise
#     frame = cv2.Canny(frame, 100, 200)  # Edge detection
#     return frame.flatten()  # Flatten to 1D array for prediction

# cap = cv2.VideoCapture(1)
# frame_count = 0
# while True:
#     ret, frame = cap.read()
#     cv2.imshow('Recording Video', frame)
#     frame_filename = os.path.join(down_folder, f'frame_ {frame_count:04d}.jpg')
#     cv2.imwrite(frame_filename, frame)
#     frame_count += 1
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
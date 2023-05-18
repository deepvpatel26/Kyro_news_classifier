import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib

# Step 1: Load the dataset
data = pd.read_csv('NewsTrain.csv')

# Step 2: Prepare the data
X = data['Text']
y = data['Category']

# Step 3: Perform TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Step 4: Train the model
model = LinearSVC()
model.fit(X, y)

# Step 5: Save the trained model
joblib.dump(model, 'news_classifier_model.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')

# Step 6: Load the trained model and vectorizer
model = joblib.load('news_classifier_model.joblib')
vectorizer = joblib.load('vectorizer.joblib')

# Step 7: Predict the category for new text
def predict_category(text):
    # Transform the input text using the trained vectorizer
    features = vectorizer.transform([text])

    # Predict the category using the trained model
    category = model.predict(features)[0]
    return category



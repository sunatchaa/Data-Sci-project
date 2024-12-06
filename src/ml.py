import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load the data
training_data_path = 'processed_subjectAreas.csv'
scopus_data_path = '/Users/pimmadaaphiwetsa/Downloads/scopus_data.csv'

training_data = pd.read_csv(training_data_path)
scopus_data = pd.read_csv(scopus_data_path)
training_data = training_data.dropna(subset=['Author Keywords'])

# Inspect data columns
print("Training data columns:", training_data.columns)
print("Scopus data columns:", scopus_data.columns)

# Preprocess data
# Assuming "Author Keywords" is the column with text and "Subject Areas" is the target in training data
training_data['combined_text'] = training_data['Cleaned and Split Publication Name'] + training_data['Processed Words'] + training_data['Author Keywords']

X_train_texts = training_data['combined_text']
y_train = training_data['Subject Areas']

# Check for missing values
assert X_train_texts.isnull().sum() == 0, "Training texts contain null values!"
assert y_train.isnull().sum() == 0, "Target column contains null values!"

# Vectorize text data using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train = vectorizer.fit_transform(X_train_texts)

# Train/test split for evaluation
X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_split, y_train_split)

# Evaluate model
y_pred_split = clf.predict(X_test_split)
print("Accuracy on test data:", accuracy_score(y_test_split, y_pred_split))
print("Classification report:\n", classification_report(y_test_split, y_pred_split))

# Process scopus_data for predictions
# Combine 'cleaned_title' and 'cleaned_publicationName' for prediction
scopus_data['combined_text'] = scopus_data['cleaned_title'] + ' ' + scopus_data['cleaned_publicationName']

# Vectorize combined text
X_scopus_texts = scopus_data['combined_text']
X_scopus = vectorizer.transform(X_scopus_texts)

# Predict subject areas for scopus_data
scopus_predictions = clf.predict(X_scopus)

# Save predictions
scopus_data['predicted subject areas'] = scopus_predictions
output_path = '/Users/pimmadaaphiwetsa/Downloads/predicts.csv'
scopus_data.to_csv(output_path, index=False)

print(f"Predictions saved to {output_path}")

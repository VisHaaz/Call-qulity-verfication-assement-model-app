from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import dill as pickle

# Load the CSV file with transcriptions
file_path = r'F:\machine learning\qulity model\test model\model 3\transcribed_data.csv' #Update this with the actual path to your files
data = pd.read_csv(file_path)
print(data.shape)
print(data['Cleaned Transcription'].head(5))

# Vocabulary
vocab = Counter()
for sentence in data['Cleaned Transcription']:
    vocab.update(sentence.split())

print("vocabulary size:",len(vocab))

tokens = [key for key in vocab if vocab[key] > 15]

print("Number of tokens appearing more than 15 times:", len(tokens))
print("Most common tokens:", tokens[:10])

# Save tokens to a text file
tokens_file_path = r'F:\machine learning\qulity model\test model\model 3\test runs\tokens.txt' #Update this with the actual path to your files
with open(tokens_file_path, 'w') as file:
    for token in tokens:
        file.write(f"{token}\n")

# Divide data set
X = data['Cleaned Transcription']
y = data['Verifications']
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training set size:",X_train.shape)
print("Testing set size:",X_test.shape)
print(y_train)

# Extract features using a custom vectorizer
def vectorizer(data, tokens):
    vectorize_lst = []

    for sentence in data:
        sentence_vec = np.zeros(len(tokens))

        for i in range(len(tokens)):
            if tokens[i] in sentence.split():
                sentence_vec[i] = 1
        vectorize_lst.append(sentence_vec)
    
    vectorize_lst_np = np.asarray(vectorize_lst, dtype=np.float32)

    return vectorize_lst_np

vectorized_X_train = vectorizer(X_train, tokens)
vectorized_X_test = vectorizer(X_test, tokens)

print(vectorized_X_test)

# Define the plot_distribution function
def plot_distribution(y, title):
    value_counts = y.value_counts()
    unique_values = value_counts.index.tolist()
    counts = value_counts.values

    print(f"{title}:")
    print("Unique values:", unique_values)
    print("Counts:", counts)

    if len(unique_values) >= 2:
        plt.figure(figsize=(8, 6))
        plt.pie(counts, labels=unique_values, autopct='%1.1f%%')
        plt.title(title)
        plt.show()
    else:
        print(f"Not enough unique values to create a pie chart for {title}.")

#distribution of call trancript lenght
data['text_length'] = data['Cleaned Transcription'].apply(lambda x: len(x.split()))
print("text data;",data['text_length'].describe())
plt.figure(figsize=(10, 6))
plt.hist(data['text_length'], bins=30)
plt.title('Distribution of Call Transcript Lengths')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.show()

#Handle imbalanced data
print("Original data distribution:")
print(y_train.value_counts())
plot_distribution(y_train, "Original Data Distribution")

smote = SMOTE()
vectorized_X_train_smote, y_train_smote = smote.fit_resample(vectorized_X_train, y_train)

print("Data distribution after SMOTE:")
print(y_train_smote.value_counts())
plot_distribution(y_train_smote, "Data Distribution After SMOTE")

# Define a function to train, predict, and evaluate a model
def train_predict_evaluate(model, model_name, X_train, y_train, X_test, y_test):
    print(f"\n--- {model_name} ---")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    try:
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    except AttributeError:
        # If the model doesn't have predict_proba, use decision_function if available
        try:
            y_pred_proba = model.decision_function(X_test)
        except AttributeError:
            y_pred_proba = y_pred  # Fall back to binary predictions
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    try:
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        print(f"ROC-AUC Score: {roc_auc}")
    except ValueError:
        print("ROC-AUC Score could not be calculated.")
        roc_auc = None

    return model, y_pred, accuracy, roc_auc

# Initialize models
models = {
    "Logistic Regression": LogisticRegression(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC(probability=True),
    "Naive Bayes": GaussianNB()
}

# Train, predict, and evaluate each model
results = {}
accuracies = []
roc_auc_scores = []
for model_name, model in models.items():
    trained_model, y_pred, accuracy, roc_auc = train_predict_evaluate(model, model_name, vectorized_X_train_smote, y_train_smote, vectorized_X_test, y_test)
    results[model_name] = {
        'model': trained_model,
        'predictions': y_pred,
        'accuracy': accuracy,
        'roc_auc': roc_auc
    }
    accuracies.append(accuracy)
    roc_auc_scores.append(roc_auc if roc_auc is not None else 0)

# Create a DataFrame to include Call ID, Actual values, and Predicted values for each model
results_df = pd.DataFrame({
    'Call ID': data.loc[y_test.index, 'Call ID'],
    'Actual': y_test.values
})

for model_name, result in results.items():
    results_df[f'Predicted_{model_name}'] = result['predictions']

# Print the results DataFrame
print("\nPrediction Results:")
print(results_df)

# Save results to CSV
results_df.to_csv(r'F:\machine learning\qulity model\test model\model 3\test runs\multi_model_results.csv', index=False) #Update this with the actual path to your files

# Save only the Logistic Regression model
logistic_model = results['Logistic Regression']['model']
model_file_path = r'F:\machine learning\qulity model\test model\model 3\test runs\logistic_regression_model.pkl' #Update this with the actual path to your files
with open(model_file_path, 'wb') as model_file:
    pickle.dump(logistic_model, model_file)
print("\nLogistic Regression model has been saved.")

# Save the vectorizer to a file
vectorizer_file_path = r'F:\machine learning\qulity model\test model\model 3\test runs\tfidf_vectorizer.pkl' #Update this with the actual path to your files
with open(vectorizer_file_path, 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)
print("\nvectorizer has been saved.")

# Create bar plots for accuracy and ROC-AUC scores
def create_bar_plot(scores, title, ylabel):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(models.keys(), scores)
    plt.title(title)
    plt.xlabel('Models')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

create_bar_plot(accuracies, 'Model Accuracies', 'Accuracy')
create_bar_plot(roc_auc_scores, 'Model ROC-AUC Scores', 'ROC-AUC Score')

print("\nAll models have been trained and evaluated. Graphs have been created for accuracies and ROC-AUC scores.")
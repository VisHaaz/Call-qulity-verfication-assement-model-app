import dill as pickle  # Using dill for serialization
import numpy as np

# File paths
model_file_path = r'F:\machine learning\qulity model\test model\model 3\software dev\callcheck_model.pkl'
vectorizer_file_path = r'F:\machine learning\qulity model\test model\model 3\software dev\token_vect.pkl'
tokens_file_path = r'F:\machine learning\qulity model\test model\model 3\software dev\tokens.pkl'

# Deserialize the model
with open(model_file_path, 'rb') as model_file:
    model = pickle.load(model_file)
    print("Model loaded successfully")

# Deserialize the vectorizer function
with open(vectorizer_file_path, 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)
    print("Vectorizer function loaded successfully")
    print("Vectorizer type:", type(vectorizer))

# Deserialize the tokens
with open(tokens_file_path, 'rb') as tokens_file:
    tokens = pickle.load(tokens_file)
    print("Tokens loaded successfully")

# Verify loaded data
print("Loaded tokens:", tokens[:10])  # Print first 10 tokens for verification

# Test the vectorizer function with a sample sentence
sample_sentence = ["This is a test transcription for verification"]
vectorized_sample = vectorizer(sample_sentence, tokens)
print("Vectorized sample:", vectorized_sample)

# Check the type of the vectorized sample
print("Type of vectorized sample:", type(vectorized_sample))
print("Shape of vectorized sample:", vectorized_sample.shape)

# Verify the model with a small test prediction
# Assuming vectorized_sample matches the expected input shape
if vectorized_sample.shape[1] == len(tokens):
    sample_prediction = model.predict(vectorized_sample)
    print("Sample prediction:", sample_prediction)
else:
    print("Mismatch in vectorized sample shape and tokens length")


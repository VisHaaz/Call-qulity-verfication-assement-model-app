import whisper
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import os
import time
import torch
import dill as pickle  # Use dill instead of pickle for serialization
import numpy as np
import nltk

# Check for GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model
whmodel = whisper.load_model("base", device=device)

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

# Function to transcribe audio files
def transcribe_audio(file_path):
    try:
        result = whmodel.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing file {file_path}: {e}")
        return ""

# Load logistic regression model, vectorizer, and tokens
def load_model_and_vectorizer_tokens(model_path, vectorizer_path, tokens_path):
    with open(model_path, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    with open(vectorizer_path, 'rb') as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)
    with open(tokens_path, 'rb') as tokens_file:
        loaded_tokens = pickle.load(tokens_file)
    
    print(f"Loaded model type: {type(loaded_model)}")
    print(f"Loaded vectorizer type: {type(loaded_vectorizer)}")
    print(f"Loaded tokens type: {type(loaded_tokens)}")
    
    return loaded_model, loaded_vectorizer, loaded_tokens


# Function to predict verification status
def predict_verification(text, model, vectorizer, tokens):
    text_vector = vectorizer([text], tokens)
    prediction = model.predict(text_vector)
    return prediction[0]

# Main function to check call quality (verification status)
def check_call_quality(audio_file):
    # Load the model, vectorizer, and tokens
    model_path = r"F:\machine learning\qulity model\test model\FInal tkineter app\Final app\callcheck_model.pkl"
    vectorizer_path = r"F:\machine learning\qulity model\test model\FInal tkineter app\Final app\token_vect.pkl"
    tokens_path = r"F:\machine learning\qulity model\test model\FInal tkineter app\Final app\tokens.pkl"
    
    # Load the model and vectorizer
    model, vectorizer, tokens = load_model_and_vectorizer_tokens(model_path, vectorizer_path, tokens_path)
    
    # Step 1: Transcribe the audio file
    transcription = transcribe_audio(audio_file)
    
    # Step 2: Predict verification status using the model
    verification_result = predict_verification(transcription, model, vectorizer, tokens)
    
    # Step 3: Return the result (3 for verified, 0 for not verified)
    if verification_result == 3:
        return "Verified"
    else:
        return "Not Verified"
    





import whisper
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import os
import time
import torch
import tkinter as tk
from tkinter import filedialog, messagebox
import dill as pickle  # Use dill instead of pickle for serialization
import numpy as np

# Check for GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model
whmodel = whisper.load_model("base", device=device)

# Ensure NLTK stopwords are downloaded
import nltk
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

# Function to process a list of audio files provided by the user
def process_audio_files(audio_files):
    rows = []
    
    for audio_file in audio_files:
        transcription = transcribe_audio(audio_file)
        cleaned_transcription = preprocess_text(transcription)
        rows.append({'Audio File': os.path.basename(audio_file), 'Cleaned Transcription': cleaned_transcription})
        time.sleep(2)  # Introduce a short break between each transcription to reduce CPU usage and heat
    
    data = pd.DataFrame(rows)
    return data

# Load logistic regression model and vectorizer & tokens
def load_model_and_vectorizer_tokens(model_path, vectorizer_path, tokens_path):
    with open(model_path, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    with open(vectorizer_path, 'rb') as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)
    with open(tokens_path, 'rb') as tokens_file:
        loaded_tokens = pickle.load(tokens_file)
    print("Tokens loaded successfully")
    # Debugging step: check the type of vectorizer
    print(f"Loaded vectorizer type: {type(loaded_vectorizer)}")
    print(f"Loaded model type: {type(loaded_model)}")
    return loaded_model, loaded_vectorizer, loaded_tokens

# Function to predict verification status
def predict_verification(text, model, vectorizer, tokens):
    text_vector = vectorizer([text], tokens)
    prediction = model.predict(text_vector)
    return prediction[0]

# GUI Application
class TranscriptionApp:
    def __init__(self, root, model, vectorizer, tokens):
        self.root = root
        self.root.title("Audio Transcription and Verification App")

        self.audio_files = []
        self.model = model
        self.vectorizer = vectorizer
        self.tokens = tokens

        self.file_label = tk.Label(root, text="No audio files selected.")
        self.file_label.pack()

        self.add_button = tk.Button(root, text="Add Audio Files", command=self.add_files)
        self.add_button.pack()

        self.output_button = tk.Button(root, text="Select Output File", command=self.select_output_file)
        self.output_button.pack()

        self.transcribe_button = tk.Button(root, text="Transcribe and Verify", command=self.transcribe_and_verify)
        self.transcribe_button.pack()

        self.output_file = None

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav *.mp3")])
        if files:
            self.audio_files.extend(files)
            self.file_label.config(text=f"{len(self.audio_files)} files selected.")

    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if self.output_file:
            messagebox.showinfo("Selected Output File", f"Output file: {self.output_file}")

    def transcribe_and_verify(self):
        if not self.audio_files:
            messagebox.showwarning("No Files", "Please add audio files to transcribe.")
            return

        if not self.output_file:
            messagebox.showwarning("No Output File", "Please select an output file.")
            return

        results = process_audio_files(self.audio_files)
        results['Verification'] = results['Cleaned Transcription'].apply(
            lambda x: predict_verification(x, self.model, self.vectorizer, self.tokens)
        )
        results.to_csv(self.output_file, index=False)
        messagebox.showinfo("Transcription and Verification Completed", f"Results saved to {self.output_file}")

def main():
    #Update this with the actual path to your files
    model_path = r"D:\MY\ltec\dissertation\Final files\23012089_Aloka_Vishvanath_Dissertation Proposal_COM 738\Final app\models and other saved files\callcheck_model.pkl"
    vectorizer_path = r"D:\MY\ltec\dissertation\Final files\23012089_Aloka_Vishvanath_Dissertation Proposal_COM 738\Final app\models and other saved files\token_vect.pkl"
    tokens_path = r"D:\MY\ltec\dissertation\Final files\23012089_Aloka_Vishvanath_Dissertation Proposal_COM 738\Final app\models and other saved files\tokens.pkl"
    
    model, vectorizer, tokens = load_model_and_vectorizer_tokens(model_path, vectorizer_path, tokens_path)
    
    root = tk.Tk()
    app = TranscriptionApp(root, model, vectorizer, tokens)
    root.mainloop()

if __name__ == "__main__":
    main()



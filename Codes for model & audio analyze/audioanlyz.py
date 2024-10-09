import whisper
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import os
import time
import torch

# Check for GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model
model = whisper.load_model("base", device=device)

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
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing file {file_path}: {e}")
        return ""

# Load the CSV file
file_path = r'F:\machine learning\qulity model\test model\manual call assement.csv'# Update this with the actual path to your files
data = pd.read_csv(file_path)

# Assuming the audio files are named with their Call ID and located in a directory named 'audio_files'
audio_dir = r'F:\machine learning\qulity model\test model\test calls wav'  # Update this with the actual path to your audio files
for index, row in data.iterrows():
    data.at[index, 'Transcription'] = transcribe_audio(os.path.join(audio_dir, f"{row['Call ID']}.wav"))
    time.sleep(2)  # Introduce a short break between each transcription to reduce CPU usage and heat

# Preprocess the transcriptions
data['Cleaned Transcription'] = data['Transcription'].apply(preprocess_text)

# Save the data with transcriptions to the specified location
output_file_path = r'F:\machine learning\qulity model\test model\model 3\transcribed_data.csv' #Update this with the actual path to your files
data.to_csv(output_file_path, index=False)

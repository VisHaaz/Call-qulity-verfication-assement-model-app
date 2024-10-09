import os
import random
from google.cloud import texttospeech
from pydub import AudioSegment

# Set environment variables for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"F:\machine learning\qulity model\service-account-file.json"
os.environ["PATH"] += os.pathsep + r"C:\ProgramData\chocolatey\bin"
# Explicitly set the path to ffmpeg and ffprobe
AudioSegment.converter = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ProgramData\chocolatey\bin\ffprobe.exe"

# Initialize Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

def synthesize_speech(text, output_filename, language_code, gender):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, specify the language code and the ssml voice gender
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=gender
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response to the output file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

# Define different conversation scenarios
conversation_scenarios =  {
    "router_password_change_with_verification": {
        "customer": [
            "Hi, I need help changing the password on my router.",
            "My name is John Doe and my driving license number is ABC123456.",
            "It's a Linksys router.",
            "Yes, I have the app installed.",
            "Okay, I've opened the app.",
            "Alright, I see the option to change the password.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, John. Can you tell me what type of router you have?",
            "Great, do you have the Linksys app installed on your phone?",
            "Perfect. Open the app and log in.",
            "Now, go to the settings menu and look for the 'Change Password' option.",
            "Enter your new password and save the changes.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "no_signal_issue_no_verification_no_greetings": {
        "customer": [
            "Hi, I'm not getting any signal on my TV.",
            "Yes, I've checked all the cables.",
            "Yes, the TV is set to the correct input.",
            "Alright, I'll try that.",
            "It worked! The signal is back.",
            "Thank you so much for your help.",
            "Goodbye."
        ],
        "agent": [
            "Have you checked all the cables to make sure they are securely connected?",
            "Is your TV set to the correct input?",
            "Let's try resetting the cable box. Unplug it from the power source, wait 10 seconds, and plug it back in.",
            "Great!",
            "Bye."
        ]
    },
    "no_signal_issue_with_verification_greetings": {
        "customer": [
            "Hi, I'm not getting any signal on my TV.",
            "My name is Jane Doe and my passport number is XYZ987654.",
            "Yes, I've checked all the cables.",
            "Yes, the TV is set to the correct input.",
            "Alright, I'll try that.",
            "It worked! The signal is back.",
            "Thank you so much for your help.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry to hear that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Jane. Have you checked all the cables to make sure they are securely connected?",
            "Is your TV set to the correct input?",
            "Let's try resetting the cable box. Unplug it from the power source, wait 10 seconds, and plug it back in.",
            "Great! I'm glad to hear the signal is back.",
            "You're welcome. Have a great day!",
            "Goodbye."
        ]
    },
    "non_technical_issue_transfer_customer_service": {
        "customer": [
            "Hi, I need help with my billing statement.",
            "Okay, thank you.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry, I can only assist with technical issues. Let me transfer you to our customer service hotline.",
            "Please hold while I transfer your call.",
            "Goodbye."
        ]
    },
    "internet_slowness_traffic_issue_apology": {
        "customer": [
            "Hi, my internet has been very slow lately.",
            "My name is Mike Smith and my driving license number is DEF654321.",
            "Is there anything I can do about it?",
            "Okay, thank you for letting me know.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry to hear that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Mike. Let me check our system for any issues in your area.",
            "It seems there is heavy usage traffic on the signal towers in your area. I apologize for the inconvenience.",
            "Unfortunately, this is a temporary issue. We are working to resolve it as soon as possible. In the meantime, you might experience some slow speeds during peak hours.",
            "You're welcome. If you have any other questions, feel free to contact us.",
            "Goodbye."
        ]
    },
    "tv_connection_poor_service": {
        "customer": [
            "Hi, my TV connection is not working.",
            "Yes, I have.",
            "Yes, I did.",
            "Can you provide more details or help me troubleshoot further?",
            "Alright, thanks.",
            "Goodbye."
        ],
        "agent": [
            "Have you checked your cables?",
            "Did you try resetting the cable box?",
            "Then I don't know what the issue is. You should call a technician.",
            "No, just call a technician.",
            "Bye."
        ]
    },
    "data_usage_details_no_verification": {
        "customer": [
            "Hi, can you give me my data usage details?",
            "Thank you.",
            "Goodbye."
        ],
        "agent": [
            "Sure, let me check that for you.",
            "You have used 150GB out of your 200GB monthly allowance.",
            "You're welcome. Have a great day!",
            "Goodbye."
        ]
    },
    "data_usage_details_with_verification": {
        "customer": [
            "Hi, can you give me my data usage details?",
            "My name is Anna Lee and my passport number is UVW456789.",
            "Thank you.",
            "Goodbye."
        ],
        "agent": [
            "Sure, can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Anna. Let me check that for you.",
            "You have used 120GB out of your 200GB monthly allowance.",
            "You're welcome. Have a great day!",
            "Goodbye."
        ]
    },
    "router_firmware_update_with_verification": {
        "customer": [
            "Hi, I need help updating the firmware on my router.",
            "My name is Sarah Johnson and my passport number is ABC987654.",
            "It's a Netgear router.",
            "Yes, I have the app installed.",
            "Okay, I've opened the app.",
            "Alright, I see the option to update the firmware.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Sarah. Can you tell me what type of router you have?",
            "Great, do you have the Netgear app installed on your phone?",
            "Perfect. Open the app and log in.",
            "Now, go to the settings menu and look for the 'Update Firmware' option.",
            "Follow the instructions to update the firmware and wait for it to complete.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "router_firmware_update_without_verification": {
        "customer": [
            "Hi, I need help updating the firmware on my router.",
            "It's a Netgear router.",
            "Yes, I have the app installed.",
            "Okay, I've opened the app.",
            "Alright, I see the option to update the firmware.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. What type of router do you have?",
            "Great, do you have the Netgear app installed on your phone?",
            "Perfect. Open the app and log in.",
            "Now, go to the settings menu and look for the 'Update Firmware' option.",
            "Follow the instructions to update the firmware and wait for it to complete.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "internet_connection_issue_verification_no_verification": {
        "customer": [
            "Hi, my internet connection is not working.",
            "My name is Paul Green and my driving license number is GHI321654.",
            "Yes, I've checked all the cables.",
            "Yes, the router is on.",
            "Okay, I'll try restarting the router.",
            "It worked! The connection is back.",
            "Thank you so much for your help.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry to hear that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Paul. Have you checked all the cables to make sure they are securely connected?",
            "Is the router turned on?",
            "Let's try restarting the router. Unplug it from the power source, wait 10 seconds, and plug it back in.",
            "Great! I'm glad to hear the connection is back.",
            "You're welcome. Have a great day!",
            "Goodbye."
        ]
    },
    "internet_connection_issue_no_verification": {
        "customer": [
            "Hi, my internet connection is not working.",
            "Yes, I've checked all the cables.",
            "Yes, the router is on.",
            "Okay, I'll try restarting the router.",
            "It worked! The connection is back.",
            "Thank you so much for your help.",
            "Goodbye."
        ],
        "agent": [
            "Have you checked all the cables to make sure they are securely connected?",
            "Is the router turned on?",
            "Let's try restarting the router. Unplug it from the power source, wait 10 seconds, and plug it back in.",
            "Great! I'm glad to hear the connection is back.",
            "Bye."
        ]
    }
}

# Define a list of voice configurations
voices = [
    {"language_code": "en-US", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-US", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-GB", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-GB", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-AU", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-AU", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-IN", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-IN", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-CA", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-CA", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-NZ", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-NZ", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-IE", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-IE", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-ZA", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
    {"language_code": "en-ZA", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
]

# Create a folder to store the audio files
audio_folder = r"F:\machine learning\qulity model\Audiosample3"
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

# Generate 100 sample calls
for call_index in range(100):
    # Randomly select a conversation scenario
    scenario_key = random.choice(list(conversation_scenarios.keys()))
    scenario = conversation_scenarios[scenario_key]

    # Randomly select voices for customer and agent
    customer_voice = random.choice(voices)
    agent_voice = random.choice(voices)

    # Generate customer audio files
    for i, text in enumerate(scenario["customer"]):
        output_filename = os.path.join(audio_folder, f"call_{call_index}_customer_{i}.mp3")
        synthesize_speech(text, output_filename, customer_voice["language_code"], customer_voice["ssml_gender"])

    # Generate agent audio files
    for i, text in enumerate(scenario["agent"]):
        output_filename = os.path.join(audio_folder, f"call_{call_index}_agent_{i}.mp3")
        synthesize_speech(text, output_filename, agent_voice["language_code"], agent_voice["ssml_gender"])

    # Combine the audio files
    combined_audio = AudioSegment.empty()

    # Load and combine the audio segments
    for i in range(len(scenario["customer"])):
        customer_audio = AudioSegment.from_mp3(os.path.join(audio_folder, f"call_{call_index}_customer_{i}.mp3"))
        combined_audio += customer_audio
        if i < len(scenario["agent"]):
            agent_audio = AudioSegment.from_mp3(os.path.join(audio_folder, f"call_{call_index}_agent_{i}.mp3"))
            combined_audio += agent_audio

    # Specify the custom file location for the combined file
    combined_file_location = os.path.join(audio_folder, f"combined_call_{call_index}.mp3")

    # Export the combined audio to the specified file location
    combined_audio.export(combined_file_location, format="wav")

print("Generated 100 sample calls.")
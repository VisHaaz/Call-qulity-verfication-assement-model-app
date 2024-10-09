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
conversation_scenarios = {
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
            "Sure, I can help with that. Can you tell me what type of router you have?",
            "Great, do you have the Netgear app installed on your phone?",
            "Perfect. Open the app and log in.",
            "Now, go to the settings menu and look for the 'Update Firmware' option.",
            "Follow the instructions to update the firmware and wait for it to complete.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "no_internet_connection_no_verification_no_greetings": {
        "customer": [
            "Hi, I have no internet connection at all.",
            "Yes, I did.",
            "No, it's off.",
            "I've checked them, they seem fine.",
            "Alright, I'll try that.",
            "It's working now, the internet is back.",
            "Thank you for your help.",
            "Goodbye."
        ],
        "agent": [
            "Have you tried restarting your router?",
            "Is the internet light on your router blinking?",
            "Let's check the cables to ensure they are securely connected.",
            "Can you unplug the router from the power source, wait 10 seconds, and plug it back in?",
            "Great.",
            "Bye."
        ]
    },
    "no_internet_connection_with_verification_greetings": {
        "customer": [
            "Hi, I have no internet connection at all.",
            "My name is Emily Davis and my driving license number is XYZ123456.",
            "Yes, I did.",
            "No, it's off.",
            "I've checked them, they seem fine.",
            "Alright, I'll try that.",
            "It's working now, the internet is back.",
            "Thank you for your help.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry to hear that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Emily. Have you tried restarting your router?",
            "Is the internet light on your router blinking?",
            "Let's check the cables to ensure they are securely connected.",
            "Can you unplug the router from the power source, wait 10 seconds, and plug it back in?",
            "Great! I'm glad to hear the internet is back.",
            "You're welcome. Have a great day!",
            "Goodbye."
        ]
    },
    "billing_issue_transfer_customer_service": {
        "customer": [
            "Hi, I have a question about a charge on my bill.",
            "Okay, thank you.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry, I can only assist with technical issues. Let me transfer you to our customer service hotline.",
            "Please hold while I transfer your call.",
            "Goodbye."
        ]
    },
    "internet_slowness_due_to_maintenance_apology": {
        "customer": [
            "Hi, my internet has been very slow lately.",
            "My name is Tom Harris and my passport number is ABC654321.",
            "How long will this maintenance take?",
            "Okay, thank you for letting me know.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry to hear that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Tom. Let me check our system for any issues in your area.",
            "It seems there is scheduled maintenance in your area. I apologize for the inconvenience.",
            "It should be completed within the next few hours. You might experience slow speeds until then.",
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
    "data_usage_details_without_verification": {
        "customer": [
            "Hi, can you give me my data usage details?",
            "Thank you.",
            "Goodbye."
        ],
        "agent": [
            "Sure, let me check that for you.",
            "You have used 75GB out of your 100GB monthly allowance.",
            "You're welcome. Have a great day!",
            "Goodbye."
        ]
    },
    "data_usage_details_with_verification": {
        "customer": [
            "Hi, can you give me my data usage details?",
            "My name is Lisa Brown and my driving license number is DEF789012.",
            "Thank you.",
            "Goodbye."
        ],
        "agent": [
            "Sure, can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Lisa. Let me check that for you.",
            "You have used 200GB out of your 300GB monthly allowance.",
            "You're welcome. Have a great day!",
            "Goodbye."
        ]
    },
    "slow_internet_due_to_device_interference": {
        "customer": [
            "Hi, my internet speed is very slow.",
            "My name is Mark Wilson and my passport number is GHI321654.",
            "Is there anything I can do about it?",
            "Okay, I'll try that. Thank you for your help.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry to hear that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Mark. Let me check our system for any issues in your area.",
            "It seems there is interference from other devices in your area causing the slow speed. I apologize for the inconvenience.",
            "You can try moving your router to a different location or reduce the number of connected devices.",
            "You're welcome. If you have any other questions, feel free to contact us.",
            "Goodbye."
        ]
    },
    "router_port_forwarding_setup_with_verification": {
        "customer": [
            "Hi, I need help setting up port forwarding on my router.",
            "My name is Robert Green and my passport number is XYZ654123.",
            "It's a TP-Link router.",
            "Yes, I can access the router settings page.",
            "Okay, I've logged in.",
            "I see the port forwarding option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Robert. Can you tell me what type of router you have?",
            "Great, do you have access to the router settings page?",
            "Please log in and go to the settings menu.",
            "Now, look for the 'Port Forwarding' option and click on it.",
            "Enter the required details and save the settings.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "router_port_forwarding_setup_without_verification": {
        "customer": [
            "Hi, I need help setting up port forwarding on my router.",
            "It's a TP-Link router.",
            "Yes, I can access the router settings page.",
            "Okay, I've logged in.",
            "I see the port forwarding option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you tell me what type of router you have?",
            "Great, do you have access to the router settings page?",
            "Please log in and go to the settings menu.",
            "Now, look for the 'Port Forwarding' option and click on it.",
            "Enter the required details and save the settings.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "satellite_tv_signal_weak_no_verification": {
        "customer": [
            "Hi, my satellite TV signal is very weak.",
            "Yes, I have checked the dish alignment.",
            "No, the weather is clear.",
            "Okay, I'll try resetting the receiver.",
            "It seems to be better now.",
            "Thank you for your help.",
            "Goodbye."
        ],
        "agent": [
            "Have you checked the dish alignment?",
            "Is there any bad weather that could be affecting the signal?",
            "Let's try resetting the receiver. Unplug it from the power source, wait 10 seconds, and plug it back in.",
            "Great! I'm glad to hear it's better.",
            "You're welcome.",
            "Goodbye."
        ]
    },
    "satellite_tv_signal_weak_with_verification": {
        "customer": [
            "Hi, my satellite TV signal is very weak.",
            "My name is Jessica White and my driving license number is LMN123456.",
            "Yes, I have checked the dish alignment.",
            "No, the weather is clear.",
            "Okay, I'll try resetting the receiver.",
            "It seems to be better now.",
            "Thank you for your help.",
            "Goodbye."
        ],
        "agent": [
            "I'm sorry to hear that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Jessica. Have you checked the dish alignment?",
            "Is there any bad weather that could be affecting the signal?",
            "Let's try resetting the receiver. Unplug it from the power source, wait 10 seconds, and plug it back in.",
            "Great! I'm glad to hear it's better.",
            "You're welcome.",
            "Goodbye."
        ]
    },
    "router_factory_reset_without_verification": {
        "customer": [
            "Hi, I need help resetting my router to factory settings.",
            "It's a D-Link router.",
            "Yes, I can access the router settings page.",
            "Okay, I've logged in.",
            "I see the factory reset option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you tell me what type of router you have?",
            "Great, do you have access to the router settings page?",
            "Please log in and go to the settings menu.",
            "Now, look for the 'Factory Reset' option and click on it.",
            "Confirm the reset and wait for the router to reboot.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "router_factory_reset_with_verification": {
        "customer": [
            "Hi, I need help resetting my router to factory settings.",
            "My name is Andrew Brown and my driving license number is GHI987654.",
            "It's a D-Link router.",
            "Yes, I can access the router settings page.",
            "Okay, I've logged in.",
            "I see the factory reset option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Andrew. Can you tell me what type of router you have?",
            "Great, do you have access to the router settings page?",
            "Please log in and go to the settings menu.",
            "Now, look for the 'Factory Reset' option and click on it.",
            "Confirm the reset and wait for the router to reboot.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "satellite_tv_box_software_update_without_verification": {
        "customer": [
            "Hi, I need help updating the software on my satellite TV box.",
            "It's a DirectTV box.",
            "Yes, I have the remote.",
            "Okay, I've accessed the settings menu.",
            "I see the software update option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you tell me what type of satellite TV box you have?",
            "Great, do you have the remote with you?",
            "Please use the remote to access the settings menu.",
            "Now, look for the 'Software Update' option and select it.",
            "Follow the instructions to update the software and wait for it to complete.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "satellite_tv_box_software_update_with_verification": {
        "customer": [
            "Hi, I need help updating the software on my satellite TV box.",
            "My name is Oliver Smith and my passport number is JKL123987.",
            "It's a DirectTV box.",
            "Yes, I have the remote.",
            "Okay, I've accessed the settings menu.",
            "I see the software update option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Oliver. Can you tell me what type of satellite TV box you have?",
            "Great, do you have the remote with you?",
            "Please use the remote to access the settings menu.",
            "Now, look for the 'Software Update' option and select it.",
            "Follow the instructions to update the software and wait for it to complete.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "router_dns_settings_change_without_verification": {
        "customer": [
            "Hi, I need help changing the DNS settings on my router.",
            "It's a Belkin router.",
            "Yes, I can access the router settings page.",
            "Okay, I've logged in.",
            "I see the DNS settings option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you tell me what type of router you have?",
            "Great, do you have access to the router settings page?",
            "Please log in and go to the settings menu.",
            "Now, look for the 'DNS Settings' option and click on it.",
            "Enter the new DNS server addresses and save the settings.",
            "You're welcome! Have a nice day.",
            "Goodbye."
        ]
    },
    "router_dns_settings_change_with_verification": {
        "customer": [
            "Hi, I need help changing the DNS settings on my router.",
            "My name is Laura Thompson and my driving license number is QRS987321.",
            "It's a Belkin router.",
            "Yes, I can access the router settings page.",
            "Okay, I've logged in.",
            "I see the DNS settings option.",
            "Thank you for your help!",
            "Goodbye."
        ],
        "agent": [
            "Sure, I can help with that. Can you please verify your identity first? May I have your name and your driving license or passport number?",
            "Thank you, Laura. Can you tell me what type of router you have?",
            "Great, do you have access to the router settings page?",
            "Please log in and go to the settings menu.",
            "Now, look for the 'DNS Settings' option and click on it.",
            "Enter the new DNS server addresses and save the settings.",
            "You're welcome! Have a nice day.",
            "Goodbye."
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
audio_folder = r"F:\machine learning\qulity model\audio"
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
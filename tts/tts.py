import os
from azure.cognitiveservices.speech import SpeechSynthesizer, SpeechConfig, AudioConfig

with open('transcript.txt', 'r') as file:
    transcript = file.read()

text = transcript

speech_config = SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
speech_config.speech_synthesis_voice_name='en-US-BrianNeural'
audio_config = AudioConfig(filename="swapprPresentationTranscriptBrian.wav")
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
synthesizer.speak_text_async(text).get()

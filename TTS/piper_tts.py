from piper import PiperVoice, SynthesisConfig
import wave 
from pathlib import Path

MODEL_PATH = str(Path(__file__).parent / 'de_DE-thorsten-medium.onnx')
OUTPUT = str(Path(__file__).parent.parent / 'AudioFiles' / 'output.wav')

syn_config = SynthesisConfig(
    volume=0.5,  # half as loud
    length_scale=1.1,  # twice as slow
    noise_scale=1.0,  # more audio variation
    noise_w_scale=1.0,  # more speaking variation
    normalize_audio=False, # use raw audio from voice
)

def TTS(input:str):
    voice = PiperVoice.load(MODEL_PATH)
    with wave.open(OUTPUT, "wb") as wav_file:
        voice.synthesize_wav(input,syn_config=syn_config, wav_file=wav_file)






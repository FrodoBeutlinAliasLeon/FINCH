import pvporcupine
import pyaudio
import numpy as np
import webrtcvad
import wave
import os
import time
from dotenv import load_dotenv
from Classification.classifier import predict
from STT.voxtral import transcribe
from TapoTools.lamps import (light_off, light_on, light_strip_on, light_strip_off, react)
from AIAgent.agents import read_user
from TTS.piper_tts import TTS
import threading
from pathlib import Path
import subprocess

load_dotenv()


WAKEWORD_MODEL_PATH = Path(__file__).parent /'PPN' /'JARVIS-RASPBERRYPI.ppn'
MODEL_PATH = Path(__file__).parent /'PPN' /'porcupine_params_de.pv'
INPUT_DEVICE_INDEX = 5
OUTPUT_DEVICE_INDEX = 2
ACCESS_KEY = os.getenv("PORCUPINE")
OUT_FILE = str(Path(__file__).parent /'AudioFiles' / 'output.wav')


def on_wake_word(pa, path_to_model: str, input_device_index: int) -> bool:
    porcupine = pvporcupine.create(
         access_key= ACCESS_KEY,
         keyword_paths=[path_to_model],
         model_path=str(MODEL_PATH))
    
    audio_stream = pa.open(
        rate = porcupine.sample_rate,
        channels = 1,
        format = pyaudio.paInt16,
        input=True,
        frames_per_buffer= porcupine.frame_length,
        input_device_index= input_device_index,
        
    )
    
    while True:
        audio_frame = audio_stream.read(porcupine.frame_length, exception_on_overflow=False) # 1 frame sind 2 byte 
        pcm_data = np.frombuffer(audio_frame, dtype=np.int16)
        keyword_index = porcupine.process(pcm_data)
        if keyword_index >= 0:
            print("Wake Word erkannt")
            porcupine.delete()
            audio_stream.close()
            return True
        
RATE = 16000 # HZ is recommended for STT 
FRAME_DURATION_MS = 20 # either 10 20 or 30
FRAME_SIZE = int(RATE * FRAME_DURATION_MS / 1000) 
FORMAT = pyaudio.paInt16 # how many samples are safed
MAX_RECORD_MS = 10000 # Hard limit
MAX_WAIT_FOR_FIRST_SPEECH = 2000
MAX_SILENCE_AFTER_SPEECH = 1000
def record_text(pa, input_device_index: int):
    vad = webrtcvad.Vad()
    vad.set_mode(3)
    threading.Thread(target=react, args=(), daemon=True).start()
    stream = pa.open(
        rate= RATE,
        input=True,
        input_device_index= input_device_index,
        format= FORMAT,
        channels= 1,
        frames_per_buffer= FRAME_SIZE
    )
    print("recording...")
    
    frames = []
    heard_voice = False
    silence_ms = 0
    waited_ms = 0
    max_frames = int(MAX_RECORD_MS / FRAME_DURATION_MS)
    for _ in range(max_frames):
        frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
        is_speech =vad.is_speech(
                    frame,
                    RATE
                )
        if is_speech:
            if not heard_voice:
                heard_voice = True
                waited_ms = 0
            silence_ms = 0
            frames.append(frame)
        else: 
            if not heard_voice:
                waited_ms += FRAME_DURATION_MS
                if waited_ms >= MAX_WAIT_FOR_FIRST_SPEECH:
                    print("Keine Sprache erkannt")
                    break
            else:
                silence_ms += FRAME_DURATION_MS
                if silence_ms >= MAX_SILENCE_AFTER_SPEECH:
                    print("stille erkannt -> aufnahme beenden")
                    break
                frames.append(frame)
                
        
    print("done recording")
    stream.stop_stream()
    stream.close()
    SPOKEN = Path(__file__).parent /'AudioFiles' /'output.wav'
    frames_to_wave(frames=frames, sample_rate= RATE, out_path=SPOKEN)
    spoken_text = transcribe(SPOKEN)
    label, pred = predict(spoken_text)
    if pred > 0.75:
        print(f"Label chosen:{label}, with confidence: {pred}")
        print(spoken_text)
        if label == "light_on":
            light_on()
        elif label == "light_off":
            light_off()
        elif label == "bed_light_on":
            light_strip_on()
        elif label == "bed_light_off":
            light_strip_off()
        # elif label == "mirror_light_on":
        #     pass
        # elif label =="set_alarm":
        #     pass           
    else:
        print(spoken_text)
        print(f"Classifier not Activated: Label {label}, with confidence: {pred} ")
        print("LLM ACTIVATED")
        answer = read_user(spoken_text)
        TTS(answer)
        subprocess.run(["aplay", "-D", f"plughw:{OUTPUT_DEVICE_INDEX},0", f"{OUT_FILE}"])
        
    
    
def frames_to_wave(frames, sample_rate, out_path):
    raw_audio = b"".join(frames)
    with out_path.open("wb") as f: #pathlib does not return a string!
        with wave.open(f, "wb") as wf:
            wf.setnchannels(1)        
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)        
            wf.writeframes(raw_audio)

    
def main():
    print("Starte main()...")
    global_pa = pyaudio.PyAudio()
    try:
        while True:
            if on_wake_word(global_pa, WAKEWORD_MODEL_PATH, INPUT_DEVICE_INDEX):
                time.sleep(0.2)
                record_text(global_pa, INPUT_DEVICE_INDEX)
    except KeyboardInterrupt:
        print("Beende Programm")
    finally:
        global_pa.terminate()


if __name__ == "__main__":
    main()
    

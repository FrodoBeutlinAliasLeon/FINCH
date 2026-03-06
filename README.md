<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1A1A1A,20:3D2B1F,40:C8652A,60:E8913A,80:D4A030,100:F5EDE0&height=150&section=header&text=FINCH&desc=Fast%20IoT%20Network%20Control%20Hub&descSize=15&descAlign=50&fontSize=70&descAlignY=55&fontAlignY=30&animation=fadeIn" align="center" />
</p>

## Hey everyone!  
This is my attempt on creating a perfectly individual smart home system.  
This project is designed to run on a Raspberrypi - therefore im not hosting the models myself.  
For privacy reasons i decided to mainly use the european AI-company "Mistral".  

### The workflow:
1. Once the wakeword is said, the programm will start to record and live transcribe the voice to text - this mainly safes latency.
2. The transcribed text will then go trough a intend classifier which labes the intend.
   - Current labels are: light_on, light_off, mirror_light_on, mirror_light_off, set_alarm and llm
3. If the intend is "llm", the inquery will be send to the Agent, which then can decide weather to make one or more tool calls, to just answer, or do both.
4. The last and final step is to transcribe response text from the agent back to speecht by using a STT model.
<p align="center">
<img src="/assets/FINCH-workflow.png"/></p>

## Project Structure

```
FINCH/
├── backbone.py              # Main loop: wake word → record → classify → act
├── actions.py               # Flask REST API (light control, disco, temp endpoint)
├── AIAgent/
│   ├── agents.py            # LangChain agent with Mistral LLM
│   └── agent_tools.py       # Tool definitions for the agent
├── Classification/
│   ├── classifier.py        # TF-IDF + SVM intent classifier
│   └── intent_model.pkl     # Trained classifier model
├── STT/
│   └── voxtral.py           # Speech-to-text via Mistral Voxtral
├── TTS/
│   └── piper_tts.py         # Text-to-speech output
├── TapoTools/
│   └── lamps.py             # Tapo smart light/strip control
├── State/
│   ├── world_state.py       # Pydantic world state (JSON persistence)
│   └── state.json           # Runtime state file (needs to be added manually)
├── PPN/
│   ├── JARVIS-RASPBERRYPI.ppn  # Wake word model
│   └── porcupine_params_de.pv  # German language model
├── SSL/
│   ├── cert.pem             # HTTPS certificate (needs to be added manually)
│   └── key.pem              # HTTPS private key (needs to be added manually)
└── AudioFiles/
    └── output.wav           # Temporary recording buffer
```
<p align="right">
<img src ="/assets/fink.png" width=150></p>

import time
import asyncio
import os
import scipy.io.wavfile
import numpy as np

# Package Imports
import pyttsx3
from gtts import gTTS
import edge_tts

# Optional high-quality models (Try-Except block to prevent crashes if not installed)
try:
    from kokoro import KPipeline
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False

async def test_pyttsx3(text):
    start = time.perf_counter()
    engine = pyttsx3.init()
    filename = "pyttsx3.wav"
    engine.save_to_file(text, filename)
    engine.runAndWait()
    duration = time.perf_counter() - start
    return "pyttsx3", duration, filename

async def test_gtts(text):
    start = time.perf_counter()
    tts = gTTS(text)
    filename = "gtts.mp3"
    tts.save(filename)
    duration = time.perf_counter() - start
    return "gTTS", duration, filename

async def test_edgetts(text):
    start = time.perf_counter()
    filename = "edge_tts.mp3"
    # Using a high-quality neural voice
    communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
    await communicate.save(filename)
    duration = time.perf_counter() - start
    return "Edge-TTS", duration, filename

async def test_kokoro(text):
    if not MODELS_AVAILABLE:
        return None, 0, "Error: Kokoro not installed"
    
    start = time.perf_counter()
    filename = "kokoro.wav"
    
    # FIX 1: Pass repo_id to suppress the warning
    pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M') 
    
    # FIX 2: Collect all audio chunks into a list
    all_audio = []
    generator = pipeline(text, voice='af_bella', speed=1)
    
    for i, (gs, ps, audio) in enumerate(generator):
        if audio is not None:
            # FIX 3: Explicitly convert torch tensor to numpy to avoid .kind error
            if hasattr(audio, 'numpy'):
                all_audio.append(audio.numpy())
            else:
                all_audio.append(audio)

    # Combine all chunks into one single audio array
    if all_audio:
        final_audio = np.concatenate(all_audio)
        scipy.io.wavfile.write(filename, 24000, final_audio)
    
    duration = time.perf_counter() - start
    return "Kokoro", duration, filename

async def main():
    print("--- Python TTS Benchmarker ---")
    
    # 1. Get Text Input
    user_text = input("\nEnter the text you want to convert: ").strip()
    if not user_text:
        print("Empty input. Exiting.")
        return

    while True:
        print("\nSelect a package to test:")
        print("1. pyttsx3 (Offline)")
        print("2. gTTS (Google Cloud)")
        print("3. edge-tts (Microsoft Neural)")
        if MODELS_AVAILABLE:
            print("4. Kokoro (Local Neural)")
        print("0. Exit")
        
        choice = input("\nChoice: ")

        result = None

        if choice == '1':
            result = await test_pyttsx3(user_text)
        elif choice == '2':
            result = await test_gtts(user_text)
        elif choice == '3':
            result = await test_edgetts(user_text)
        elif choice == '4' and MODELS_AVAILABLE:
            result = await test_kokoro(user_text)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            continue

        if result and result[0]:
            name, dur, path = result
            print("-" * 40)
            print(f"Model Used:   {name}")
            print(f"Time Taken:   {dur:.4f} seconds")
            print(f"File Saved:   {path}")
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
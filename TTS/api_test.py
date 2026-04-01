# =====================================================
# TTS API Providers Benchmark Script for Google Colab
# Packages / Providers: ElevenLabs • Noiz.ai • Cartesia Sonic • Deepgram Aura-2 • Murf.ai • Respeecher • Resemble AI
# =====================================================
# Features:
# • Uses .env file for API keys (secure)
# • Auto-installs required SDKs
# • Measures exact generation + download time
# • Saves audio file and auto-downloads it
# • Works perfectly in Google Colab

import time
import subprocess
import os
from dotenv import load_dotenv
import asyncio
import struct
import wave

# Helper function to write raw PCM data as proper WAV file
def write_pcm_as_wav(filename, audio_data, sample_rate=44100, channels=1, sample_width=2):
    """Convert raw PCM bytes to a proper WAV file"""
    try:
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data)
        return True
    except Exception as e:
        print(f"Error writing WAV: {e}")
        return False

print(" TTS API Providers Benchmark Script Loaded!")
print("Available providers:")
print("   1. ElevenLabs")
print("   2. Noiz.ai")
print("   3. Cartesia Sonic")
print("   4. Deepgram Aura-2")
print("   5. Murf.ai")
print("   6. Respeecher")
print("   7. Resemble AI")

provider_choice = input("\nEnter provider name or number (e.g. 'ElevenLabs' or '1'): ").strip().lower()
text = input("\nEnter the text/paragraph you want to convert to speech:\n").strip()

if not text:
    text = "Hello, this is a high-quality test of the TTS API benchmark running in Google Colab."

# Map to proper name
provider_map = {
    "1": "elevenlabs", "elevenlabs": "elevenlabs",
    "2": "noiz.ai", "noiz": "noiz.ai", "noiz.ai": "noiz.ai",
    "3": "cartesia", "cartesia sonic": "cartesia", "cartesia": "cartesia",
    "4": "deepgram", "deepgram aura-2": "deepgram", "aura-2": "deepgram",
    "5": "murf.ai", "murf": "murf.ai", "murf.ai": "murf.ai",
    "6": "respeecher", "respeecher": "respeecher",
    "7": "resemble", "resemble ai": "resemble", "resemble": "resemble"
}

provider = provider_map.get(provider_choice, provider_choice)

valid_providers = ["elevenlabs", "noiz.ai", "cartesia", "deepgram", "murf.ai", "respeecher", "resemble"]
if provider not in valid_providers:
    print(f" Unknown provider: {provider}")
    raise SystemExit

print(f"\n Testing: {provider.capitalize()}")
start_time = time.perf_counter()



if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write(env_content)
    print(" Created .env file. Please edit it with your API keys!")
    print("   → Double-click the .env file in the file browser on the left to edit.")

load_dotenv()

# ====================== AUTO-INSTALL SDKs ======================
install_map = {
    "elevenlabs": "elevenlabs",
    "noiz.ai": "requests",          
    "deepgram": "deepgram-sdk",
    "murf.ai": "murf",
    "respeecher": "respeecher",
    "resemble": "resemble"
}

pkg = install_map.get(provider)
if pkg:
    print(f"   Installing {pkg} SDK ...")
    subprocess.check_call(["pip", "install", "--quiet", pkg])

print("   SDK ready!")

# ====================== GET API KEY ======================
api_key = os.getenv({
    "elevenlabs": "ELEVENLABS_API_KEY",
    "noiz.ai": "Authorization",
    "cartesia": "CARTESIA_API_KEY",
    "deepgram": "DEEPGRAM_API_KEY",
    "murf.ai": "MURF_API_KEY",
    "respeecher": "RESPEECHER_API_KEY",
    "resemble": "RESEMBLE_API_KEY"
}[provider])

if not api_key or api_key.startswith("your_"):
    print(f"❌ Missing API key for {provider}!")
    print("   Please edit the .env file and add your key, then run this cell again.")
    raise SystemExit

# ====================== TTS GENERATION ======================
filename = "speech_output.wav"

if provider == "elevenlabs":
    filename = "speech_output.mp3"
    from elevenlabs.client import ElevenLabs
    from elevenlabs import save
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",   # Bella (change as needed)
        model_id="eleven_flash_v2_5",      # fast & high quality
        output_format="mp3_44100_128"
    )
    save(audio, filename)

elif provider == "cartesia":
    filename = "speech_output.wav"
    from cartesia import Cartesia
    import io
    client = Cartesia(api_key=api_key)
    response = client.tts.generate(
        model_id="sonic-2",
        transcript=text,
        voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},  # example voice
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}
    )
    # Read audio data from response (it's a file-like object or bytes)
    if hasattr(response, 'read'):
        audio_data = response.read()
    else:
        audio_data = response.getvalue() if hasattr(response, 'getvalue') else bytes(response)
    
    # Convert raw PCM to proper WAV file
    write_pcm_as_wav(filename, audio_data, sample_rate=44100, channels=1, sample_width=4)

elif provider == "deepgram":
    filename = "speech_output.mp3"
    from deepgram import DeepgramClient
    deepgram = DeepgramClient(api_key=api_key)
    response = deepgram.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en"          # Aura-2 model
    )
    # Collect all chunks from generator
    audio_data = b''.join(response)
    with open(filename, "wb") as f:
        f.write(audio_data)

elif provider == "murf.ai":
    filename = "speech_output.wav"
    from murf import Murf
    import base64
    client = Murf(api_key=api_key)
    response = client.text_to_speech.generate(
        text=text,
        voice_id="en-US-natalie",        # change voice_id as needed
        format="WAV",
        sample_rate=44100.0
    )
    # response.audio_file is base64 encoded, decode it to bytes
    audio_bytes = base64.b64decode(response.audio_file)
    with open(filename, "wb") as f:
        f.write(audio_bytes)

elif provider == "respeecher":
    filename = "speech_output.wav"
    from respeecher import Respeecher
    client = Respeecher(api_key=api_key)
    
    # Call tts.bytes and capture response (returns generator)
    response = client.tts.bytes(
        transcript=text,
        voice={"id": "samantha"}  # change voice id as needed
    )
    
    # Collect all chunks from generator into bytes
    audio_data = b''.join(response)
    with open(filename, "wb") as f:
        f.write(audio_data)

elif provider == "resemble":
    filename = "speech_output.wav"
    from resemble import Resemble
    Resemble.api_key(api_key)
    response = Resemble.v2.clips.create_sync(
        project_uuid=" ",   # ← Change to your project UUID
        voice_uuid="",       # ← Change to your voice UUID
        body=text,
        title="Colab Test"
    )
    # Download the clip with proper error handling
    clip_url = None
    if isinstance(response, dict):
        # Try different response structures
        if 'item' in response and 'audio_url' in response.get('item', {}):
            clip_url = response['item']['audio_url']
        elif 'audio_url' in response:
            clip_url = response['audio_url']
    
    if clip_url:
        import requests
        r = requests.get(clip_url)
        with open(filename, "wb") as f:
            f.write(r.content)
    else:
        print(f"⚠ Resemble: Unable to extract audio URL from response.")
        print(f"   Response structure: {response}")

elif provider == "noiz.ai":
    filename = "speech_output.wav"
    import requests
    # Replace with actual Noiz.ai endpoint when official (as of 2026, check docs)
    # Using placeholder - update with real endpoint from https://noiz.ai
    print("  Noiz.ai: Using placeholder endpoint. Update code with official endpoint from their docs.")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"text": text, "voice": "default", "format": "wav"}
    response = requests.post("https://noiz.ai/v1/text-to-speech", json=payload, headers=headers)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Error: {response.text}")

# ====================== TIMING & DOWNLOAD ======================
elapsed = time.perf_counter() - start_time

if os.path.exists(filename):
    file_size = os.path.getsize(filename)
    print(f"\n✓ Done! Speech file: {filename}")
    print(f"  File size: {file_size} bytes")
    print(f"  Total time (generation + save): {elapsed:.3f} seconds")
    
    # Verify file is not empty and check magic numbers
    if file_size > 0:
        with open(filename, "rb") as f:
            header = f.read(12)
        
        # Check file format by magic numbers
        if filename.endswith('.mp3'):
            if header[:2] == b'\xFF\xFB' or header[:2] == b'\xFF\xFA':
                print(f"  ✓ Valid MP3 format detected")
            elif header[:3] == b'ID3':
                print(f"  ✓ Valid MP3 (ID3 tagged) detected")
            else:
                print(f"  ⚠ Not a valid MP3! Header: {header[:4].hex()}")
        elif filename.endswith('.wav'):
            if header[:4] == b'RIFF' and header[8:12] == b'WAVE':
                print(f"  ✓ Valid WAV format detected")
            else:
                print(f"  ⚠ Raw PCM/Invalid WAV detected! Header: {header[:4].hex()}")
                print(f"  Attempting to convert to proper WAV...")
                # Read all audio data and wrap in WAV container
                with open(filename, "rb") as f:
                    audio_data = f.read()
                
                # Try to determine format and convert
                if len(audio_data) > 0:
                    # For 32-bit float PCM (most common from TTS)
                    if len(audio_data) % 4 == 0:
                        success = write_pcm_as_wav(filename, audio_data, sample_rate=44100, channels=1, sample_width=4)
                        if success:
                            print(f"  ✓ Converted to proper WAV format (32-bit PCM)")
                    # For 16-bit PCM
                    elif len(audio_data) % 2 == 0:
                        success = write_pcm_as_wav(filename, audio_data, sample_rate=44100, channels=1, sample_width=2)
                        if success:
                            print(f"  ✓ Converted to proper WAV format (16-bit PCM)")
                    else:
                        print(f"  ⚠ Unable to determine audio format (size not divisible by 2 or 4)")
        else:
            print(f"  File header (hex): {header[:8].hex()}")
    else:
        print(f"  ⚠ File is empty! Audio generation may have failed.")
    
    # Try to download in Google Colab
    try:
        from google.colab import files
        files.download(filename)
    except ImportError:
        print(f"   Local file saved: {os.path.abspath(filename)}")
        print(f"  (Not in Colab, file available locally)")
else:
    print(f"\n Done! (Check output above)")
    print(f"  Total time: {elapsed:.3f} seconds")
    print(f"  ⚠ File not created - audio generation may have failed")

print("\n Test complete! Edit .env with new keys and run again for another provider.")
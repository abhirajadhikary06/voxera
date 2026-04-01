import whisper
import jiwer
import os

def calculate_tts_accuracy(audio_path, reference_text, model_name):
    # 1. Check if file exists
    if not os.path.exists(audio_path):
        return f"Error: File {audio_path} not found."

    print(f"--- Testing Accuracy for: {model_name} ---")
    
    # 2. Load Whisper Model (Base is fast and accurate enough for testing)
    # Options: 'tiny', 'base', 'small', 'medium', 'large'
    stt_model = whisper.load_model("base")

    # 3. Transcribe the audio (STT)
    print("Transcribing audio...")
    result = stt_model.transcribe(audio_path)
    hypothesis_text = result['text'].strip()

    # 4. Text Normalization (Critical for fair testing)
    # This removes punctuation and forced lowercase so "Hello!" matches "hello"
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip()
    ])

    clean_reference = transformation(reference_text)
    clean_hypothesis = transformation(hypothesis_text)

    # 5. Calculate Word Error Rate (WER)
    wer = jiwer.wer(clean_reference, clean_hypothesis)
    
    # 6. Convert WER to Accuracy
    # Accuracy = (1 - WER) * 100
    # Note: Accuracy can technically be negative if the model adds too many extra words
    accuracy = max(0, (1 - wer) * 100)

    print("\n" + "="*40)
    print(f"MODEL NAME:   {model_name}")
    print(f"ORIGINAL:     {reference_text}")
    print(f"STT HEARD:    {hypothesis_text}")
    print("-" * 40)
    print(f"ACCURACY:     {accuracy:.2f}%")
    print("="*40 + "\n")

if __name__ == "__main__":
    # USER INPUTS
    # Replace these with your actual file path and text
    target_audio = "speech_output.wav" 
    target_model = ""
    original_text = ""

    calculate_tts_accuracy(target_audio, original_text, target_model)
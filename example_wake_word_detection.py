#!/usr/bin/env python3
"""
Example demonstrating wake word detection with identification of which wake word was triggered.

This example shows how to use the updated RealtimeSTT library to detect multiple wake words
and identify which specific wake word was detected.
"""

from RealtimeSTT import AudioToTextRecorder
import time

def main():
    print("Wake Word Detection Example")
    print("===========================")
    print("This example demonstrates detection of multiple wake words.")
    print("Try saying different wake words to see which one is detected.")
    print()

    # Callback function that receives the detected wake word name
    def on_wakeword_detected(wake_word_name=None):
        if wake_word_name:
            print(f"\n🎯 Wake word detected: '{wake_word_name}'")
        else:
            print(f"\n🎯 Wake word detected (name not available)")
        print("Listening for speech...")

    def on_recording_start():
        print("🎤 Recording started...")

    def on_recording_stop():
        print("⏹️  Recording stopped. Transcribing...")

    def on_wakeword_timeout():
        print("\n⏱️  Wake word timeout. Say a wake word to start recording.")

    def on_wakeword_detection_start():
        print("\n👂 Listening for wake words...")

    def process_text(text):
        if text:
            print(f"\n📝 Transcription: {text}")
        # Continue listening after transcription
        return True

    # Initialize the recorder with multiple wake words
    # For this example, we'll use the OpenWakeWord backend
    # You'll need to download appropriate .onnx model files for your wake words
    recorder_config = {
        'spinner': False,
        'model': 'tiny',  # Using tiny model for faster performance in this example
        'language': 'en',
        'wakeword_backend': 'openwakeword',
        'wake_words_sensitivity': 0.6,
        'on_wakeword_detected': on_wakeword_detected,
        'on_recording_start': on_recording_start,
        'on_recording_stop': on_recording_stop,
        'on_wakeword_timeout': on_wakeword_timeout,
        'on_wakeword_detection_start': on_wakeword_detection_start,
        'wake_word_activation_delay': 0,
        'wake_word_timeout': 5.0,
        'post_speech_silence_duration': 0.4,
    }

    # If using specific OpenWakeWord models, uncomment and modify:
    # recorder_config['openwakeword_model_paths'] = "model1.onnx,model2.onnx"
    
    # If using Porcupine wake words instead:
    # recorder_config['wakeword_backend'] = 'pvporcupine'
    # recorder_config['wake_words'] = 'jarvis,computer,assistant'

    print("Initializing audio recorder...")
    
    try:
        with AudioToTextRecorder(**recorder_config) as recorder:
            print("\n✅ Recorder initialized successfully!")
            print("Say a wake word to start recording.")
            print("Press Ctrl+C to exit.\n")
            
            while True:
                # Wait for wake word and transcribe speech
                text = recorder.text()
                
                # Process the transcribed text
                if not process_text(text):
                    break
                    
                # You can also get the last detected wake word at any time:
                last_wake_word = recorder.get_last_detected_wake_word()
                if last_wake_word:
                    print(f"(Last wake word used: {last_wake_word})")
                    
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    main()
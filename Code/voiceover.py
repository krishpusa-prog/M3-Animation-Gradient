"""Optional neural TTS generation; defaults to a warm adult female voice.
Install edge-tts and run: python voiceover.py
Narration segments are stored in ../Narration.md; edit VOICE below if desired.
"""
import asyncio
import edge_tts
VOICE = "en-US-JennyNeural"  # swap to another installed Edge TTS voice
TEXT = "Welcome to a visual guide to the gradient, the direction of steepest increase."
async def main():
    await edge_tts.Communicate(TEXT, VOICE, rate="-5%", pitch="+2Hz").save("../voiceover_sample.mp3")
if __name__ == "__main__":
    asyncio.run(main())

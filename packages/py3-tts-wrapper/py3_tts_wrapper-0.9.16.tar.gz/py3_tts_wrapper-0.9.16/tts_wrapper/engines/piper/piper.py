from typing import Any, List, Optional, Dict

from tts_wrapper.exceptions import UnsupportedFileFormat

from ...tts import AbstractTTS, FileFormat
from . import PiperClient, PiperSSML
import threading
import time
from ...engines.utils import estimate_word_timings  

class PiperTTS(AbstractTTS):

    def __init__(self, client: PiperClient, lang: Optional[str] = None, voice: Optional[str] = None):
        super().__init__()
        self._client = client
        self._voices = self.get_voices()
        self.set_voice(voice or "Joanna", lang or "en-US")
        self.audio_rate = 16000

    def synth_to_bytes(self, text: Any) -> bytes:
        word_timings = estimate_word_timings(str(text))
        self.set_timings(word_timings)
        audio_bytes = self._client.synth(str(text))
        
        if self.audio_bytes[:4] == b'RIFF':
            audio_bytes = self._strip_wav_header(audio_bytes)
        
        return audio_bytes

    @property
    def ssml(self) -> PiperSSML:
        return PiperSSML()

    def get_voices(self) -> List[Dict[str, Any]]:
        return self._client.get_voices()

    def set_voice(self, voice_id: str, lang_id: str):
        super().set_voice(voice_id)
        self._voice = voice_id
        self._lang = lang_id

    def construct_prosody_tag(self, text:str ) -> str:
        pass
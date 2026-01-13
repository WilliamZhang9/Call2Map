# utils/audio_processing.py
import base64
import struct
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Handle audio format conversions for Twilio"""
    
    # μ-law decompression lookup table
    MULAW_TO_LINEAR = [
        -32124, -31100, -30076, -29052, -28028, -27004, -25980, -24956,
        -23932, -22908, -21884, -20860, -19836, -18812, -17788, -16764,
        -15996, -15484, -14972, -14460, -13948, -13436, -12924, -12412,
        -11900, -11388, -10876, -10364, -9852, -9340, -8828, -8316,
        -7932, -7676, -7420, -7164, -6908, -6652, -6396, -6140,
        -5884, -5628, -5372, -5116, -4860, -4604, -4348, -4092,
        -3900, -3772, -3644, -3516, -3388, -3260, -3132, -3004,
        -2876, -2748, -2620, -2492, -2364, -2236, -2108, -1980,
        -1884, -1820, -1756, -1692, -1628, -1564, -1500, -1436,
        -1372, -1308, -1244, -1180, -1116, -1052, -988, -924,
        -876, -844, -812, -780, -748, -716, -684, -652,
        -620, -588, -556, -524, -492, -460, -428, -396,
        -372, -356, -340, -324, -308, -292, -276, -260,
        -244, -228, -212, -196, -180, -164, -148, -132,
        -120, -112, -104, -96, -88, -80, -72, -64,
        -56, -48, -40, -32, -24, -16, -8, 0,
        32124, 31100, 30076, 29052, 28028, 27004, 25980, 24956,
        23932, 22908, 21884, 20860, 19836, 18812, 17788, 16764,
        15996, 15484, 14972, 14460, 13948, 13436, 12924, 12412,
        11900, 11388, 10876, 10364, 9852, 9340, 8828, 8316,
        7932, 7676, 7420, 7164, 6908, 6652, 6396, 6140,
        5884, 5628, 5372, 5116, 4860, 4604, 4348, 4092,
        3900, 3772, 3644, 3516, 3388, 3260, 3132, 3004,
        2876, 2748, 2620, 2492, 2364, 2236, 2108, 1980,
        1884, 1820, 1756, 1692, 1628, 1564, 1500, 1436,
        1372, 1308, 1244, 1180, 1116, 1052, 988, 924,
        876, 844, 812, 780, 748, 716, 684, 652,
        620, 588, 556, 524, 492, 460, 428, 396,
        372, 356, 340, 324, 308, 292, 276, 260,
        244, 228, 212, 196, 180, 164, 148, 132,
        120, 112, 104, 96, 88, 80, 72, 64,
        56, 48, 40, 32, 24, 16, 8, 0
    ]
    
    @staticmethod
    def mulaw_to_pcm(mulaw_data: bytes) -> bytes:
        """Convert μ-law to 16-bit PCM"""
        try:
            pcm_data = b''
            for byte in mulaw_data:
                linear = AudioProcessor.MULAW_TO_LINEAR[byte]
                pcm_data += struct.pack('<h', linear)
            return pcm_data
        except Exception as e:
            logger.error(f"μ-law to PCM conversion error: {e}")
            return b''
    
    @staticmethod
    def resample_audio(audio_data: bytes, from_rate: int, to_rate: int) -> bytes:
        """Simple resampling for 8kHz -> 16kHz"""
        if from_rate == to_rate:
            return audio_data
        
        # Simple duplication for 8k->16k
        if from_rate == 8000 and to_rate == 16000:
            resampled = b''
            for i in range(0, len(audio_data), 2):
                sample = audio_data[i:i+2]
                resampled += sample + sample
            return resampled
        
        logger.warning(f"Resampling {from_rate}->{to_rate} not implemented")
        return audio_data
    
    @staticmethod
    def base64_to_bytes(b64_string: str) -> bytes:
        """Decode base64 audio from Twilio"""
        return base64.b64decode(b64_string)
    
    @staticmethod
    def bytes_to_base64(data: bytes) -> str:
        """Encode audio to base64 for Twilio"""
        return base64.b64encode(data).decode('utf-8')

from pathlib import Path
import math
import struct
import tempfile
import unittest
import wave

from ventura_voice import analyze_wav, is_probably_silent


class AudioPipelineTests(unittest.TestCase):
    def _wav(self, samples: list[int], sample_rate: int = 8000) -> Path:
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp.close()
        path = Path(tmp.name)
        with wave.open(str(path), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(sample_rate)
            handle.writeframes(struct.pack(f"<{len(samples)}h", *samples))
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_analyzes_duration_peak_and_rms(self):
        samples = [0, 16384, -16384, 0] * 2000
        metrics = analyze_wav(self._wav(samples))
        self.assertEqual(metrics.channels, 1)
        self.assertEqual(metrics.sample_rate, 8000)
        self.assertEqual(metrics.frames, 8000)
        self.assertAlmostEqual(metrics.duration_seconds, 1.0, places=6)
        self.assertAlmostEqual(metrics.peak, 0.5, places=4)
        self.assertAlmostEqual(metrics.rms, math.sqrt(0.125), places=4)
        self.assertFalse(is_probably_silent(metrics))

    def test_detects_silence(self):
        metrics = analyze_wav(self._wav([0] * 800))
        self.assertEqual(metrics.rms, 0.0)
        self.assertTrue(is_probably_silent(metrics))

    def test_rejects_negative_silence_threshold(self):
        metrics = analyze_wav(self._wav([0] * 8))
        with self.assertRaisesRegex(ValueError, "non-negative"):
            is_probably_silent(metrics, -0.1)


if __name__ == "__main__":
    unittest.main()

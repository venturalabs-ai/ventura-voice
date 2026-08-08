from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import struct
import wave


@dataclass(frozen=True)
class AudioMetrics:
    channels: int
    sample_rate: int
    frames: int
    duration_seconds: float
    rms: float
    peak: float


def analyze_wav(path: str | Path) -> AudioMetrics:
    """Analyze uncompressed PCM WAV using only the Python standard library."""
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_rate = handle.getframerate()
        frames = handle.getnframes()
        sample_width = handle.getsampwidth()
        compression = handle.getcomptype()
        raw = handle.readframes(frames)

    if compression != "NONE":
        raise ValueError("compressed WAV is not supported")
    if sample_width != 2:
        raise ValueError("only 16-bit PCM WAV is supported")
    if channels <= 0 or sample_rate <= 0:
        raise ValueError("invalid WAV metadata")

    sample_count = len(raw) // 2
    samples = struct.unpack(f"<{sample_count}h", raw) if sample_count else ()
    if not samples:
        rms = 0.0
        peak = 0.0
    else:
        scale = 32768.0
        rms = math.sqrt(sum((sample / scale) ** 2 for sample in samples) / len(samples))
        peak = max(abs(sample) for sample in samples) / scale

    return AudioMetrics(
        channels=channels,
        sample_rate=sample_rate,
        frames=frames,
        duration_seconds=frames / sample_rate,
        rms=rms,
        peak=peak,
    )


def is_probably_silent(metrics: AudioMetrics, threshold: float = 0.01) -> bool:
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    return metrics.rms < threshold

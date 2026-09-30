from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TSNStream:
    name: str
    period_ms: float
    payload_bytes: int
    deadline_ms: float
    priority: int


@dataclass(frozen=True, slots=True)
class MCSProfile:
    name: str
    spectral_efficiency: float
    threshold_db: float


MCS_TABLE = (
    MCSProfile("QPSK-robust", 1.0, 0.0),
    MCSProfile("QPSK", 1.8, 4.0),
    MCSProfile("16QAM", 3.0, 9.0),
    MCSProfile("64QAM", 4.5, 15.0),
    MCSProfile("64QAM-high", 5.5, 19.0),
)

from __future__ import annotations

from .models import MCSProfile, MCS_TABLE


class FixedPolicy:
    def __init__(self, index: int = 2) -> None:
        self.index = index

    def select(self, snr_db: float, queue_depth: int = 0) -> MCSProfile:
        return MCS_TABLE[self.index]


class ThresholdPolicy:
    def select(self, snr_db: float, queue_depth: int = 0) -> MCSProfile:
        selected = MCS_TABLE[0]
        for profile in MCS_TABLE:
            if snr_db >= profile.threshold_db:
                selected = profile
        return selected

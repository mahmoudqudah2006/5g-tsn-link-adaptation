from __future__ import annotations

import numpy as np


class CorrelatedSNR:
    def __init__(
        self,
        mean_db: float = 12.0,
        std_db: float = 4.0,
        rho: float = 0.95,
        seed: int = 7,
    ) -> None:
        self.mean_db = mean_db
        self.std_db = std_db
        self.rho = rho
        self.rng = np.random.default_rng(seed)
        self.value = mean_db

    def reset(self) -> float:
        self.value = float(self.rng.normal(self.mean_db, self.std_db))
        return self.value

    def step(self) -> float:
        innovation = self.std_db * np.sqrt(1.0 - self.rho**2)
        self.value = float(
            self.rho * self.value
            + (1.0 - self.rho) * self.mean_db
            + self.rng.normal(0.0, innovation)
        )
        return self.value


class ConstantSNR:
    def __init__(self, value: float) -> None:
        self.value = value

    def reset(self) -> float:
        return self.value

    def step(self) -> float:
        return self.value

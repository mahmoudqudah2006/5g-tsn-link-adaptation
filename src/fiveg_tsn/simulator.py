from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .models import MCSProfile, TSNStream


@dataclass(slots=True)
class Packet:
    stream: TSNStream
    created_ms: float
    remaining_bytes: float
    retries: int = 0


def bler_probability(snr_db: float, mcs: MCSProfile, slope_db: float = 1.8) -> float:
    return float(1.0 / (1.0 + np.exp((snr_db - mcs.threshold_db) / slope_db)))


def simulate(
    streams: list[TSNStream],
    policy,
    channel,
    *,
    duration_ms: float = 1000.0,
    slot_ms: float = 0.5,
    bandwidth_hz: float = 20e6,
    max_retries: int = 3,
    seed: int = 7,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    queue: list[Packet] = []
    next_arrival = {stream.name: 0.0 for stream in streams}
    generated = delivered = deadline_missed = dropped = retransmissions = 0
    delivered_bytes = 0
    latencies: list[float] = []
    snr = channel.reset()

    steps = int(np.ceil(duration_ms / slot_ms))
    for step in range(steps):
        now_ms = step * slot_ms
        for stream in streams:
            while next_arrival[stream.name] <= now_ms + 1e-9:
                queue.append(Packet(stream, next_arrival[stream.name], float(stream.payload_bytes)))
                generated += 1
                next_arrival[stream.name] += stream.period_ms

        still_valid: list[Packet] = []
        for packet in queue:
            if now_ms - packet.created_ms > packet.stream.deadline_ms:
                deadline_missed += 1
            else:
                still_valid.append(packet)
        queue = still_valid

        if queue:
            queue.sort(
                key=lambda packet: (
                    packet.stream.priority,
                    packet.created_ms + packet.stream.deadline_ms,
                    packet.created_ms,
                )
            )
            packet = queue[0]
            mcs = policy.select(snr, len(queue))
            capacity_bytes = bandwidth_hz * (slot_ms / 1000.0) * mcs.spectral_efficiency / 8.0
            packet.remaining_bytes -= capacity_bytes
            if packet.remaining_bytes <= 0:
                if rng.random() >= bler_probability(snr, mcs):
                    delivered += 1
                    delivered_bytes += packet.stream.payload_bytes
                    latencies.append(now_ms + slot_ms - packet.created_ms)
                    queue.pop(0)
                else:
                    retransmissions += 1
                    packet.retries += 1
                    if packet.retries > max_retries:
                        dropped += 1
                        queue.pop(0)
                    else:
                        packet.remaining_bytes = float(packet.stream.payload_bytes)
        snr = channel.step()

    queued_at_end = len(queue)
    latency = np.asarray(latencies, dtype=float)
    return {
        "generated": generated,
        "delivered": delivered,
        "dropped_after_retries": dropped,
        "deadline_missed": deadline_missed,
        "queued_at_end": queued_at_end,
        "delivery_ratio": delivered / generated if generated else 0.0,
        "deadline_miss_ratio": deadline_missed / generated if generated else 0.0,
        "retransmissions": retransmissions,
        "mean_latency_ms": float(latency.mean()) if len(latency) else None,
        "p99_latency_ms": float(np.percentile(latency, 99)) if len(latency) else None,
        "throughput_mbps": delivered_bytes * 8.0 / (duration_ms / 1000.0) / 1e6,
    }

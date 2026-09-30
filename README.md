# 5G–TSN Link Adaptation Simulator

A research-oriented simulator for studying the interaction between **time-sensitive traffic**, **wireless link quality**, and **adaptive modulation/coding decisions**.

This repository is inspired by Mahmoud Alqudah's research direction in 5G–TSN integration and adaptive channel modulation/coding. The implementation is deliberately transparent and lightweight so policies can be inspected, compared, and replaced.

> **Important:** this is an abstract link/queue simulator. It is **not** a 3GPP-compliant NR simulator and it does not claim conformance with IEEE TSN standards. For protocol-accurate work, integrate the policies with tools such as ns-3/5G-LENA or OMNeT++ models.

## Model

The simulator combines four components:

1. periodic TSN-like traffic streams with deadlines and priorities
2. a temporally correlated wireless SNR process
3. an abstract MCS table with spectral efficiency and logistic BLER curves
4. a slot-based priority/deadline queue

## Default traffic

The CLI ships with three representative streams:

| Stream | Period | Payload | Deadline | Priority |
|---|---:|---:|---:|---:|
| control | 2 ms | 300 B | 2 ms | 0 |
| sensor | 5 ms | 500 B | 5 ms | 1 |
| telemetry | 10 ms | 900 B | 10 ms | 2 |

Priority `0` is highest.

## Policies

- `fixed`: fixed mid-level MCS
- `adaptive`: SNR-threshold MCS selection

The output compares delivery ratio, deadline misses, latency percentiles, retransmissions, and throughput.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

fiveg-tsn compare --duration-ms 2000 --seed 7 --output results/comparison.json
```

## Research questions this can support

- How does aggressive MCS selection affect deadline misses?
- How should reliability penalties change for critical streams?
- How does channel correlation affect deterministic traffic?
- Can ML/RL reduce deadline violations versus threshold policies?
- What state should an adaptive policy observe: SNR only, or also queue/deadline state?

## Roadmap

- [ ] 5G NR numerology/resource-grid adapter
- [ ] HARQ timing abstraction
- [ ] TSN gate-control-list traffic
- [ ] multi-flow schedulers
- [ ] RL policy integration
- [ ] OMNeT++/ns-3 trace interchange
- [ ] calibration from link-level BLER curves
- [ ] reproducible paper experiment manifests

## License

MIT

---

**Mahmoud Alqudah** · 5G · Time-Sensitive Networking · Adaptive Modulation & Coding

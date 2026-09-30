from fiveg_tsn.channel import ConstantSNR
from fiveg_tsn.models import TSNStream
from fiveg_tsn.policies import ThresholdPolicy
from fiveg_tsn.simulator import simulate


def test_light_load_high_snr_delivers_packets() -> None:
    streams = [TSNStream("control", 10.0, 100, 10.0, 0)]
    result = simulate(
        streams,
        ThresholdPolicy(),
        ConstantSNR(35.0),
        duration_ms=100.0,
        slot_ms=0.5,
        seed=2,
    )
    assert result["delivery_ratio"] > 0.8
    assert result["deadline_miss_ratio"] < 0.2

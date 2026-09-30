from fiveg_tsn.policies import ThresholdPolicy


def test_threshold_policy_is_monotonic() -> None:
    policy = ThresholdPolicy()
    efficiencies = [policy.select(snr).spectral_efficiency for snr in [-5, 5, 12, 25]]
    assert efficiencies == sorted(efficiencies)

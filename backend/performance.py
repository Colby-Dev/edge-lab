def roi(total_stake: float, total_return: float) -> float:
    if total_stake <= 0:
        return 0.0
    return (total_return - total_stake) / total_stake


def expected_vs_actual(expected: float, actual: float) -> float:
    return actual - expected


def edge_capture(expected_values: list[float]) -> float:
    if not expected_values:
        return 0.0
    return sum(expected_values) / len(expected_values)

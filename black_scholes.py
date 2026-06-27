import math
from dataclasses import dataclass

from scipy.stats import norm


@dataclass
class OptionInputs:
    spot: float
    strike: float
    time_to_expiry: float
    risk_free_rate: float
    volatility: float
    option_type: str = "call"


def _validate_inputs(inputs: OptionInputs) -> None:
    if inputs.spot <= 0:
        raise ValueError("Spot must be positive.")
    if inputs.strike <= 0:
        raise ValueError("Strike must be positive.")
    if inputs.time_to_expiry <= 0:
        raise ValueError("Time to expiry must be positive.")
    if inputs.volatility <= 0:
        raise ValueError("Volatility must be positive.")
    if inputs.option_type.lower() not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'.")


def d1(inputs: OptionInputs) -> float:
    _validate_inputs(inputs)
    return (
        math.log(inputs.spot / inputs.strike)
        + (inputs.risk_free_rate + 0.5 * inputs.volatility**2) * inputs.time_to_expiry
    ) / (inputs.volatility * math.sqrt(inputs.time_to_expiry))


def d2(inputs: OptionInputs) -> float:
    return d1(inputs) - inputs.volatility * math.sqrt(inputs.time_to_expiry)


def black_scholes_price(inputs: OptionInputs) -> float:
    _validate_inputs(inputs)
    d_1 = d1(inputs)
    d_2 = d2(inputs)

    discount = math.exp(-inputs.risk_free_rate * inputs.time_to_expiry)

    if inputs.option_type.lower() == "call":
        return inputs.spot * norm.cdf(d_1) - inputs.strike * discount * norm.cdf(d_2)

    return inputs.strike * discount * norm.cdf(-d_2) - inputs.spot * norm.cdf(-d_1)


def greeks(inputs: OptionInputs) -> dict:
    _validate_inputs(inputs)
    d_1 = d1(inputs)
    d_2 = d2(inputs)

    sqrt_t = math.sqrt(inputs.time_to_expiry)
    discount = math.exp(-inputs.risk_free_rate * inputs.time_to_expiry)
    pdf_d1 = norm.pdf(d_1)

    gamma = pdf_d1 / (inputs.spot * inputs.volatility * sqrt_t)
    vega = inputs.spot * pdf_d1 * sqrt_t / 100  # per 1 vol point
    theta_common = -(inputs.spot * pdf_d1 * inputs.volatility) / (2 * sqrt_t)

    if inputs.option_type.lower() == "call":
        delta = norm.cdf(d_1)
        theta = (
            theta_common
            - inputs.risk_free_rate * inputs.strike * discount * norm.cdf(d_2)
        ) / 365
    else:
        delta = norm.cdf(d_1) - 1
        theta = (
            theta_common
            + inputs.risk_free_rate * inputs.strike * discount * norm.cdf(-d_2)
        ) / 365

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
    }


def price_and_greeks(inputs: OptionInputs) -> dict:
    result = {"price": black_scholes_price(inputs)}
    result.update(greeks(inputs))
    return result

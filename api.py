from fastapi import FastAPI, Query

from black_scholes import OptionInputs, price_and_greeks


app = FastAPI(
    title="Equity Derivatives Trading Analytics API",
    description="FastAPI service for Black-Scholes option pricing and Greeks.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Equity Derivatives Trading Analytics API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/price")
def price_option(
    spot: float = Query(100.0, gt=0),
    strike: float = Query(100.0, gt=0),
    time_to_expiry: float = Query(0.5, gt=0),
    risk_free_rate: float = Query(0.05),
    volatility: float = Query(0.25, gt=0),
    option_type: str = Query("call", pattern="^(call|put)$"),
):
    inputs = OptionInputs(
        spot=spot,
        strike=strike,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        option_type=option_type,
    )

    result = price_and_greeks(inputs)

    return {
        "inputs": {
            "spot": spot,
            "strike": strike,
            "time_to_expiry": time_to_expiry,
            "risk_free_rate": risk_free_rate,
            "volatility": volatility,
            "option_type": option_type,
        },
        "outputs": result,
    }

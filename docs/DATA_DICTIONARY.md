# Data Dictionary

## State Tensors (Input to Neural Net)

| Variable | Type | Range | Description |
| --- | --- | --- | --- |
| `stock_level` | Float | `[0, inf)` | Current physical inventory units available. |
| `cash_on_hand` | Float | `(-inf, inf)` | Liquid capital available for orders. Negative implies debt. |
| `pending_orders` | Float | `[0, inf)` | Units purchased but not yet received (Work in Progress). |
| `market_volatility` | Float | `[0.0, 1.0]` | Normalized risk score. 0=Stable, 1=Crisis. |

## Action Tensors (Output)

| Variable | Type | Range | Description |
| --- | --- | --- | --- |
| `order_quantity` | Float | `[0, 1000]` | Number of units to purchase immediately. |
| `release_capital` | Float | `[0, 1M]` | Amount of extra credit/liquidity to inject into the system. |

## Metadata

- **WACC (Weighted Average Cost of Capital)**: Set to 8% (`0.08`) in `config.py`.
- **Service_Level_Target**: 99% (`0.99`). The target fill rate the agents aim to maintain.

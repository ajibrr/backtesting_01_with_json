# NIFTY Backtesting Engine

Config-driven 1-minute NIFTY options backtesting skeleton.

The design separates data loading, indicators, conditions, strategy, execution, backtest, reporting and optimization.

Run:

```bash
pip install -r requirements.txt
python main.py
```

The first implementation step is to map the actual JSON/JSONL schema into `data/loaders/`.

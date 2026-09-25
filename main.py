from pathlib import Path
import yaml

from data.loaders.option_chain_loader import OptionChainLoader


PROJECT_ROOT = Path(__file__).resolve().parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "nifty"
    / "NIFTY_20260922_OPTION_CHAIN_1MIN.log"
)

CONFIG_FILE = (
    PROJECT_ROOT
    / "config"
    / "strategy.yaml"
)


def main():

    print("=" * 60)
    print("NIFTY BACKTESTER")
    print("=" * 60)

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    print(f"\nData file:")
    print(DATA_FILE)

    print(f"\nConfig file:")
    print(CONFIG_FILE)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Data file not found: {DATA_FILE}"
        )

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found: {CONFIG_FILE}"
        )

    # --------------------------------------------------------
    # Load configuration
    # --------------------------------------------------------

    with CONFIG_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        config = yaml.safe_load(file)

    print("\nStrategy configuration")
    print("----------------------")
    print(config)

    # --------------------------------------------------------
    # Load option chain
    # --------------------------------------------------------

    loader = OptionChainLoader(DATA_FILE)

    count = loader.count()

    print("\nOption-chain data")
    print("-----------------")
    print(f"Snapshots: {count}")

    # --------------------------------------------------------
    # First snapshot
    # --------------------------------------------------------

    first = loader.first_record()

    print("\nFirst snapshot")
    print("--------------")
    print(f"Timestamp : {first.get('timestamp')}")
    print(f"Spot      : {first.get('current_price')}")
    print(f"ATM       : {first.get('at_the_money_strike')}")
    print(f"Expiry    : {first.get('expiry')}")
    print(f"Strikes   : {len(first.get('strikes', []))}")

    # --------------------------------------------------------
    # Flatten first snapshot
    # --------------------------------------------------------

    rows = loader.flatten_snapshot(first)

    print("\nFlattened records")
    print("-----------------")
    print(f"Records: {len(rows)}")

    # --------------------------------------------------------
    # Display first available option
    # --------------------------------------------------------

    for row in rows:

        if row["ltp"] is not None:

            print("\nExample option")
            print("--------------")
            print(f"Time      : {row['timestamp']}")
            print(f"Type      : {row['option_type']}")
            print(f"Strike    : {row['strike']}")
            print(f"Spot      : {row['spot']}")
            print(f"LTP       : {row['ltp']}")
            print(f"OI        : {row['oi']}")
            print(f"OI Change : {row['oi_change']}")
            print(f"Delta     : {row['delta']}")
            print(f"Gamma     : {row['gamma']}")
            print(f"Theta     : {row['theta']}")
            print(f"Vega      : {row['vega']}")

            break

    print("\n" + "=" * 60)
    print("STEP 2 DATA LOADER SUCCESSFUL")
    print("=" * 60)


if __name__ == "__main__":
    main()
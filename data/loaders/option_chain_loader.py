from pathlib import Path
import json
from typing import Iterator, Dict, Any


class OptionChainLoader:
    """
    Loader for NIFTY 1-minute option-chain .log files.

    Each line in the source file is one JSON snapshot.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def records(self) -> Iterator[Dict[str, Any]]:
        """
        Yield one complete option-chain snapshot at a time.
        """
        with self.path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                try:
                    yield json.loads(line)

                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid JSON at line {line_number}: "
                        f"{self.path}"
                    ) from exc

    def count(self) -> int:
        """
        Count valid JSON snapshots.
        """
        return sum(1 for _ in self.records())

    def first_record(self) -> Dict[str, Any]:
        """
        Return the first snapshot.
        """
        return next(self.records())

    def get_snapshot(self, timestamp: str) -> Dict[str, Any] | None:
        """
        Find a snapshot by timestamp.

        Example:
            2026-09-22 14:12:00
        """
        for record in self.records():
            if record.get("timestamp") == timestamp:
                return record

        return None

    @staticmethod
    def flatten_snapshot(record: Dict[str, Any]):
        """
        Convert one snapshot into normalized option records.

        One strike produces two records:
            CE
            PE
        """

        timestamp = record.get("timestamp")
        spot = record.get("current_price")
        expiry = record.get("expiry")
        exchange = record.get("exchange")
        asset = record.get("asset")

        rows = []

        for strike_data in record.get("strikes", []):

            strike = strike_data.get("strike")

            # --------------------------------------------------
            # CE
            # --------------------------------------------------

            rows.append({
                "timestamp": timestamp,
                "asset": asset,
                "expiry": expiry,
                "exchange": exchange,
                "spot": spot,
                "strike": strike,
                "option_type": "CE",

                "ltp": strike_data.get(
                    "ce_last_traded_price"
                ),

                "ltp_change": strike_data.get(
                    "ce_ltp_change"
                ),

                "oi": strike_data.get(
                    "ce_open_interest"
                ),

                "previous_oi": strike_data.get(
                    "ce_previous_open_interest"
                ),

                "oi_change": strike_data.get(
                    "ce_oi_difference"
                ),

                "volume": strike_data.get(
                    "ce_volume"
                ),

                "iv": strike_data.get(
                    "ce_iv"
                ),

                "delta": strike_data.get(
                    "ce_delta"
                ),

                "gamma": strike_data.get(
                    "ce_gamma"
                ),

                "theta": strike_data.get(
                    "ce_theta"
                ),

                "vega": strike_data.get(
                    "ce_vega"
                ),
            })

            # --------------------------------------------------
            # PE
            # --------------------------------------------------

            rows.append({
                "timestamp": timestamp,
                "asset": asset,
                "expiry": expiry,
                "exchange": exchange,
                "spot": spot,
                "strike": strike,
                "option_type": "PE",

                "ltp": strike_data.get(
                    "pe_last_traded_price"
                ),

                "ltp_change": strike_data.get(
                    "pe_ltp_change"
                ),

                "oi": strike_data.get(
                    "pe_open_interest"
                ),

                "previous_oi": strike_data.get(
                    "pe_previous_open_interest"
                ),

                "oi_change": strike_data.get(
                    "pe_oi_difference"
                ),

                "volume": strike_data.get(
                    "pe_volume"
                ),

                "iv": strike_data.get(
                    "pe_iv"
                ),

                "delta": strike_data.get(
                    "pe_delta"
                ),

                "gamma": strike_data.get(
                    "pe_gamma"
                ),

                "theta": strike_data.get(
                    "pe_theta"
                ),

                "vega": strike_data.get(
                    "pe_vega"
                ),
            })

        return rows
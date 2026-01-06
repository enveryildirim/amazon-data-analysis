"""Data Loader - Pandas version for immediate data exploration.

This module provides pandas-based data loading for quick exploration
without requiring Java/Spark. For production-scale processing,
use data_loader_spark.py after installing Java.
"""

import logging
from pathlib import Path
from typing import Dict

import pandas as pd


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_amazon_sales(input_path: str) -> pd.DataFrame:
    """Load and clean Amazon Sale Report.csv.

    Args:
        input_path: Path to Amazon Sale Report.csv

    Returns:
        Cleaned DataFrame
    """
    logging.info("Loading Amazon Sale Report.csv")

    df = pd.read_csv(input_path)

    df = df.dropna(subset=["Date"]).copy()
    df["date"] = pd.to_datetime(df["Date"], format="%m-%d-%y", errors="coerce")
    df["amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["b2b"] = df["B2B"].astype(bool)

    # Drop original columns to prevent duplication in Spark (case-insensitive)
    df = df.drop(columns=["Date", "Amount", "Qty", "B2B"], errors="ignore")

    return df


def load_international_sales(input_path: str) -> pd.DataFrame:
    """Load and clean International sale Report.csv.

    Args:
        input_path: Path to International sale Report.csv

    Returns:
        Cleaned DataFrame
    """
    logging.info("Loading International sale Report.csv")

    df = pd.read_csv(input_path)

    df["date"] = pd.to_datetime(df["DATE"], format="%m-%d-%y", errors="coerce")
    df["rate"] = pd.to_numeric(df["RATE"], errors="coerce")
    df["gross_amt"] = pd.to_numeric(df["GROSS AMT"], errors="coerce")
    df["pcs"] = pd.to_numeric(df["PCS"], errors="coerce")

    # Drop original columns to prevent duplication
    df = df.drop(columns=["DATE", "RATE", "GROSS AMT", "PCS"], errors="ignore")

    return df


def load_inventory(input_path: str) -> pd.DataFrame:
    """Load and clean Sale Report.csv (inventory data).

    Args:
        input_path: Path to Sale Report.csv

    Returns:
        Cleaned DataFrame
    """
    logging.info("Loading Sale Report.csv")

    df = pd.read_csv(input_path)

    df["category"] = (
        df["Category"].str.replace(r"^AN\s*:\s*", "", regex=True).str.strip()
    )
    df["stock"] = pd.to_numeric(df["Stock"], errors="coerce").fillna(0).astype(int)

    # Drop original columns
    df = df.drop(columns=["Category", "Stock"], errors="ignore")

    return df


def load_pricing_data(input_path: str) -> pd.DataFrame:
    """Load pricing data from May-2022 or similar files.

    Args:
        input_path: Path to pricing CSV

    Returns:
        Cleaned DataFrame
    """
    logging.info(f"Loading pricing data from {input_path}")

    df = pd.read_csv(input_path)

    df["weight"] = pd.to_numeric(df["Weight"], errors="coerce")
    cols_to_drop = ["Weight"]

    if "TP" in df.columns:
        df["tp"] = pd.to_numeric(df["TP"], errors="coerce")
        cols_to_drop.append("TP")
    elif "TP 1" in df.columns:
        df["tp"] = pd.to_numeric(df["TP 1"], errors="coerce")
        cols_to_drop.append("TP 1")

    for col_name in df.columns:
        if "MRP" in col_name or "Mrp" in col_name or "mrp" in col_name:
            df[col_name] = pd.to_numeric(df[col_name], errors="coerce")

    df = df.drop(columns=cols_to_drop, errors="ignore")

    return df


def load_expenses(input_path: str) -> pd.DataFrame:
    """Load expense data.

    Args:
        input_path: Path to expenses CSV

    Returns:
        DataFrame
    """
    logging.info("Loading Expense IIGF.csv")
    df = pd.read_csv(input_path)
    return df


def load_warehouse_costs(input_path: str) -> pd.DataFrame:
    """Load warehouse cost comparison data.

    Args:
        input_path: Path to warehouse costs CSV

    Returns:
        DataFrame
    """
    logging.info("Loading Cloud Warehouse Compersion Chart.csv")
    df = pd.read_csv(input_path)
    return df


def save_to_parquet(df: pd.DataFrame, output_path: str) -> None:
    """Save DataFrame to Parquet format.

    Args:
        df: DataFrame to save
        output_path: Output path for Parquet file
    """
    logging.info(f"Saving to {output_path}")
    df.to_parquet(
        output_path, index=False, allow_truncated_timestamps=True, coerce_timestamps="us"
    )
    logging.info(f"Saved {len(df)} rows to {output_path}")


def main():
    """Main execution function."""
    try:
        datasets_dir = Path("datasets")
        processed_dir = Path("processed")
        processed_dir.mkdir(exist_ok=True)

        data_files = {
            "amazon_sales": datasets_dir / "Amazon Sale Report.csv",
            "international_sales": datasets_dir / "International sale Report.csv",
            "inventory": datasets_dir / "Sale Report.csv",
            "pricing_may2022": datasets_dir / "May-2022.csv",
            "pricing_march2021": datasets_dir / "P  L March 2021.csv",
            "expenses": datasets_dir / "Expense IIGF.csv",
            "warehouse_costs": datasets_dir / "Cloud Warehouse Compersion Chart.csv",
        }

        loaders = {
            "amazon_sales": load_amazon_sales,
            "international_sales": load_international_sales,
            "inventory": load_inventory,
            "pricing_may2022": load_pricing_data,
            "pricing_march2021": load_pricing_data,
            "expenses": load_expenses,
            "warehouse_costs": load_warehouse_costs,
        }

        for name, path in data_files.items():
            if path.exists():
                logging.info(f"Processing {name}")
                df = loaders[name](str(path))
                output_path = processed_dir / f"{name}.parquet"
                save_to_parquet(df, str(output_path))
            else:
                logging.warning(f"File not found: {path}")

        logging.info("Data loading completed successfully!")

    except Exception as e:
        logging.error(f"Error during data loading: {e}")
        raise


if __name__ == "__main__":
    main()

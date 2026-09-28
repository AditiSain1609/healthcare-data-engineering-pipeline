import pandas as pd
import os

from src.ingestion import load_all_data
from src.cleaning import clean_all_data
from src.validation import validate_all_data


OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# DATA QUALITY REPORT
# =========================================================

def calculate_quality_score(total_records, invalid_records, missing_values):

    if total_records == 0:
        return 0

    invalid_score = (invalid_records / total_records) * 100
    missing_score = min(
        (missing_values / total_records) * 100,
        100
    )

    score = 100 - invalid_score - missing_score

    return max(round(score, 2), 0)


def create_quality_report(raw_data, cleaned_data, valid_data):

    report = []

    for table_name in raw_data.keys():

        raw_df = raw_data[table_name]
        cleaned_df = cleaned_data[table_name]
        valid_df = valid_data[table_name]

        total_records = len(raw_df)
        cleaned_records = len(cleaned_df)
        valid_records = len(valid_df)

        invalid_records = (
            cleaned_records - valid_records
        )

        missing_values = int(
            cleaned_df.isnull().sum().sum()
        )

        duplicate_records = (
            total_records - cleaned_records
        )

        quality_score = calculate_quality_score(
            total_records,
            invalid_records,
            missing_values
        )

        report.append({
            "table_name": table_name,
            "total_records": total_records,
            "cleaned_records": cleaned_records,
            "valid_records": valid_records,
            "invalid_records": invalid_records,
            "duplicate_records": duplicate_records,
            "missing_values": missing_values,
            "quality_score": quality_score
        })

    return pd.DataFrame(report)


# =========================================================
# MAIN
# =========================================================

def main():

    print("\nLoading raw data...")
    raw_data = load_all_data()

    print("Cleaning data...")
    cleaned_data = clean_all_data(raw_data)

    print("Validating data...")
    valid_data = validate_all_data(cleaned_data)

    print("\nGenerating data quality report...")

    report = create_quality_report(
        raw_data,
        cleaned_data,
        valid_data
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        "data_quality_report.csv"
    )

    report.to_csv(
        output_file,
        index=False
    )

    print("\n" + "=" * 70)
    print("DATA QUALITY REPORT")
    print("=" * 70)

    print(report.to_string(index=False))

    print("=" * 70)

    print(
        f"\nQuality report saved to: {output_file}"
    )

    print("\nData quality report generated successfully!")


if __name__ == "__main__":
    main()
import logging
import os
import sys

# ---------------------------------------------------------
# Project path
# ---------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from ingestion import load_all_data
from cleaning import clean_all_data
from validation import validate_all_data
from transformation import transform_all_data
from load_to_mysql import load_valid_data_to_mysql


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_DIR,
    "pipeline.log"
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Quality Report
# ---------------------------------------------------------

def generate_quality_report(
    raw_data,
    cleaned_data,
    valid_data
):

    from quality_report import create_quality_report

    report = create_quality_report(
        raw_data,
        cleaned_data,
        valid_data
    )

    output_dir = os.path.join(
        PROJECT_ROOT,
        "output"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    report_file = os.path.join(
        output_dir,
        "data_quality_report.csv"
    )

    report.to_csv(
        report_file,
        index=False
    )

    return report


# ---------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------

def main():

    print()
    print("=" * 70)
    print("HEALTHCARE DATA ENGINEERING PIPELINE")
    print("=" * 70)

    logger.info(
        "Healthcare ETL pipeline started"
    )

    try:

        # =================================================
        # STEP 1 - INGESTION
        # =================================================

        print()
        print("[1/7] Loading raw data...")

        raw_data = load_all_data()

        for name, df in raw_data.items():

            print(
                f"{name}: {len(df)} records"
            )

            logger.info(
                f"Loaded {name}: {len(df)} records"
            )

        print()
        print("Raw data loaded successfully.")

        # =================================================
        # STEP 2 - CLEANING
        # =================================================

        print()
        print("[2/7] Cleaning data...")

        cleaned_data = clean_all_data(
            raw_data
        )

        print(
            "Data cleaning completed."
        )

        logger.info(
            "Data cleaning completed"
        )

        # =================================================
        # STEP 3 - VALIDATION
        # =================================================

        print()
        print("[3/7] Validating data...")

        valid_data = validate_all_data(
            cleaned_data
        )

        print()
        print(
            "VALID DATA SUMMARY"
        )

        print("-" * 50)

        for name, df in valid_data.items():

            print(
                f"{name}: {len(df)} valid records"
            )

            logger.info(
                f"{name}: {len(df)} valid records"
            )

        print("-" * 50)

        print()
        print(
            "Data validation completed."
        )

        # =================================================
        # STEP 4 - TRANSFORMATION
        # =================================================

        print()
        print("[4/7] Transforming data...")

        transformed_data = transform_all_data(
            valid_data
        )

        print(
            "Data transformation completed."
        )

        logger.info(
            "Data transformation completed"
        )

        # =================================================
        # STEP 5 - QUALITY REPORT
        # =================================================

        print()
        print("[5/7] Generating data quality report...")

        quality_report = generate_quality_report(
            raw_data,
            cleaned_data,
            valid_data
        )

        quality_file = os.path.join(
            PROJECT_ROOT,
            "output",
            "data_quality_report.csv"
        )

        print(
            f"Quality report saved: {quality_file}"
        )

        logger.info(
            "Data quality report generated"
        )

        # =================================================
        # STEP 6 - MYSQL
        # =================================================

        print()
        print("[6/7] Loading data into MySQL...")

        load_valid_data_to_mysql(
            valid_data
        )

        print()
        print(
            "MySQL loading completed."
        )

        logger.info(
            "Data successfully loaded into MySQL"
        )

        # =================================================
        # STEP 7 - FINAL SUMMARY
        # =================================================

        print()
        print("[7/7] Pipeline Summary")

        print()
        print("=" * 70)

        print(
            "ETL PIPELINE COMPLETED SUCCESSFULLY!"
        )

        print("=" * 70)

        print()
        print("Final Valid Records:")
        print("-" * 50)

        for name, df in valid_data.items():

            print(
                f"{name:<25} {len(df):>6}"
            )

        print("-" * 50)

        print()
        print(
            "Generated Output Files:"
        )

        print(
            "✓ Invalid records CSV files"
        )

        print(
            "✓ Patient metrics"
        )

        print(
            "✓ Doctor metrics"
        )

        print(
            "✓ Daily revenue"
        )

        print(
            "✓ Monthly revenue"
        )

        print(
            "✓ Data quality report"
        )

        print(
            "✓ Pipeline log"
        )

        print()
        print(
            f"Log file: {LOG_FILE}"
        )

        print()
        print(
            "Healthcare ETL pipeline finished."
        )

        logger.info(
            "Healthcare ETL pipeline completed successfully"
        )

    except Exception as error:

        print()
        print("=" * 70)
        print("PIPELINE FAILED")
        print("=" * 70)

        print()
        print(
            f"Error: {error}"
        )

        logger.exception(
            "Pipeline failed"
        )

        raise


# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
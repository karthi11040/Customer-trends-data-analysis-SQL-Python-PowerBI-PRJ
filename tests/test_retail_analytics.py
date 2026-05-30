import unittest
from pathlib import Path
import tempfile

import pandas as pd

from src.retail_analytics import clean_data, run_pipeline


class RetailAnalyticsTests(unittest.TestCase):
    def test_clean_data_removes_invalid_rows_and_adds_total_amount(self):
        frame = pd.DataFrame(
            [
                {
                    "customer_id": "C001",
                    "category": "Apparel",
                    "price": "20",
                    "quantity": "2",
                    "purchase_date": "2025-01-01",
                },
                {
                    "customer_id": "C002",
                    "category": "Beauty",
                    "price": "",
                    "quantity": "1",
                    "purchase_date": "2025-01-02",
                },
            ]
        )

        cleaned = clean_data(frame)

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(float(cleaned.iloc[0]["total_amount"]), 40.0)

    def test_pipeline_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            raw_path = tmp / "raw.csv"
            processed_path = tmp / "clean.csv"
            db_path = tmp / "analytics.db"
            output_dir = tmp / "out"

            pd.DataFrame(
                [
                    {
                        "customer_id": "C001",
                        "gender": "Female",
                        "age": 29,
                        "city": "New York",
                        "category": "Apparel",
                        "product": "T-Shirt",
                        "price": 25,
                        "quantity": 2,
                        "payment_method": "Card",
                        "purchase_date": "2025-01-04",
                    }
                ]
            ).to_csv(raw_path, index=False)

            summary = run_pipeline(raw_path, processed_path, db_path, output_dir)

            self.assertEqual(summary["rows"], 1)
            self.assertTrue((output_dir / "monthly_sales.csv").exists())
            self.assertTrue((output_dir / "category_performance.csv").exists())
            self.assertTrue((output_dir / "top_customers.csv").exists())


if __name__ == "__main__":
    unittest.main()

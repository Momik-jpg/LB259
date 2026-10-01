import csv
import tempfile
import unittest
from pathlib import Path

import numpy as np

from validate_model import FEATURES, TARGET, load_data, split_by_country


class DataLoadingTests(unittest.TestCase):
    def load_rows(self, rows, include_country=True, encoding="utf-8"):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            fields = [*FEATURES, TARGET]
            if include_country:
                fields.insert(0, "country")
            with path.open("w", encoding=encoding, newline="") as output:
                writer = csv.DictWriter(output, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            return load_data(path)

    @staticmethod
    def valid_rows():
        return [
            {"country": f"Country {index}", **{name: index + 1 for name in FEATURES}, TARGET: index + 2}
            for index in range(6)
        ]

    def test_missing_country_rows_do_not_form_a_validation_group(self):
        rows = self.valid_rows()
        for country in ("", "   ", None):
            rows.append({**rows[0], "country": country, TARGET: 999})
        x, y, countries = self.load_rows(rows)
        self.assertEqual(x.shape, (6, len(FEATURES)))
        self.assertEqual(len(y), 6)
        self.assertNotIn(999, y)
        self.assertEqual(len(set(countries)), 6)

    def test_utf8_bom_export_matches_plain_utf8(self):
        rows = self.valid_rows()
        plain = self.load_rows(rows)
        exported = self.load_rows(rows, encoding="utf-8-sig")
        for expected, actual in zip(plain, exported):
            np.testing.assert_array_equal(actual, expected)

    def test_country_whitespace_does_not_create_extra_groups(self):
        rows = self.valid_rows()[:5]
        rows.append({**rows[0], "country": " Country 0 "})
        with self.assertRaisesRegex(ValueError, "At least six countries"):
            self.load_rows(rows)

    def test_missing_country_column_has_a_clear_validation_error(self):
        rows = [{key: value for key, value in row.items() if key != "country"} for row in self.valid_rows()]
        with self.assertRaisesRegex(ValueError, "At least six countries"):
            self.load_rows(rows, include_country=False)

    def test_invalid_and_non_finite_numbers_are_excluded(self):
        rows = self.valid_rows()
        for value in ("not-a-number", "nan", "inf"):
            rows.append({**rows[0], FEATURES[0]: value})
            rows.append({**rows[0], TARGET: value})
        x, y, _ = self.load_rows(rows)
        self.assertEqual(len(y), 6)
        self.assertTrue(np.isfinite(x).all())
        self.assertTrue(np.isfinite(y).all())


class CountrySplitTests(unittest.TestCase):
    def test_splits_are_disjoint_complete_and_reproducible(self):
        groups = np.repeat([f"Country {index}" for index in range(12)], 4)
        first = split_by_country(groups)
        second = split_by_country(groups)
        all_indices = np.concatenate(first)
        self.assertEqual(len(np.unique(all_indices)), len(groups))
        np.testing.assert_array_equal(np.sort(all_indices), np.arange(len(groups)))
        country_sets = [set(groups[indices]) for indices in first]
        for i in range(3):
            self.assertTrue(country_sets[i])
            np.testing.assert_array_equal(first[i], second[i])
            for j in range(i + 1, 3):
                self.assertTrue(country_sets[i].isdisjoint(country_sets[j]))


if __name__ == "__main__":
    unittest.main()

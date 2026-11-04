#!/usr/bin/env python3
# ©  2026 Terrabit
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
"""Generate l10n_it_zip/data/res.city.csv from the GeoNames postal codes of Italy.

Usage: python3 scripts/generate_city_data.py <path to IT.txt>

IT.txt comes from https://download.geonames.org/export/zip/IT.zip (GeoNames,
Creative Commons Attribution 4.0). Columns: country, postal code, place name,
region, region code, province, province code (sigla), ...
"""

import csv
import sys
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "l10n_it_zip" / "data" / "res.city.csv"


def main(source):
    rows = set()
    with open(source, encoding="utf-8", newline="") as handle:
        for row in csv.reader(handle, delimiter="\t"):
            if len(row) < 7 or row[0] != "IT":
                continue
            zip_code, name, province = row[1].strip(), row[2].strip(), row[6].strip().lower()
            if not (zip_code and name and province):
                continue
            rows.add((zip_code, name, province))
    counter = {}
    with open(OUTPUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["id", "country_id:id", "zipcode", "name", "state_id:id"])
        for zip_code, name, province in sorted(rows):
            index = counter.get(zip_code, 0)
            counter[zip_code] = index + 1
            writer.writerow([f"it_city_{zip_code}_{index}", "base.it", zip_code, name, f"base.state_it_{province}"])
    print(f"{len(rows)} cities written to {OUTPUT}")  # pylint: disable=print-used


if __name__ == "__main__":
    main(sys.argv[1])

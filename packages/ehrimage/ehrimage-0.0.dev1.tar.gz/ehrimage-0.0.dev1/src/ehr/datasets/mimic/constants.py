import pathlib as pl
from dataclasses import dataclass

from ehr.utilities import fs

__all__ = [
    "MIMICMetadata",
]


@dataclass()
class MIMICMetadata:
    dataset_dir = pl.Path.home() / "ds/datasets/physionet.org/files/mimiciv/2.2"
    table_paths = fs.list_nested_files(dataset_dir, fn_includes=[".csv.gz"])
    # Table Overview
    table_map = {fs.filename(tp).split(".csv.gz")[0]: tp for tp in table_paths}

    # Column type: id, date, numeric, text

    # minimum information
    sid_cols = {}
    start_date_cols = {}

    end_date_cols = {}


if __name__ == "__main__":
    from pprint import pprint

    metadata = MIMICMetadata()
    pprint(
        metadata.table_map,
    )

import pathlib as pl

import ibis
from public import public
from dataclasses import dataclass
from enum import StrEnum
import logging

from ehr.utilities import fs
from ehr.utilities.constants import Relationship
from ehr.utilities.metadata import build_table_schema_from_ibis_table
from ehr.datasets._base import TableMetadata

logger = logging.getLogger(__name__)


class Tables(StrEnum):
    edstays = "edstays"
    triage = "triage"


@public
@dataclass()
class MIMICEDMetadata:
    _dataset_dir = pl.Path.home() / "ds/datasets/physionet.org/files/mimic-iv-ed-2.2/ed"
    _table_paths = fs.list_nested_files(_dataset_dir, fn_includes=[".csv.gz"])

    #
    # Table Overview
    #
    # note: ideally this should be derived from {table_name: TableMetadata}, but right now
    # it is done the reverse way: manually construct overview first, then infer TableMetadata from overview
    sid_col_name = "subject_id"
    table_paths = {fs.filename(tp).split(".csv.gz")[0]: tp for tp in _table_paths}
    start_date_cols = {
        Tables.edstays: "intime",
    }
    end_date_cols = {
        Tables.edstays: "outtime",
    }

    relationships = {
        Tables.edstays: [{"relationship": Relationship.LINKS, "table_id": Tables.triage, "foreign_key": "stay_id"}],
        Tables.triage: [{"relationship": Relationship.LINKS, "table_id": Tables.edstays, "foreign_key": "stay_id"}]
    }

    # ------------ Table Metadata ------------

    table_metadatas = {}
    for tn, tp in table_paths.items():
        logger.info(f"Building TableMetadata for {tn}...")

        table_schema = build_table_schema_from_ibis_table(ibis.read_csv(tp))

        table_metadatas[tn] = TableMetadata(
            table_id=tn,
            table_name=tn,
            table_path=tp,
            schema=table_schema,
            sid_col=sid_col_name if sid_col_name in table_schema else None,
            start_date_col=start_date_cols.get(tn),
            end_date_col=end_date_cols.get(tn),
            relationship=relationships.get(tn)
        )

    def __post_init__(self):
        self.sid_cols = {tn: self.sid_col_name for tn in self.table_metadatas if self.sid_col_name in self.schema[tn]}


if __name__ == "__main__":
    from pprint import pprint

    ds_metadata = MIMICEDMetadata()
    pprint(
        ds_metadata.table_metadatas
    )

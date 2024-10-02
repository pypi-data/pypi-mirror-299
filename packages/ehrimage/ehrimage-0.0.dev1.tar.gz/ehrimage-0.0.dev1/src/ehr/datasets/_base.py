from dataclasses import dataclass, field


@dataclass()
class TableMetadata:
    """table level metadata can be used for analysis"""
    table_id: str
    table_name: str
    table_path: str
    schema: dict
    sid_col: str = None
    start_date_col: str = None
    end_date_col: str = None
    id_cols: list[str] = field(default_factory=list)
    code_cols: list[str] = field(default_factory=list)
    numeric_value_cols: list[str] = field(default_factory=list)
    string_value_cols: list[str] = field(default_factory=list)
    relationship: list[dict] = field(default_factory=list)


@dataclass()
class DatasetMetadata:
    #
    # Core
    #
    # {table_name: TableMetadata}
    table_metadatas: dict[str, TableMetadata]

    #
    # Derived info
    #
    # derived from {table: table_metadata} for better lookup operation
    sid_cols = {}  # subject id columns
    vid_cols = {}  # visit id columns
    start_date_cols = {}
    end_date_cols = {}

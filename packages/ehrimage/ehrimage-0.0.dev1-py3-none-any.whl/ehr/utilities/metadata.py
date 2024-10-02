from public import public
from ibis.expr.types.relations import Table
from .constants import DataType


@public
def build_table_schema_from_ibis_table(t: Table) -> dict:
    table_schema = {}
    for col_name, dtype in t.schema().items():
        if "int" in str(dtype).lower():
            table_schema[col_name] = DataType.INT
        elif "string" in str(dtype).lower():
            table_schema[col_name] = DataType.STR
        elif "float" in str(dtype).lower():
            table_schema[col_name] = DataType.FLOAT
        elif any(k in str(dtype).lower() for k in ["timestamp", "date"]):
            table_schema[col_name] = DataType.DATETIME
        elif any(k in str(dtype).lower() for k in ["boolean", "binary"]):
            table_schema[col_name] = DataType.BOOL
        else:
            raise NotImplementedError(f"{dtype} is not accounted for")

    return table_schema

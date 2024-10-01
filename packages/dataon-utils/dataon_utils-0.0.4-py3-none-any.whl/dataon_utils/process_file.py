import re
from collections.abc import Iterable

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

from dataon_utils.hierarchy import build_hierarchy_from_iterable


def get_active_session() -> SparkSession:
    return SparkSession.getActiveSession()


def _count_delimiters(lines: Iterable[str], possible_delimiters: list[str]) -> dict[str, int]:
    delimiter_counts = {delimiter: 0 for delimiter in possible_delimiters}

    for line in lines:
        for delimiter in possible_delimiters:
            delimiter_counts[delimiter] += line.count(delimiter)
    return delimiter_counts


def detect_delimiter(path: str) -> str:
    spark = get_active_session()
    # Read a small portion of the file to detect the delimiter
    sample = spark.read.text(path).limit(10).collect()
    lines: list[str] = [row[0] for row in sample]
    possible_delimiters = ["|", ";", ","]
    delimiter_counts = _count_delimiters(lines, possible_delimiters)

    # Choose the delimiter with the highest count
    detected_delimiter = max(delimiter_counts, key=delimiter_counts.get)
    return detected_delimiter


def load_file(path: str) -> DataFrame:
    spark = get_active_session()
    file_extension = path.split(".")[-1]

    if file_extension == "csv":
        df = spark.read.option("sep", detect_delimiter(path)).csv(
            path, header=True, inferSchema=True
        )
    elif file_extension == "json":
        df = spark.read.json(path, inferSchema=True)
    elif file_extension == "parquet":
        df = spark.read.parquet(path, inferSchema=True)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    return df


def clean_column_name(df: DataFrame, column_name: str | None = None) -> DataFrame:
    def clean_name(col_name) -> str:
        # Replace invalid characters with underscores
        return re.sub(r"[^a-zA-Z0-9_]", "_", col_name)

    if column_name:
        # Clean the specified column name
        new_col_name = clean_name(column_name)
        df = df.withColumnRenamed(column_name, new_col_name)
    else:
        # Clean all column names in the DataFrame
        for col_name in df.columns:
            new_col_name = clean_name(col_name)
            df = df.withColumnRenamed(col_name, new_col_name)

    return df


def build_hierarchy(
    df: DataFrame,
    id_col: str,
    parent_col: str,
    include_last_value: bool = True,
    include_hierarchy_string: bool = True,
) -> DataFrame:
    """
    Builds a hierarchical structure from a DataFrame based on parent-child relationships.

    Parameters:
    -----------
    df : DataFrame
        The input DataFrame containing the hierarchical data.
    id_col : str
        The column name representing the unique identifier for each entity (node).
    parent_col : str
        The column name representing the parent entity (node) for each entity.
    include_last_value : bool, optional
        If True, adds a column 'last_value' representing the last non-null level in the hierarchy (default is True).
    include_hierarchy_string : bool, optional
        If True, adds a column 'hierarchy_string' concatenating all hierarchical levels as a string (default is True).

    Returns:
    --------
    DataFrame
        A DataFrame with hierarchical levels, and optionally 'last_value' and 'hierarchy_string' columns.

    Example:
    --------
    result_df = build_hierarchy(df, id_col="_id", parent_col="parentOrgUnit", include_last_value=True, include_hierarchy_string=True)
    """
    # Init spark spession
    spark = get_active_session()

    # Filter out rows where the ID is null
    df_filtered = df.filter(col(id_col).isNotNull())

    hierarchy_iterator = build_hierarchy_from_iterable(
        df_filtered.select(
            col(id_col).cast("string"), col(parent_col).cast("string")
        ).rdd.toLocalIterator()
    )

    all_data = list(hierarchy_iterator)  # Compute all the data
    # Figure out what the schema is.
    all_keys = {}
    for dct in all_data:
        all_keys.update(**dct)
    schema = list(all_keys.keys())

    # Create the final data frame
    result_df = spark.createDataFrame(all_data, schema=schema)
    if not include_last_value:
        # Drop last value
        result_df = result_df.drop("last_value")
    if not include_hierarchy_string:
        # Drop hierarchy string
        result_df.drop("hierarchy_string")
    return result_df.collect()

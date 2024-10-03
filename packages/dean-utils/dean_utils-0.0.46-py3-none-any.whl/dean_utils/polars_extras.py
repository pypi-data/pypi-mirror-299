import polars as pl
from polars.type_aliases import (
    ParallelStrategy,
    ParquetCompression,
    ColumnNameOrSelector,
)
import pyarrow.parquet as pq
import fsspec
import os
from typing import Any, Sequence, cast
from inspect import signature
from pathlib import Path

try:
    from deltalake import DeltaTable, WriterProperties
except ModuleNotFoundError:
    pass
abfs = fsspec.filesystem("abfss", connection_string=os.environ["Synblob"])

key_conv = {"AccountName": "account_name", "AccountKey": "account_key"}
stor = {(splt := x.split("=", 1))[0]: splt[1] for x in os.environ["Synblob"].split(";")}
stor = {key_conv[key]: val for key, val in stor.items() if key in key_conv.keys()}


def pl_scan_pq(
    source: str,
    *,
    n_rows: int | None = None,
    row_index_name: str | None = None,
    row_index_offset: int = 0,
    parallel: ParallelStrategy = "auto",
    use_statistics: bool = True,
    rechunk: bool = True,
    low_memory: bool = False,
    cache: bool = True,
    storage_options=None,
    retries: int = 2,
    include_file_paths: str | None = None,
    **kwargs,
) -> pl.LazyFrame:
    """
    # wrapper for pl.scan_parquet that prepends abfs:// to the path, injects user credentials from Synblob env variable, and sets hive to False

    Parameters
    ----------
    source
        Path(s) to a file
        If a single path is given, it can be a globbing pattern.
    n_rows
        Stop reading from parquet file after reading `n_rows`.
    row_count_name
        If not None, this will insert a row count column with the given name into the
        DataFrame
    row_count_offset
        Offset to start the row_count column (only used if the name is set)
    parallel : {'auto', 'columns', 'row_groups', 'none'}
        This determines the direction of parallelism. 'auto' will try to determine the
        optimal direction.
    use_statistics
        Use statistics in the parquet to determine if pages
        can be skipped from reading.
    rechunk
        In case of reading multiple files via a glob pattern rechunk the final DataFrame
        into contiguous memory chunks.
    low_memory
        Reduce memory pressure at the expense of performance.
    cache
        Cache the result after reading.
    retries
        Number of retries if accessing a cloud instance fails.
    include_file_paths
        Include the path of the source file(s) as a column with this name."""
    if storage_options is None:
        storage_options = stor
    named = dict(
        n_rows=n_rows,
        cache=cache,
        parallel=parallel,
        rechunk=rechunk,
        row_index_name=row_index_name,
        row_index_offset=row_index_offset,
        low_memory=low_memory,
        use_statistics=use_statistics,
        retries=retries,
        storage_options=storage_options,
        hive_partitioning=False,
        include_file_paths=include_file_paths,
    )
    renamed = [
        ("row_index_name", "row_count_name"),
        ("row_index_offset", "row_count_offset"),
    ]
    for rename in renamed:
        for ordered in [-1, 1]:
            if (
                rename[::ordered][0] in signature(pl.scan_parquet).parameters.keys()
                and rename[::ordered][1] in kwargs
            ):
                named[rename[::ordered][0]] = kwargs[rename[::ordered][1]]
    assert isinstance(named, dict)

    return pl.scan_parquet(
        f"abfs://{source}",
        **named,  # type: ignore
    )


def pl_scan_hive(
    source: str,
    *,
    n_rows: int | None = None,
    row_count_name: str | None = None,
    row_count_offset: int = 0,
    parallel: ParallelStrategy = "auto",
    use_statistics: bool = True,
    rechunk: bool = True,
    low_memory: bool = False,
    cache: bool = True,
    storage_options=None,
    retries: int = 2,
    include_file_paths: str | None = None,
    **kwargs,
) -> pl.LazyFrame:
    """
    # wrapper for pl.scan_parquet that prepends abfs:// to the path, injects user credentials from Synblob env variable, and sets hive to False

    Parameters
    ----------
    source
        Path(s) to a file
        If a single path is given, it can be a globbing pattern.
    n_rows
        Stop reading from parquet file after reading `n_rows`.
    row_count_name
        If not None, this will insert a row count column with the given name into the
        DataFrame
    row_count_offset
        Offset to start the row_count column (only used if the name is set)
    parallel : {'auto', 'columns', 'row_groups', 'none'}
        This determines the direction of parallelism. 'auto' will try to determine the
        optimal direction.
    use_statistics
        Use statistics in the parquet to determine if pages
        can be skipped from reading.
    rechunk
        In case of reading multiple files via a glob pattern rechunk the final DataFrame
        into contiguous memory chunks.
    low_memory
        Reduce memory pressure at the expense of performance.
    cache
        Cache the result after reading.
    retries
        Number of retries if accessing a cloud instance fails."""
    if storage_options is None:
        storage_options = stor
    named = dict(
        n_rows=n_rows,
        cache=cache,
        parallel=parallel,
        rechunk=rechunk,
        row_count_name=row_count_name,
        row_count_offset=row_count_offset,
        low_memory=low_memory,
        use_statistics=use_statistics,
        retries=retries,
        storage_options=storage_options,
        hive_partitioning=True,
        include_file_paths=include_file_paths,
    )
    renamed = [
        ("row_index_name", "row_count_name"),
        ("row_index_offset", "row_count_offset"),
    ]
    for rename in renamed:
        for ordered in [-1, 1]:
            if (
                rename[::ordered][0] in signature(pl.scan_parquet).parameters.keys()
                and rename[::ordered][1] in kwargs
            ):
                named[rename[::ordered][0]] = kwargs[rename[::ordered][1]]

    return pl.scan_parquet(
        f"abfs://{source}",
    )


def pl_write_pq(
    self,
    file: str,
    *,
    filesystem=abfs,
    compression: ParquetCompression = "zstd",
    compression_level: int | None = None,
    row_group_part: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
    pyarrow_extra_options: dict[str, Any] | None = None,
) -> None:
    """
    Write to Apache Parquet file with pyarrow writer.
    Defaults to writing to Azure cloud as defined by Synblob env variable.

    Parameters
    ----------
    file
        ABFS File path to which the result will be written.

    compression : {'lz4', 'uncompressed', 'snappy', 'gzip', 'lzo', 'brotli', 'zstd'}
        Choose "zstd" for good compression performance.
        Choose "lz4" for fast compression/decompression.
        Choose "snappy" for more backwards compatibility guarantees
        when you deal with older parquet readers.

    compression_level
        The level of compression to use. Higher compression means smaller files on
        disk.

        - "gzip" : min-level: 0, max-level: 10.
        - "brotli" : min-level: 0, max-level: 11.
        - "zstd" : min-level: 1, max-level: 22.

    row_group_part: use partition_by to create defined row groups

    pyarrow_extra_options:
        Extra options to feed to pyarrow
    """
    if pyarrow_extra_options is None:
        pyarrow_extra_options = {}
    pq_common_params = dict(
        filesystem=filesystem,
        compression=compression,
        compression_level=compression_level,
        **pyarrow_extra_options,
    )

    if row_group_part is None:
        pq.write_table(self.to_arrow(), file, **pq_common_params)
    else:
        writer_params = dict(schema=self.to_arrow().schema, **pq_common_params)
        with pq.ParquetWriter(file, **writer_params) as writer:
            for row_group in self.partition_by(row_group_part):
                writer.write_table(row_group.to_arrow())


def pl_write_delta_append(
    df: pl.DataFrame,
    target: str | Path | DeltaTable,
    *,
    storage_options: dict[str, str] | None = None,
    delta_write_options: dict[str, Any] | None = None,
):
    """
    Appends DataFrame to delta table and auto computes range partition.

        Parameters
        ----------
        target
            URI of a table or a DeltaTable object.
        storage_options
            Extra options for the storage backends supported by `deltalake`.
            For cloud storages, this may include configurations for authentication etc.

            - See a list of supported storage options for S3 `here <https://docs.rs/object_store/latest/object_store/aws/enum.AmazonS3ConfigKey.html#variants>`__.
            - See a list of supported storage options for GCS `here <https://docs.rs/object_store/latest/object_store/gcp/enum.GoogleConfigKey.html#variants>`__.
            - See a list of supported storage options for Azure `here <https://docs.rs/object_store/latest/object_store/azure/enum.AzureConfigKey.html#variants>`__.
        delta_write_options
            Additional keyword arguments while writing a Delta lake Table.
            See a list of supported write options `here <https://delta-io.github.io/delta-rs/api/delta_writer/#deltalake.write_deltalake>`__.
    """
    if isinstance(target, (str, Path)):
        target = DeltaTable(target, storage_options=storage_options)
    add_actions = cast(pl.DataFrame, pl.from_arrow(target.get_add_actions()))
    ### Only allows single column partition range
    partition_by = (
        add_actions.slice(1)
        .select("partition_values")
        .unnest("partition_values")
        .columns[0]
    )
    partition_col = partition_by.replace("_range", "")
    ranges = (
        add_actions.select(
            pl.col("partition_values").struct.field(partition_by),
            pl.col("min")
            .struct.field(partition_col)
            .alias("min_id")
            .cast(df.schema[partition_col]),
            pl.col("max").struct.field(partition_col).alias("max_id"),
        )
        .group_by(partition_by)
        .agg(pl.col("min_id").min(), pl.col("max_id").max())
        .sort("min_id")
    )
    initial_height = df.height
    df = df.sort(partition_col).join_asof(
        ranges, left_on=partition_col, right_on="min_id"
    )
    assert df.height == initial_height
    assert df.filter((pl.col(partition_col) < pl.col("min_id"))).height == 0
    df = df.drop("min_id", "max_id")
    assert isinstance(target, DeltaTable)

    if delta_write_options is None:
        delta_write_options = {
            "writer_properties": WriterProperties(compression="ZSTD"),
            "engine": "rust",
        }
    else:
        if "engine" not in delta_write_options:
            delta_write_options["engine"] = "rust"
        if "writer_properties" in delta_write_options:
            if delta_write_options["writer_properties"].compression is None:
                delta_write_options["writer_properties"].compression = "ZSTD(1)"
        else:
            delta_write_options["writer_properties"] = WriterProperties(
                compression="ZSTD"
            )
    df.write_delta(
        target=target,
        mode="append",
        storage_options=storage_options,
        delta_write_options=delta_write_options,
    )


setattr(pl, "scan_pq", pl_scan_pq)
setattr(pl, "scan_hive", pl_scan_hive)
DF = pl.DataFrame
setattr(DF, "write_pq", pl_write_pq)
setattr(pl, "DataFrame", DF)

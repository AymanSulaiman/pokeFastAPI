import polars as pl
import pandas as pd
import os
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(first_gen_df, *args, **kwargs):
    """
    Exports data to some source

    Args:
        args: The input variables from upstream blocks

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # This can be saved to a data lake like an S3 Bucket
    pl.from_pandas(first_gen_df).write_parquet(os.path.join("..","data", "pokemon_from_mage.parquet"))
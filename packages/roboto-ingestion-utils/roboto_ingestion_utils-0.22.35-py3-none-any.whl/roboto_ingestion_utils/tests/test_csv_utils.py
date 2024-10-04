from pathlib import Path
from mcap.reader import make_reader
import shutil
import pandas as pd
from typing import Union, Dict, Any


from roboto_ingestion_utils.csv import csv_to_mcap, sanitize_filename


def assert_almost_equal(var1: float, var2: float, decimal_places: int = 7) -> None:
    """
    Assert that two floating point numbers are equal up to a certain number of decimal places.

    Args:
        var1: First floating point number.
        var2: Second floating point number.
        decimal_places: Number of decimal places to round to.
    """
    rounded_var1 = round(var1, decimal_places)
    rounded_var2 = round(var2, decimal_places)

    assert rounded_var1 == rounded_var2, f"Assertion failed: {rounded_var1} != {rounded_var2} (rounded to {decimal_places} decimal places)"


def calculate_metrics(csv_file: Union[str, Path]) -> Dict[str, Dict[str, Any]]:
    """
    Read a CSV file and return a dictionary with column metrics.

    Args:
        csv_file: Path to the CSV file.

    Returns:
        A dictionary where keys are column names and values are dictionaries of metrics.
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Initialize the result dictionary
    metrics_dict: Dict[str, Dict[str, Any]] = {}

    # Calculate metrics for each column
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            col_min = df[column].min()
            col_max = df[column].max()
            col_mean = df[column].mean()
            col_median = df[column].median()
            column = column.replace(".", "_")
            metrics_dict[column] = {
                'min': col_min,
                'max': col_max,
                'mean': col_mean,
                'median': col_median
            }
        else:
            # Skip non-numeric columns or handle differently if needed
            metrics_dict[column] = {
                'min': None,
                'max': None,
                'mean': None,
                'median': None
            }

    return metrics_dict


def test_csv_to_mcap():
    """
    minievents.csv is a truncated version of a larger file from a public dataset.
    it has 15 rows of data across message paths of various datatypes.
    the timestamps are keyed to the field "video_offset" and are formatted
    in seconds.
    """
    csv_fname = "minievents.csv"
    output_dir = Path("./test_outputs").resolve()
    output_dir.mkdir(exist_ok=True)
    input_dir = Path("./test_inputs").resolve()
    timestamp_key = "video_offset"
    timestamp_format = "seconds"
    csv_file = input_dir / csv_fname

    topic_info_dict, topic_metrics_dict, _, field_type_mappings = csv_to_mcap(input_dir=input_dir,
                                                                              output_dir=output_dir,
                                                                              rel_file_path=csv_fname,
                                                                              calculate_metrics=True,
                                                                              timestamp_format=timestamp_format,
                                                                              timestamp_key=timestamp_key)

    for key in field_type_mappings.keys():
        output_path = output_dir / f"minievents_{key}.mcap"
        assert output_path.is_file()

    info_dict = topic_info_dict['minievents']
    assert info_dict["nr_msgs"] == 15
    assert info_dict["first_timestamp"] == 0
    assert info_dict["last_timestamp"] == int((1 + 1/6) * 1e9)

    with open(output_path, "rb") as f:
        reader = make_reader(f)
        summary = reader.get_summary()
        stats = summary.statistics
        assert stats.message_count == info_dict["nr_msgs"]
        assert stats.channel_count == 1
        assert stats.message_start_time == info_dict["first_timestamp"]
        assert stats.message_end_time == info_dict["last_timestamp"]

    for path, stats in topic_metrics_dict.items():
        assert set(stats.keys()) == set(["min", "max", "median", "mean"])
    # remove file after tests pass
    shutil.rmtree(output_dir)

    metrics_csv = calculate_metrics(csv_file)

    for key in topic_metrics_dict.keys():
        assert_almost_equal(metrics_csv[key]["max"], topic_metrics_dict[key]["max"])


def test_sanitize_file_name():
    assert sanitize_filename("some_weird_name!)@)$&%$#@(^_&(&~!@[Inc].mcap") == "some_weird_name%21%29%40%29%24%26%25%24%23%40%28%5E_%26%28%26~%21%40%5BInc%5D.mcap"








    

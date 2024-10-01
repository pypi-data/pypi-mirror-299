import pandas as pd

from .qvd_utils import QvdReader


def read(file_name):
    reader = QvdReader(file_name)
    n_records = reader.get_number_of_records()
    df = pd.DataFrame.from_dict(reader.fetch_rows(n_records))
    return df


def read_in_chunks(file_name, chunk_size=None):
    reader = QvdReader(file_name)
    n_records = reader.get_number_of_records()
    if chunk_size is None:
        chunk_size = n_records
    for _ in range(0, n_records, chunk_size):
        yield reader.fetch_rows(chunk_size)


def read_to_dict(file_name):
    reader = QvdReader(file_name)
    n_records = reader.get_number_of_records()
    data = reader.fetch_rows(n_records)
    return data

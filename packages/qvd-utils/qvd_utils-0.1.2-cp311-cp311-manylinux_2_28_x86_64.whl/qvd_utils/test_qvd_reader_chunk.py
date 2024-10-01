import os
import pandas as pd

from qvd_utils import qvd_reader


class TestReadQVDChunk():

    @staticmethod
    def load_qvd_chunks(file_path):
        try:
            data = qvd_reader.read_in_chunks(file_path, chunk_size=1000)
            data = [
                pd.DataFrame.from_dict(chunk) for chunk in data
            ]
            return data
        except Exception as e:
            print(f"Error loading QVD file: {e}")
            return None

    def test_qvd_file_load_in_chunks(self):
        # Replace 'your_qvd_file.qvd' with the path to your QVD file
        qvd_file_path = f'{os.path.dirname(__file__)}/test_files/AAPL.qvd'

        # Try to load the QVD file
        loaded_data = self.load_qvd_chunks(qvd_file_path)

        # Check if the data was successfully loaded
        load_error_msg = f"Failed to load QVD file: {qvd_file_path}"

        assert loaded_data is not None, load_error_msg

        for i, chunk in enumerate(loaded_data):
            assert len(chunk) > 0, "Empty chunk loaded!"
            print(f'Loaded chunk #{i+1} with {len(chunk)} rows')

        csv_file_path = f'{os.path.dirname(__file__)}/test_files/AAPL.csv'
        csv_data = pd.read_csv(csv_file_path)

        size_error_msg = "Loaded data size doesn't match CSV file size"
        chunks_sizes = [chunk.shape[0] for chunk in loaded_data]
        assert sum(chunks_sizes) == csv_data.shape[0], size_error_msg

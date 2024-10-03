from pathlib import Path

from digatron_utility.read import DigatronDataFormat, read_digatron_data_file

# Path to the test data
cwd = Path(__file__)
test_data_path = cwd.parents[1] / "test_data"

form = "fP-5_3_8-Form.csv"
fifty = "fP-5_3_3-50.csv"
hundred = "fP-5_2_4-100.csv"

results = dict()
# key: (file_path, format)
options = {
    "form": (test_data_path / form, DigatronDataFormat.german_client_csv),
    "fifty": (test_data_path / fifty, DigatronDataFormat.german_client_csv),
    "hundred": (test_data_path / hundred, DigatronDataFormat.german_client_csv),
}

for key, value in options.items():
    results[key] = read_digatron_data_file(file_path=value[0], frmt=value[1])

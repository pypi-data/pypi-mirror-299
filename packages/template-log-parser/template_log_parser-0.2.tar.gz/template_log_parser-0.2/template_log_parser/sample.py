import pandas as pd

omada_sample_log = "../template_log_parser/sample_log_files/omada_sample_log.log"
synology_sample_log = (
    "../template_log_parser/sample_log_files/synology_sample_log.log"
)

# Sample df that contains columns suitable for testing of built-in column functions
sample_df = pd.DataFrame(
    {
        "utc_time": ["2024-09-15T11:44:51+01:00", "2024-09-15T12:44:51+01:00"],
        "data": ["45MB", "132.0KB"],
        "time": ["2024-09-15T11:44:51+01:00", "2024-09-15T12:44:51+01:00"],
        "client_name_and_mac": ["name_1:E4-A8-EF-4A-40-DC", "name2:b8-3e-9d-41-0b-6d"],
        "time_elapsed": ["26h5m", "30s"],
        "ip_address_raw": ["192.168.0.1", "(10.0.0.1)"],
    }
)

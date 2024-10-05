from source.log_functions import process_log

from source.debian_templates import debian_template_dict
from source.log_type_classes import BuiltInLogFileType

debian = BuiltInLogFileType(
name="debian",
    sample_log_file=None,
    templates=debian_template_dict,
    column_functions=None,
    merge_events=None,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)

def omv_process_log(file, dict_format=True):
    """
    Return a single Pandas Dataframe or dictionary of dfs whose keys are the log file event types,
        utilizes predefined templates and functions.  This function is tailored to Omada log files.

        Args:
            file (text log file):
                most commonly in the format of some_log_process.log

            dict_format (bool) (True by default):
                If False, function returns a concatenated df of all event types with numerous NaN values.
                Use with caution as this will consume more memory.

        Returns:
              dict or Pandas DataFrame:
                dict formatted as {'event_type_1': df_1, 'event_type_2': df_2, ...}
                Pandas Dataframe will include all event types and all columns

        Notes:
            This function is built on process_log()
    """
    final = process_log(
        file=file, template_dictionary=debian.templates, dict_format=dict_format
    )

    return final


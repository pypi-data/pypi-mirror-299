from simple_template_log_parser.log_type_classes import BuiltInLogFileType

from simple_template_log_parser.log_functions import process_log
from simple_template_log_parser.column_functions import (
    calc_time,
    calc_data_usage,
    split_name_and_mac,
)

from simple_template_log_parser.omada_templates import omada_template_dict
from simple_template_log_parser.sample import omada_sample_log

# Three columns need cleanup, connection time, data usage, and client_name/mac
omada_column_process_dict = {
    "time": [calc_time, "conn_time_min"],
    "data": [calc_data_usage, "data_usage_MB"],
    "client_name_and_mac": [split_name_and_mac, ["client_name", "client_mac"]],
}

# Merging events for consolidation
omada_merge_events_dict = {
    "client_connections": ["conn_hw", "conn_w"],
    "client_disconnections": ["disc_hw", "disc_w", "disc_hw_recon", "disc_w_recon"],
    "logins": ["login", "failed_login"],
    "online": ["online_hw", "online_w"],
}

omada = BuiltInLogFileType(
    name="omada",
    sample_log_file=omada_sample_log,
    templates=omada_template_dict,
    column_functions=omada_column_process_dict,
    merge_events=omada_merge_events_dict,
    datetime_columns=["utc", "local_time"],
    localize_datetime_columns=None,
)


def omada_process_log(file, dict_format=True):
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
    output = process_log(
        file=file,
        template_dictionary=omada.templates,
        additional_column_functions=omada.column_functions,
        merge_dictionary=omada.merge_events,
        datetime_columns=omada.datetime_columns,
        localize_timezone_columns=omada.localize_datetime_columns,
        dict_format=dict_format,
    )

    return output

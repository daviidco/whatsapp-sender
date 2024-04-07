import re

import flet as ft
import pandas as pd

from pages.handle_errors import DfEmptyException, TemplateEmptyOrNoneException


def find_option(selector: ft.Dropdown, option_name: str):
    for option in selector.options:
        if option_name == option.key:
            return option
    return None


def validate_dataframe(df):
    """
    Validates that the DataFrame is not None and is not empty.

    Parameters:
    df (pd.DataFrame): The DataFrame to validate.

    Raises:
    DfEmptyException: If the DataFrame is None or empty.
    """
    if df is None:
        raise DfEmptyException("No file uploaded.")
    if df.empty:
        raise DfEmptyException("File empty.")


def format_message_base(original_message: str, data: pd.Series or pd.DataFrame):
    """
    Base function to format a message by replacing placeholders with values.

    Parameters:
    original_message (str): The original message with placeholders in curly braces.
    data (pd.Series or pd.DataFrame): The data to replace the placeholders.

    Returns:
    str: The formatted message with placeholders replaced by the corresponding values.
    """
    if original_message in [None, ""]:
        raise TemplateEmptyOrNoneException("Template empty.")

    result = original_message
    placeholders = re.findall(r'\{([^}]+)\}', original_message)
    variable_names = [var.strip() for var in placeholders]
    for var_name in variable_names:
        if var_name in data.columns:
            var_value = data.loc[0, var_name]
            result = result.replace('{' + var_name + '}', str(var_value))
        else:
            if var_name in data.index:
                var_value = data[var_name]
                result = result.replace('{' + var_name + '}', str(var_value))
    return result


def format_preview_message(original_message: str, df: pd.DataFrame):
    """
    Formats a message by replacing placeholders with values from the first row of a DataFrame.

    Parameters:
    original_message (str): The original message with placeholders in curly braces.
    df (pd.DataFrame): The DataFrame containing the data to replace the placeholders.

    Returns:
    str: The formatted message with placeholders replaced by the corresponding values.

    Raises:
    DfEmptyException: If the DataFrame is empty or not uploaded.
    """
    validate_dataframe(df)
    return format_message_base(original_message, df)


def format_message(row: pd.Series, original_message: str):
    """
    Formats a message by replacing placeholders with values from a DataFrame row.

    Parameters:
    row (pd.Series): The row from the DataFrame containing the data to replace the placeholders.
    original_message (str): The original message with placeholders in curly braces.

    Returns:
    str: The formatted message with placeholders replaced by the corresponding values.
    """
    return format_message_base(original_message, row)

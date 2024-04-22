import flet as ft
from pandas import DataFrame


def check_selector_template(selector_template: ft.Dropdown) -> bool:
    """
    Checks if a template is selected in the dropdown.

    Args:

        selector_template (ft.Dropdown): The dropdown widget to check.



    Returns:

        bool: True if a template is selected, False otherwise.
    """
    if selector_template.value in [None, ""]:
        selector_template.error_text = "Please select a template"
        selector_template.update()
        return False
    return True


def check_df_uploaded(df: DataFrame, row_table, txf_result) -> bool:
    """
    Checks if a DataFrame is uploaded and not empty.


    Args:

        df (DataFrame): The DataFrame to check.

        row_table:

        txf_result:



    Returns:

        bool: True if DataFrame is uploaded and not empty, False otherwise.

    """
    if df.empty:
        row_table.controls.clear()
        txf_result.value = "The file is empty."
        txf_result.bgcolor = ft.colors.RED
        txf_result.color = ft.colors.WHITE
        row_table.update()
        txf_result.update()
        return False
    return True


def check_upload_file(df: DataFrame, row_table, txf_result) -> bool:
    """

    Checks if a DataFrame is uploaded.



    Args:

        df (DataFrame): The DataFrame to check.

        row_table:

        txf_result:



    Returns:

        bool: True if DataFrame is uploaded, False otherwise.

    """
    if df is None or df.empty:
        row_table.controls.clear()
        txf_result.value = (
            "Please upload the base file." if df is None else "The file is empty."
        )
        txf_result.bgcolor = ft.colors.RED
        txf_result.color = ft.colors.WHITE
        row_table.update()
        txf_result.update()
        return False
    return True

import flet as ft
from pandas import DataFrame


def check_selector_template(selector_template: ft.Dropdown) -> bool:
    if selector_template.value in [None, ""]:
        selector_template.error_text = "Please select a template"
        selector_template.update()
        return False
    return True


def check_df_uploaded(df: DataFrame, row_table, txf_result) -> bool:
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
    if df is None or df.empty:
        row_table.controls.clear()
        txf_result.value = "Please upload the base file." if df is None else "The file is empty."
        txf_result.bgcolor = ft.colors.RED
        txf_result.color = ft.colors.WHITE
        row_table.update()
        txf_result.update()
        return False
    return True

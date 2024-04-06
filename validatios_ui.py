import flet as ft


def check_selector_template(selector_template: ft.Dropdown) -> bool:
    if selector_template.value in [None, ""]:
        selector_template.error_text = "Please select a template"
        selector_template.update()
        return False
    return True

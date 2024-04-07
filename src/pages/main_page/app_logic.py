from typing import Optional

import flet as ft
import pandas as pd
from simpledt import DataFrame

from constants_style import COLOR_GREEN
from pages import utils
from pages.handle_errors import DfEmptyException, TemplateEmptyOrNoneException
from pages.main_page import validatios_ui
from paginated_dt import PaginatedDataTable
from schemas.templates_schema import TemplateInsertSchema, TemplateUpdateSchema, TemplateSchema
from service_whatsapp.handle_errors import NotLoggedInException
from service_whatsapp.main import check_login_whatsapp, send_whatsapp_message


class AppLogicManager:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager

    def handle_dropdown_changed(self):
        """
        Maneja el cambio en el dropdown seleccionado.
        """
        selected_template_name = self.ui_manager.selector_template.value
        self.ui_manager.selected_template = self.find_template_by_name(selected_template_name)
        if self.ui_manager.selected_template:
            self.update_ui_with_selected_template(self.ui_manager.selected_template)
        else:
            print("Template not found")

    def handle_download_sample(self):
        pass

    def handle_pick_file_result(self, e: ft.FilePickerResultEvent):
        """
        Handles the result of the FilePicker, loading the selected file and updating the table.
        """
        if e.files:
            file_path = e.files[0].path
            self.ui_manager.df = pd.read_excel(file_path, dtype={'numero': str})
            if not validatios_ui.check_upload_file(self.ui_manager.df, self.ui_manager.row_table,
                                                   self.ui_manager.txf_result):
                return

            simpledt_df = DataFrame(self.ui_manager.df)
            pdt = PaginatedDataTable(
                datatable=simpledt_df.datatable,
                table_title="Base Uploaded from field",
                rows_per_page=5
            )
            pdt.datatable.border = ft.border.all(2, "green")
            for index, row in enumerate(pdt.datarows):
                if index % 2 == 0:
                    row.color = COLOR_GREEN
                else:
                    row.color = None
            self.ui_manager.row_table.controls.clear()
            self.ui_manager.row_table.controls.append(ft.Column(controls=[pdt]))
            self.ui_manager.txf_result.value = file_path
            self.ui_manager.txf_result.bgcolor = ft.colors.LIGHT_GREEN
            self.ui_manager.txf_result.color = ft.colors.BLACK
            self.ui_manager.update()

    def handle_pick_file(self):
        """
        Opens the FilePicker to select the database base.
        """
        # Add the FilePicker to the page overlay just before opening it
        self.ui_manager.page.overlay.append(self.ui_manager.file_picker)
        self.ui_manager.page.update()
        # Now open the FilePicker
        self.ui_manager.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx"]
        )

    def handle_send_messages(self):
        if validatios_ui.check_selector_template(self.ui_manager.selector_template):
            print("Initializing service send messages...")

            if not validatios_ui.check_upload_file(self.ui_manager.df, self.ui_manager.row_table,
                                                   self.ui_manager.txf_result):
                return

            # Retrieve profiles from the Excel file
            try:
                self.ui_manager.df['formatted_message'] = self.ui_manager.df.apply(
                    lambda row: utils.format_message(row, self.ui_manager.txf_area_msg.value),
                    axis=1)
            except Exception as e:
                self.ui_manager.txf_result.value = f"Error formatting messages: {e}"
                self.ui_manager.txf_result.bgcolor = ft.colors.RED
                self.ui_manager.txf_result.color = ft.colors.WHITE
                self.ui_manager.update()
                return

            try:
                check_login_whatsapp()
                print("Sending messages...")

                # Iterate through each profile and send personalized messages
                for index, recipient in self.ui_manager.df.iterrows():
                    try:
                        print(f"Messages [{self.ui_manager.df.shape[0]}]...")

                        send_whatsapp_message(phone=recipient['numero'],
                                              message=recipient['formatted_message'])

                        print(f"Message {index} sent [Ok]...")

                    except Exception as e:
                        print(f"Error sending message to {recipient['numero']}: {str(e)}")
                print("End Service Sent messages... ")

            except NotLoggedInException as e:
                self.ui_manager.txf_result.value = ("Error trying sent messages. "
                                                    "Please verify you are login in https://web.whatsapp.com")
                self.ui_manager.txf_result.bgcolor = ft.colors.RED
                self.ui_manager.txf_result.color = ft.colors.WHITE
                self.ui_manager.update()

    def handle_save_new_template(self):
        print("new template")
        new_template = TemplateInsertSchema(template_name=self.ui_manager.txf_new_template.value,
                                            content=self.ui_manager.txf_area_msg.value)
        self.ui_manager.template_repository.save_template_db(new_template)

        self.ui_manager.selector_template.options.append(ft.dropdown.Option(self.ui_manager.txf_new_template.value))
        self.ui_manager.selector_template.value = self.ui_manager.txf_new_template.value
        self.ui_manager.update()
        self.ui_manager.templates = self.ui_manager.template_repository.get_templates_db()
        self.handle_dropdown_changed()

    def handle_open_edit_dialog(self):
        if validatios_ui.check_selector_template(self.ui_manager.selector_template):
            self.ui_manager.page.dialog = self.ui_manager.confirm_edit_dialog
            self.ui_manager.confirm_edit_dialog.open = True
            self.ui_manager.page.update()

    def handle_update_template(self):
        print("update template")
        option = utils.find_option(self.ui_manager.selector_template, self.ui_manager.selector_template.value)
        if option is not None:
            old_template = TemplateUpdateSchema(id=self.ui_manager.selected_template.id,
                                                template_name=self.ui_manager.txf_new_template.value,
                                                content=self.ui_manager.txf_area_msg.value)
            self.ui_manager.template_repository.update_template_db(old_template)

            print("updated at db")

            self.ui_manager.selector_template.options.remove(option)
            self.ui_manager.selector_template.options.append(ft.dropdown.Option(self.ui_manager.txf_new_template.value))
            self.ui_manager.selector_template.value = self.ui_manager.txf_new_template.value
            self.ui_manager.update()
            self.ui_manager.templates = self.ui_manager.template_repository.get_templates_db()
            self.handle_dropdown_changed()
            print("updated at app")
        self.handle_close_dialog()

    def handle_open_delete_dialog(self):
        if validatios_ui.check_selector_template(self.ui_manager.selector_template):
            self.ui_manager.page.dialog = self.ui_manager.confirm_delete_dialog
            self.ui_manager.confirm_delete_dialog.open = True
            self.ui_manager.page.update()

    def handle_delete_template(self):
        print("Delete template")
        option = utils.find_option(self.ui_manager.selector_template, self.ui_manager.selector_template.value)
        if option is not None:
            self.ui_manager.template_repository.delete_template_db(self.ui_manager.selected_template.id)
            self.ui_manager.selector_template.options.remove(option)
            self.reset_template_fields([self.ui_manager.txf_area_msg,
                                        self.ui_manager.txf_new_template,
                                        self.ui_manager.selector_template])
            self.ui_manager.update()
        self.handle_close_dialog()

    def handle_open_preview_dialog(self):
        # if not validatios_ui.check_selector_template(self.ui_manager.selector_template):
        #     return
        # if not validatios_ui.check_upload_file(self.ui_manager.df, self.ui_manager.row_table, self.ui_manager.txf_result):
        #     return
        # if not validatios_ui.check_df_uploaded(self.ui_manager.df, self.ui_manager.row_table,
        #                                        self.ui_manager.txf_result):
        #    return
        message_formatted = self.generate_preview_template()
        self.ui_manager.confirm_preview_dialog.content.value = message_formatted
        self.ui_manager.confirm_preview_dialog.open = True
        self.ui_manager.page.dialog = self.ui_manager.confirm_preview_dialog
        self.ui_manager.page.update()

    def handle_close_dialog(self):
        self.ui_manager.page.dialog.open = False
        self.ui_manager.page.update()


    def find_template_by_name(self, template_name) -> Optional[TemplateSchema]:
        """
        Busca una plantilla por su nombre.
        """
        template = next(
            (template for template in self.ui_manager.templates if template[1] == template_name),
            None)
        if template is not None:
            template_result = TemplateSchema(id=template[0], template_name=template[1], content=template[2])
            return template_result
        else:
            return None

    def update_ui_with_selected_template(self, template: TemplateSchema):
        """
        Actualiza la interfaz de usuario con la plantilla seleccionada.
        """
        text_template = template.content
        self.ui_manager.txf_area_msg.value = f"{text_template}"
        self.ui_manager.selector_template.error_text = None
        self.ui_manager.txf_new_template.value = template.template_name
        self.ui_manager.update()

    def generate_preview_template(self):
        try:
            message_formatted = utils.format_preview_message(self.ui_manager.txf_area_msg.value, self.ui_manager.df)
            return message_formatted
        except (DfEmptyException, TemplateEmptyOrNoneException) as e:
            self.ui_manager.txf_result.value = "The file is empty."
            self.ui_manager.txf_result.bgcolor = ft.colors.RED
            self.ui_manager.txf_result.color = ft.colors.WHITE
            self.ui_manager.update()

    def reset_template_fields(self, controls):
        """
        Resets the value of specified template fields to None.

        Parameters:
        fields_to_reset (list): A list of controls ft to reset.
        """
        for control in controls:
            control.value = None

    def get_templates(self):
        return self.ui_manager.template_repository.get_templates_db()

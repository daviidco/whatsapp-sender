from typing import Optional

import flet as ft
import pandas as pd
from simpledt import DataFrame

from constants_style import COLOR_GREEN
from pages import utils
from pages.handle_errors import DfEmptyException, TemplateEmptyOrNoneException
from pages.main_page import validations_ui
from paginated_dt import PaginatedDataTable
from schemas.templates_schema import TemplateInsertSchema, TemplateUpdateSchema, TemplateSchema
from service_whatsapp.handle_errors import NotLoggedInException
from service_whatsapp.main import check_login_whatsapp, send_whatsapp_message


class AppLogicManager:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager

    def handle_dropdown_changed(self):
        """
        Handles the change in the selected dropdown.
        """
        selected_template_name = self.ui_manager.selector_template.value
        self.ui_manager.selected_template = self.find_template_by_name(selected_template_name)
        if self.ui_manager.selected_template:
            self.update_ui_with_selected_template(self.ui_manager.selected_template)
        else:
            print("Template not found")

    def handle_download_sample(self):
        """
        Placeholder function for handling downloading samples.
        """
        pass

    def handle_pick_file_result(self, e: ft.FilePickerResultEvent):
        """
        Handles the result of the FilePicker, loads the selected file, and updates the table.



        Args:

            e (ft.FilePickerResultEvent): The event object containing information about the selected file.

        """
        if e.files:
            file_path = e.files[0].path
            self.ui_manager.df = pd.read_excel(file_path, dtype={'numero': str})
            if not validations_ui.check_upload_file(self.ui_manager.df, self.ui_manager.row_table,
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
        """
        Handles sending messages to selected recipients.
        """
        if not validations_ui.check_selector_template(self.ui_manager.selector_template):
            return

        if not validations_ui.check_upload_file(self.ui_manager.df, self.ui_manager.row_table,
                                                self.ui_manager.txf_result):
            return

        print("Initializing service send messages...")

        try:
            self.ui_manager.df['formatted_message'] = self.ui_manager.df.apply(
                lambda row: utils.format_message(row, self.ui_manager.txf_area_msg.value),
                axis=1)
        except Exception as e:
            error_message = f"Error formatting messages: {e}"
            self.ui_manager.txf_result.value = error_message
            self.ui_manager.txf_result.bgcolor = ft.colors.RED
            self.ui_manager.txf_result.color = ft.colors.WHITE
            self.ui_manager.update()
            return

        try:
            check_login_whatsapp()
            print("Sending messages...")
            messages_sent = 0

            for index, recipient in self.ui_manager.df.iterrows():
                try:
                    print(f"Messages [{self.ui_manager.df.shape[0]}]...")
                    send_whatsapp_message(phone=recipient['numero'],
                                          message=recipient['formatted_message'])
                    messages_sent += 1
                    print(f"Message {index} sent [Ok]...")
                except Exception as e:
                    print(f"Error sending message to {recipient['numero']}: {str(e)}")
                    self.ui_manager.txf_result_op.value = f"Error with message to {recipient['numero']}."
                    self.ui_manager.txf_result_op.bgcolor = ft.colors.RED
                    self.ui_manager.txf_result_op.color = ft.colors.WHITE
                    self.ui_manager.update()
                    return

            self.ui_manager.txf_result_op.value = f"Messages sent successfully. [{messages_sent}]"
            self.ui_manager.txf_result_op.bgcolor = ft.colors.LIGHT_GREEN
            self.ui_manager.txf_result_op.color = ft.colors.WHITE
            self.ui_manager.update()
            print("End Service Sent messages... ")


        except NotLoggedInException as e:
            error_message = "Error trying sent messages. Please verify you are logged in at https://web.whatsapp.com"
            self.ui_manager.txf_result.value = error_message
            self.ui_manager.txf_result.bgcolor = ft.colors.RED
            self.ui_manager.txf_result.color = ft.colors.WHITE
            self.ui_manager.update()

    def handle_save_new_template(self):
        """
        Handles saving a new message template.
        """
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
        """
        Handles opening the edit dialog for the selected template.
        """
        if validations_ui.check_selector_template(self.ui_manager.selector_template):
            self.ui_manager.page.dialog = self.ui_manager.confirm_edit_dialog
            self.ui_manager.confirm_edit_dialog.open = True
            self.ui_manager.page.update()

    def handle_update_template(self):
        """
        Handles updating an existing message template.
        """
        print("Update template")
        option = utils.find_option(self.ui_manager.selector_template, self.ui_manager.selector_template.value)
        if option is not None:
            old_template = TemplateUpdateSchema(id=self.ui_manager.selected_template.id,
                                                template_name=self.ui_manager.txf_new_template.value,
                                                content=self.ui_manager.txf_area_msg.value)
            self.ui_manager.template_repository.update_template_db(old_template)

            print("Template updated at db")

            self.ui_manager.selector_template.options.remove(option)
            self.ui_manager.selector_template.options.append(ft.dropdown.Option(self.ui_manager.txf_new_template.value))
            self.ui_manager.selector_template.value = self.ui_manager.txf_new_template.value
            self.ui_manager.update()
            self.ui_manager.templates = self.ui_manager.template_repository.get_templates_db()
            self.handle_dropdown_changed()
        self.handle_close_dialog()

    def handle_open_delete_dialog(self):
        """
        Handles opening the delete dialog for the selected template.
        """
        if validations_ui.check_selector_template(self.ui_manager.selector_template):
            self.ui_manager.page.dialog = self.ui_manager.confirm_delete_dialog
            self.ui_manager.confirm_delete_dialog.open = True
            self.ui_manager.page.update()

    def handle_delete_template(self):
        """
        Handles deleting an existing message template.
        """
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
        """
        Handles opening the preview dialog for the selected template.
        """
        if not validations_ui.check_selector_template(self.ui_manager.selector_template):
            return
        if not validations_ui.check_upload_file(self.ui_manager.df, self.ui_manager.row_table,
                                                self.ui_manager.txf_result):
            return
        if not validations_ui.check_df_uploaded(self.ui_manager.df, self.ui_manager.row_table,
                                                self.ui_manager.txf_result):
            return
        message_formatted = self.generate_preview_template()
        self.ui_manager.confirm_preview_dialog.content.value = message_formatted
        self.ui_manager.confirm_preview_dialog.open = True
        self.ui_manager.page.dialog = self.ui_manager.confirm_preview_dialog
        self.ui_manager.page.update()

    def handle_close_dialog(self):
        """
        Handles closing the currently opened dialog.
        """
        self.ui_manager.page.dialog.open = False
        self.ui_manager.page.update()

    def find_template_by_name(self, template_name) -> Optional[TemplateSchema]:
        """
        Finds a template by its name.


        Args:

            template_name (str): The name of the template to search for.



        Returns:

            Optional[TemplateSchema]: The TemplateSchema object if found, else None.

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
        Updates the user interface with the selected template.

        Args:

            template (TemplateSchema): The TemplateSchema object representing the selected template.
        """
        text_template = template.content
        self.ui_manager.txf_area_msg.value = f"{text_template}"
        self.ui_manager.selector_template.error_text = None
        self.ui_manager.txf_new_template.value = template.template_name
        self.ui_manager.update()

    def generate_preview_template(self):
        """
        Generates a preview of the message based on the template and the uploaded DataFrame.

        Returns:
            str: The formatted preview message.
        """
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

        Args:

            controls (list): A list of controls to reset.

        """
        for control in controls:
            control.value = None

    def get_templates(self):
        """
        Retrieves all templates from the template repository.

        Returns:
            list: A list of TemplateSchema objects representing the templates.
        """
        return self.ui_manager.template_repository.get_templates_db()

import time

import flet as ft
import numpy as np
import pandas as pd
from simpledt import DataFrame

from database import get_templates_db, delete_template_db, save_template_db, update_template_db
from paginated_dt import PaginatedDataTable
from service_whatsapp.main import send_whatsapp_message, NotLoggedInException, check_login_whatsapp
from templates_schema import TemplateInsert, TemplateUpdate
from utils import format_preview_message, DfEmptyException, TemplateEmptyOrNoneException, format_message
from validatios_ui import check_selector_template

COLOR_GREEN = "#005B4A"
WIDTH_3_COL = 380


class WhatsSenderApp(ft.UserControl):
    """
    Main application class that handles the user interface and application logic.
    """

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.templates = None
        self.txf_area_msg, self.txf_new_template, self.txf_result = self.create_text_fields()
        (self.btn_sent, self.btn_schedule_sent, self.btn_new_template, 
         self.btn_edit_template, self.btn_del_template, self.btn_prev_template) = self.create_icon_buttons()
        self.row_table = ft.Row(scroll=ft.ScrollMode.ALWAYS)
        self.selector_template = self.create_dropdown()
        self.file_picker = ft.FilePicker(on_result=self.pick_file_result)
        self.df = None
        # Buttons
        self.btn_download_sample = ft.ElevatedButton(text="Download Sample",
                                                     icon="DOWNLOAD_FOR_OFFLINE",
                                                     on_click=self.download_sample)
        self.btn_select_base = ft.ElevatedButton(
            text="Choose the base to sent",
            icon=ft.icons.UPLOAD_FILE,
            on_click=self.select_base
        )

    def create_text_fields(self):
        """
        Creates the text fields for the application.
        """
        txf_area_msg = ft.TextField(
            width=WIDTH_3_COL,
            height=400,
            multiline=True,
            min_lines=10000,
            max_lines=10000,
            bgcolor="#005B4A",
            border_radius=20
        )

        txf_new_template = ft.TextField(
            label="Name Template",
            width=WIDTH_3_COL
        )

        txf_result = ft.TextField(
            read_only=True,
        )
        return txf_area_msg, txf_new_template, txf_result

    def create_icon_buttons(self):
        """
        Creates the icon buttons for the application.
        """
        btn_send = ft.CircleAvatar(
            content=ft.IconButton(
                icon=ft.icons.SEND,
                icon_color=ft.colors.BLACK,
                icon_size=35,
                tooltip="Sent messages",
                on_click=self.send_messages
            ),
            bgcolor=ft.colors.GREEN,
            radius=25
        )

        btn_schedule_sent = ft.CircleAvatar(
            content=ft.IconButton(
                icon=ft.icons.SCHEDULE_SEND,
                icon_color=ft.colors.BLACK,
                icon_size=35,
                tooltip="Schedule sent messages",
                on_click=self.send_messages
            ),
            bgcolor=ft.colors.GREEN_ACCENT_100,
            radius=25
        )

        btn_new_template = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE_SHARP,
            icon_color=ft.colors.YELLOW,
            tooltip="Save new template",
            on_click=self.save_new_template,
            # disabled=True
        )

        btn_edit_template = ft.IconButton(
            icon=ft.icons.SAVE,
            icon_color="GREEN",
            tooltip="Update template",
            on_click=self.open_edit_dialog,
            # disabled=True
        )

        btn_del_template = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color=ft.colors.RED,
            tooltip="Delete current template",
            on_click=self.open_delete_dialog,
            # disabled=True
            opacity=40
        )

        btn_prev_template = ft.IconButton(
            icon=ft.icons.REMOVE_RED_EYE_ROUNDED,
            icon_color=ft.colors.AMBER_100,
            tooltip="Preview template with the first row from base",
            on_click=self.open_preview_dialog,  # self.preview_template,
            # disabled=True
        )
        return btn_send, btn_schedule_sent, btn_new_template, btn_edit_template, btn_del_template, btn_prev_template

    def create_dropdown(self):
        """
        Creates the dropdown for selecting templates.
        """
        self.templates = get_templates_db(self.conn)
        template_names = [template[1] for template in self.templates]
        return ft.Dropdown(
            on_change=self.dropdown_changed,
            label="Select template",
            width=WIDTH_3_COL,
            options=[ft.dropdown.Option(name) for name in template_names],

        )

    def dropdown_changed(self, e):
        """
        Handles the dropdown change event.
        """
        selected_template_name = self.selector_template.value
        self.selected_template = next(
            (template for template in self.templates if template[1] == selected_template_name),
            None)

        if self.selected_template:
            text_template = self.selected_template[2]
            self.txf_area_msg.value = f"{text_template}"
            self.selector_template.error_text = ""

            self.txf_new_template.value = selected_template_name

        else:
            print("Template not found")

        self.update()

    def download_sample(self, e):
        """
        Implements the logic for downloading the sample.
        """
        pass

    def pick_file_result(self, e: ft.FilePickerResultEvent):
        """
        Handles the result of the FilePicker, loading the selected file and updating the table.
        """
        if e.files:
            file_path = e.files[0].path
            try:
                self.df = pd.read_excel(file_path, dtype={'numero': str})
                if self.df.empty:
                    raise pd.errors.EmptyDataError("The file is empty.")
                simpledt_df = DataFrame(self.df)
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
                self.row_table.controls.clear()
                self.row_table.controls.append(ft.Column(controls=[pdt]))
                self.txf_result.value = file_path
                self.txf_result.bgcolor = ft.colors.LIGHT_GREEN
                self.txf_result.color = ft.colors.BLACK
                self.update()
            except pd.errors.EmptyDataError:
                self.row_table.controls.clear()
                self.txf_result.value = "The file is empty."
                self.txf_result.bgcolor = ft.colors.RED
                self.txf_result.color = ft.colors.WHITE
                self.update()

    def select_base(self, e):
        """
        Opens the FilePicker to select the database base.
        """
        # Add the FilePicker to the page overlay just before opening it
        self.page.overlay.append(self.file_picker)
        self.page.update()
        # Now open the FilePicker
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx"]
        )

    def send_messages(self, e):
        if check_selector_template(self.selector_template):
            print("Initializing service send messages...")

            if self.df is None:
                self.row_table.controls.clear()
                self.txf_result.value = "Please upload the base file."
                self.txf_result.bgcolor = ft.colors.RED
                self.txf_result.color = ft.colors.WHITE
                self.update()
                return

            # Retrieve profiles from the Excel file
            try:
                self.df['formatted_message'] = self.df.apply(lambda row: format_message(row, self.txf_area_msg.value),
                                                             axis=1)
            except Exception as e:
                self.txf_result.value = f"Error formatting messages: {e}"
                self.txf_result.bgcolor = ft.colors.RED
                self.txf_result.color = ft.colors.WHITE
                self.update()
                return


            try:
                check_login_whatsapp()
                print("Sending messages...")

                # Iterate through each profile and send personalized messages
                for index, recipient in self.df.iterrows():
                    try:
                        print(f"Messages [{self.df.shape[0]}]...")

                        send_whatsapp_message(phone=recipient['numero'],
                                              message=recipient['formatted_message'])

                        print(f"Message {index} sent [Ok]...")

                    except Exception as e:
                        print(f"Error sending message to {recipient['numero']}: {str(e)}")
                print("End Service Sent messages... ")

            except NotLoggedInException as e:
                self.txf_result.value = ("Error trying sent messages. "
                                         "Please verify you are login in https://web.whatsapp.com")
                self.txf_result.bgcolor = ft.colors.RED
                self.txf_result.color = ft.colors.WHITE
                self.update()

    def save_new_template(self, e):
        print("new template")
        new_template = TemplateInsert(template_name=self.txf_new_template.value,
                                      content=self.txf_area_msg.value)
        save_template_db(self.conn, new_template)

        self.selector_template.options.append(ft.dropdown.Option(self.txf_new_template.value))
        self.selector_template.value = self.txf_new_template.value
        self.update()
        self.templates = get_templates_db(self.conn)
        self.dropdown_changed(e)

    def open_edit_dialog(self, e):

        if check_selector_template(self.selector_template):
            
            confirm_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Do you really want to edit this template?"),
                actions=[
                    ft.TextButton("Yes", on_click=self.update_template),
                    ft.TextButton("No", on_click=self.close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=self.close_dialog,
            )
            self.page.dialog = confirm_dialog
            confirm_dialog.open = True
            self.page.update()

    def update_template(self, e):
        print("update template")
        option = self.find_option(self.selector_template.value)
        if option is not None:
            old_template = TemplateUpdate(id=self.selected_template[0],
                                          template_name=self.txf_new_template.value,
                                          content=self.txf_area_msg.value)
            update_template_db(self.conn, old_template)

            print("updated at db")

            self.selector_template.options.remove(option)
            self.selector_template.options.append(ft.dropdown.Option(self.txf_new_template.value))
            self.selector_template.value = self.txf_new_template.value
            self.update()
            self.templates = get_templates_db(self.conn)
            self.dropdown_changed(e)
            print("updated at app")
        self.close_dialog(e)

    def find_option(self, option_name):
        for option in self.selector_template.options:
            if option_name == option.key:
                return option
        return None

    def open_delete_dialog(self, e):

        if check_selector_template(self.selector_template):
            
            confirm_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Do you really want to delete this template?"),
                actions=[
                    ft.TextButton("Yes", on_click=self.delete_template),
                    ft.TextButton("No", on_click=self.close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=self.close_dialog,
            )
            
            self.page.dialog = confirm_dialog
            confirm_dialog.open = True
            self.page.update()

    def delete_template(self, e):
        print("Delete template")
        option = self.find_option(self.selector_template.value)
        if option != None:
            delete_template_db(self.conn, self.selected_template[0])
            self.selector_template.options.remove(option)
            self.txf_area_msg.value = None
            self.txf_new_template.value = None
            self.selector_template.value = None
            self.update()
        self.close_dialog(e)

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

    def open_preview_dialog(self, e):

        if check_selector_template(self.selector_template):
            message_formatted = self.preview_template

            confirm_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text(
                    width=WIDTH_3_COL,
                    height=400,
                    color=ft.colors.WHITE,
                    value=message_formatted
                ),
                actions=[
                    ft.TextButton("Close", on_click=self.close_dialog),
                ],
                bgcolor="#005B4A",
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=self.close_dialog,

            )
            
            self.page.dialog = confirm_dialog
            confirm_dialog.open = True
            self.page.update()

    @property
    def preview_template(self):
        try:
            message_formatted = format_preview_message(self.txf_area_msg.value, self.df)
            return message_formatted
        except (DfEmptyException, TemplateEmptyOrNoneException) as e:
            self.txf_result.value = "The file is empty."
            self.txf_result.bgcolor = ft.colors.RED
            self.txf_result.color = ft.colors.WHITE
            self.update()

    def build(self):
        """
        Builds the user interface of the application.
        """
        return ft.Container(
            width=1410,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    # ft.Row(controls=[ft.TextField(
                    #     value="Instructions: \n"
                    #           "1. Login at https://web.whatsapp.com/ \n"
                    #           "2. Upload your base xlsx with the correct format \n"
                    #           "3. Clic at sent messages ▶",
                    #     width=800,
                    #     multiline=True,
                    #     max_lines=20,
                    #
                    # )]),
                    ft.Row(
                        controls=[
                            self.btn_download_sample,
                            self.btn_select_base,
                            # self.btn_sent,
                            # self.btn_schedule_sent,
                            ft.Container(content=self.selector_template),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(controls=[self.txf_result,
                                                ft.ListView(controls=[self.row_table])], expand=1),

                            ft.Column(
                                controls=[
                                    ft.Row(controls=[ft.Container(content=self.txf_area_msg), ]),
                                    # , margin=ft.margin.only(left=60)),
                                    ft.Row(controls=[self.txf_new_template, ]),
                                    ft.Row(controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    self.btn_edit_template,
                                                    self.btn_del_template,
                                                    self.btn_prev_template,
                                                    self.btn_new_template,
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                            ), width=WIDTH_3_COL, )],

                                    )
                                ]
                            )
                        ],
                        height=500,  # Set a fixed height for the row

                    ),
                    ft.Row(controls=[
                        self.btn_schedule_sent,
                        self.btn_sent,
                    ],
                        alignment=ft.MainAxisAlignment.CENTER)

                ],
            ),
        )

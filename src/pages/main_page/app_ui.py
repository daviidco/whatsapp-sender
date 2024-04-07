import flet as ft

from constants_style import WIDTH_3_COL
from database.repositories.template_reporitory import TemplateRepository
from pages.main_page.app_logic import AppLogicManager


class UIComponentManager(ft.UserControl):
    """
    Main application class that handles the user interface and application logic.
    """

    def __init__(self, template_repository: TemplateRepository):
        """
        Initialize the UIComponentManager with a database connection.

        Args:
            conn: Database connection object.
        """
        super().__init__()
        self.template_repository = template_repository

        self.app_logic_manager = AppLogicManager(self)

        self.create_text_fields()
        self.create_icon_buttons()
        self.create_dropdown()
        self.row_table = ft.Row(scroll=ft.ScrollMode.ALWAYS)
        self.create_buttons()
        self.create_dialogs()
        self.file_picker = ft.FilePicker(on_result=self.pick_file_result)

        self.df = None

    def create_text_fields(self):
        """
        Creates the text fields for the application.
        """
        self.txf_area_msg = ft.TextField(
            width=WIDTH_3_COL,
            height=400,
            multiline=True,
            min_lines=10000,
            max_lines=10000,
            bgcolor="#005B4A",
            border_radius=20
        )

        self.txf_new_template = ft.TextField(
            label="Name Template",
            width=WIDTH_3_COL
        )

        self.txf_result = ft.TextField(
            read_only=True,
        )

    def create_icon_buttons(self):
        """
        Creates the icon buttons for the application.
        """
        self.btn_send = ft.CircleAvatar(
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

        self.btn_schedule_sent = ft.CircleAvatar(
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

        self.btn_new_template = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE_SHARP,
            icon_color=ft.colors.YELLOW,
            tooltip="Save new template",
            on_click=self.save_new_template,
            # disabled=True
        )

        self.btn_edit_template = ft.IconButton(
            icon=ft.icons.SAVE,
            icon_color="GREEN",
            tooltip="Update template",
            on_click=self.open_edit_dialog,
            # disabled=True
        )

        self.btn_del_template = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color=ft.colors.RED,
            tooltip="Delete current template",
            on_click=self.open_delete_dialog,
            opacity=40
        )

        self.btn_prev_template = ft.IconButton(
            icon=ft.icons.REMOVE_RED_EYE_ROUNDED,
            icon_color=ft.colors.AMBER_100,
            tooltip="Preview template with the first row from base",
            on_click=self.open_preview_dialog
        )

    def create_dropdown(self):
        """
        Creates the dropdown for selecting templates.
        """
        self.templates = self.app_logic_manager.get_templates()
        template_names = [template[1] for template in self.templates]
        self.selector_template = ft.Dropdown(
            on_change=self.dropdown_changed,
            label="Select template",
            width=WIDTH_3_COL,
            options=[ft.dropdown.Option(name) for name in template_names],
        )

    def create_buttons(self):
        """
        Creates the buttons for the application.
        """
        self.btn_download_sample = ft.ElevatedButton(text="Download Sample",
                                                     icon="DOWNLOAD_FOR_OFFLINE",
                                                     on_click=self.download_sample)
        self.btn_select_base = ft.ElevatedButton(
            text="Choose the base to send",
            icon=ft.icons.UPLOAD_FILE,
            on_click=self.pick_file
        )

    def create_dialogs(self):
        self.confirm_edit_dialog = ft.AlertDialog(
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

        self.confirm_delete_dialog = ft.AlertDialog(
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

        self.confirm_preview_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Preview message"),
            content=ft.Text(
                width=WIDTH_3_COL,
                height=400,
                color=ft.colors.WHITE,
            ),
            actions=[
                ft.TextButton("Close", on_click=self.close_dialog),
            ],
            bgcolor="#005B4A",
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self.close_dialog,

        )

    # UI Methods
    def dropdown_changed(self, e):
        """
        Handles the event of changing the dropdown selection.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_dropdown_changed()

    def download_sample(self, e):
        """
        Implements the logic for downloading the sample.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_download_sample()

    def pick_file_result(self, e):
        """
        Handles the result of the FilePicker, loading the selected file and updating the table.

        Args:
            e: FilePickerResultEvent object.
        """
        self.app_logic_manager.handle_pick_file_result(e)

    def pick_file(self, e):
        """
        Opens the FilePicker to select the database base.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_pick_file()

    def send_messages(self, e):
        """
        Handles the event of sending messages.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_send_messages()

    def save_new_template(self, e):
        """
        Handles the event of saving a new template.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_save_new_template()

    def open_edit_dialog(self, e):
        """
        Handles the event of opening the edit dialog.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_open_edit_dialog()

    def update_template(self, e):
        """
        Handles the event of updating a template.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_update_template()

    # def find_option(self, option_name):
    #     """
    #     Handles the event of finding an option.
    #
    #     Args:
    #         option_name: Name of the option to find.
    #     """
    #     self.app_logic_manager.handle_find_option(option_name)

    def open_delete_dialog(self, e):
        """
        Handles the event of opening the delete dialog.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_open_delete_dialog()

    def delete_template(self, e):
        """
        Handles the event of deleting a template.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_delete_template()

    def open_preview_dialog(self, e):
        """
        Handles the event of opening the preview dialog.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_open_preview_dialog()

    def close_dialog(self, e):
        self.app_logic_manager.handle_close_dialog()

    def build(self):
        """
        Builds the user interface of the application.

        Returns:
            A Container object representing the application's UI.
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
                        self.btn_send,
                    ],
                        alignment=ft.MainAxisAlignment.CENTER)

                ],
            ),
        )

import flet as ft

from pages.constants_style import WIDTH_3_COL
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
            template_repository (TemplateRepository): The template repository object.
        """
        super().__init__()
        self.template_repository = template_repository

        # Initialize the app logic manager
        self.app_logic_manager = AppLogicManager(self)

        # Create the text fields for the application
        self.create_text_fields()

        # Create the icon buttons for the application
        self.create_icon_buttons()

        # Create the dropdown for selecting templates
        self.create_dropdown()

        # Create the row table with scrolling mode set to ALWAYS
        self.row_table = ft.Row(scroll=ft.ScrollMode.ALWAYS)

        # Create the buttons for the application
        self.create_buttons()

        # Create the dialogs for the application
        self.create_dialogs()

        # Initialize the file picker with the pick file result event handler
        self.file_picker = ft.FilePicker(on_result=self.pick_file_result)
        self.saveme = ft.FilePicker(on_result=self.download_sample)

        # Set the dataframe to None
        self.df = None

    def create_text_fields(self) -> None:
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

        self.txf_result_op = ft.TextField(
            read_only=True,
            width=WIDTH_3_COL,
        )

    def create_icon_buttons(self) -> None:
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

    def create_dropdown(self) -> None:
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

    def create_buttons(self) -> None:
        """
        Creates the buttons for the application.
        """
        self.btn_download_sample = ft.ElevatedButton(text="Download Sample",
                                                     icon="DOWNLOAD_FOR_OFFLINE",
                                                     on_click=lambda _: self.saveme.save_file(file_name="sample.xlsx"))
        self.btn_select_base = ft.ElevatedButton(
            text="Choose the base to send",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["xlsx"])
        )

    def create_dialogs(self) -> None:
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

    def download_sample(self, e: ft.FilePickerResultEvent):
        """
        Implements the logic for downloading the sample.

        Args:
            e: Event object.
        """
        self.app_logic_manager.handle_download_sample(e)

    def pick_file_result(self, e):
        """
        Handles the result of the FilePicker by loading the selected file and updating the table.

        Args:
            e: FilePickerResultEvent object representing the selected file.
        """
        # Delegates the handling of the picked file result to the AppLogicManager
        self.app_logic_manager.handle_pick_file_result(e)

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

    def did_mount(self):
        self.page.overlay.append(self.file_picker)
        self.page.overlay.append(self.saveme)
        self.page.update()

    def build(self):
        """
        Builds the user interface of the application.

        Returns:
            A Container object representing the application's UI.
        """
        # Create a Container with specified properties
        return ft.Container(
            width=1410,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    # Row 1 with download button, base selection button, and template selector
                    ft.Row(
                        controls=[
                            self.btn_download_sample,
                            self.btn_select_base,
                            ft.Container(content=self.selector_template),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    # Row 2 with result text field and table view
                    ft.Row(
                        controls=[
                            ft.Column(controls=[self.txf_result,
                                                ft.ListView(controls=[self.row_table])], expand=1),

                            # Column with message field, new template field, and template control buttons
                            ft.Column(
                                controls=[
                                    ft.Row(controls=[ft.Container(content=self.txf_area_msg), ]),
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
                    # Row 3 with scheduled send button and send button
                    ft.Row(controls=[
                        ft.Row(controls=[
                                # Todo Next version with schedule button
                                #self.btn_schedule_sent,
                                self.btn_send],
                            expand=1,
                            alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(
                                content=ft.Row(controls=[
                                    self.txf_result_op],
                                alignment=ft.MainAxisAlignment.END,
                            )
                        )
                    ],
                    )
                ],
            ),
        )

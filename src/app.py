import flet as ft

from database.conection import Database
from database.repositories.template_reporitory import TemplateRepository
from database.scripts_sql import sql_create_templates_table, sql_create_sent_messages_table, \
    sql_create_scheduled_messages_table
from pages.main_page.app_ui import UIComponentManager


def main(page: ft.Page):
    """
    Main function that initializes and runs the application.

    Args:
        page (ft.Page): The page object to display the UI.
    """
    # Initialize the database
    database = 'whatsapp-sender.db'
    db = Database(database)
    template_repository = TemplateRepository(db)

    # Create necessary tables if the database connection is established
    if db.connection is not None:
        db.create_table(sql_create_templates_table)
        db.create_table(sql_create_sent_messages_table)
        db.create_table(sql_create_scheduled_messages_table)

        # Insert templates if they don't exist in the database
        if not template_repository.check_if_templates_exist():
            template_repository.insert_templates()
    else:
        print("Error! Cannot create the database connection.")

    # Set the page title
    page.title = "Whatsapp Sender"

    # Initialize the UI component manager and add it to the page
    app = UIComponentManager(template_repository)
    page.add(app)

    # Update the page to display the changes
    page.update()


ft.app(target=main)

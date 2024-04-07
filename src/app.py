import flet as ft

from database.conection import Database
from database.repositories.template_reporitory import TemplateRepository
from database.scripts_sql import sql_create_templates_table, sql_create_sent_messages_table, \
    sql_create_scheduled_messages_table
from pages.main_page.app_ui import UIComponentManager


def main(page: ft.Page):
    """
    Main function that initializes and runs the application.
    """
    database = 'whatsapp-sender.db'

    db = Database(database)
    template_repository = TemplateRepository(db)

    # create tables
    if db.connection is not None:
        # create templates table
        db.create_table(sql_create_templates_table)
        db.create_table(sql_create_sent_messages_table)
        db.create_table(sql_create_scheduled_messages_table)

        if not template_repository.check_if_templates_exist():
            template_repository.insert_templates()
    else:
        print("Error! cannot create the database connection.")

    page.title = "Whatsapp Sender"

    app = UIComponentManager(template_repository)

    page.add(app)
    page.update()


ft.app(target=main)

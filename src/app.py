import flet as ft

from controlsFlet import WhatsSenderApp
from database import create_connection, create_table, insert_templates, check_if_templates_exist
from scripts_sql import sql_create_templates_table, sql_query_count_templates, \
    sql_create_sent_messages_table, sql_create_scheduled_messages_table
from seed_templates import templates


def main(page: ft.Page):
    """
    Main function that initializes and runs the application.
    """
    database = 'whatsapp-sender.db'

    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create templates table
        create_table(conn, sql_create_templates_table)
        create_table(conn, sql_create_sent_messages_table)
        create_table(conn, sql_create_scheduled_messages_table)

        if not check_if_templates_exist(conn, sql_query_count_templates):
            insert_templates(conn, templates)
    else:
        print("Error! cannot create the database connection.")

    page.title = "Whatsapp Sender"
    app = WhatsSenderApp(conn)
    page.add(app)
    page.update()


ft.app(target=main)

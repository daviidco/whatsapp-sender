import sqlite3
from sqlite3 import Error

from scripts_sql import sql_query_all_templates


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def check_if_templates_exist(conn, create_table_sql) -> bool:
    try:
        c = conn.cursor()
        c.execute("SELECT count(*) FROM templates")
        count = c.fetchone()[0]
        return count > 0
    except Error as e:
        print(e)


def insert_templates(conn, templates):
    try:
        cursor = conn.cursor()
        for template in templates:
            cursor.execute("INSERT INTO templates (template_name, content) VALUES (?, ?)", template)
        conn.commit()
    except Error as e:
        print(e)


def get_templates_db(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query_all_templates)
        templates = cursor.fetchall()
        return templates
    except Error as e:
        print(e)


def save_template_db(conn, template):
    try:
        cursor = conn.cursor()
        template_tuple = (template.template_name, template.content)
        cursor.execute("INSERT INTO templates (template_name, content) VALUES (?, ?)", template_tuple)
        conn.commit()
    except Error as e:
        print(e)


def update_template_db(conn, template):
    try:
        cursor = conn.cursor()
        template_tuple = (template.template_name, template.content, template.id)
        cursor.execute("UPDATE templates SET template_name=?, content=? WHERE id=?", template_tuple)
        conn.commit()
    except Error as e:
        print(e)


def delete_template_db(conn, template_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM templates WHERE id=?", (template_id,))
        conn.commit()
    except Error as e:
        print(e)

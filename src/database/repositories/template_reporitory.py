import sqlite3
from sqlite3 import Error

from loguru import logger

from database.scripts_sql import sql_query_all_templates
from database.seed_templates import templates


class TemplateRepository:
    """
    Repositorio para manejar las operaciones relacionadas con las plantillas.
    """

    def __init__(self, db):
        """
        Inicializa el repositorio con una instancia de la base de datos.

        Args:
            db (Database): Instancia de la clase Database.
        """
        self.db = db

    def check_if_templates_exist(self) -> bool:
        """
        Verifica si existen plantillas en la base de datos.

        Returns:
            bool: Verdadero si existen plantillas, falso en caso contrario.
        """
        try:
            self.db.cursor.execute("SELECT count(*) FROM templates")
            count = self.db.cursor.fetchone()[0]
            return count > 0
        except Error as e:
            logger.exception(f"{str(e)}")

    def insert_templates(self):
        """
        Inserta plantillas en la base de datos.

        """
        try:
            for template in templates:
                self.db.cursor.execute("INSERT INTO templates (template_name, content) VALUES (?, ?)", template)
            self.db.connection.commit()
        except Error as e:
            logger.exception(f"{str(e)}")

    def get_templates_db(self):
        try:
            cursor = self.db.cursor
            cursor.execute(sql_query_all_templates)
            templates = cursor.fetchall()
            return templates
        except Error as e:
            logger.exception(f"{str(e)}")

    def save_template_db(self, template):
        try:
            cursor = self.db.cursor
            template_tuple = (template.template_name, template.content)
            cursor.execute("INSERT INTO templates (template_name, content) VALUES (?, ?)", template_tuple)
            self.db.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            return False
        except Error as e:
            logger.exception(f"{str(e)}")
            return False

    def update_template_db(self, template):
        try:
            cursor = self.db.cursor
            template_tuple = (template.template_name, template.content, template.id)
            cursor.execute("UPDATE templates SET template_name=?, content=? WHERE id=?", template_tuple)
            self.db.connection.commit()
        except Error as e:
            logger.exception(f"{str(e)}")

    def delete_template_db(self, template_id):
        try:
            cursor = self.db.cursor
            cursor.execute("DELETE FROM templates WHERE id=?", (template_id,))
            self.db.connection.commit()
        except Error as e:
            logger.exception(f"{str(e)}")

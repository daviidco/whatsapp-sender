import datetime
import platform
import os

from loguru import logger


def newt_task(programa: str, path_script: str, task_name: str, start_boundary: datetime.datetime,
              descripcion: str="Task created by Python") -> None:
    """
    Initialize the UIComponentManager with a database connection.

    Args:
        template_repository (TemplateRepository): The template repository object.
    """

    if platform.system() == 'Windows':
        import win32com.client

        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()

        root_folder = scheduler.GetFolder('\\')
        task_def = scheduler.NewTask(0)
        task_def.RegistrationInfo.Description = descripcion

        task_triggers = task_def.Triggers
        trigger = task_triggers.Create(1)  # Tipo 1: diario
        trigger.StartBoundary = start_boundary  # Hora en formato 'YYYY-MM-DDTHH:MM:SS'

        task_settings = task_def.Settings
        task_settings.Enabled = True
        task_settings.Hidden = False

        action = task_def.Actions.Create(0)  # Tipo 0: Ejecutar un programa
        action.Path = programa
        action.Arguments = path_script

        root_folder.RegisterTaskDefinition(
            task_name,
            task_def,
            6,  # Constante para permitir que se sobrescriban las tareas existentes
            '',  # Usuario que ejecutará la tarea, en blanco para usar el usuario actual
            '',  # Contraseña del usuario que ejecutará la tarea, en blanco para usuario actual
            3  # Constante para permitir que la tarea se ejecute en cualquier momento
        )
    else:
        logger.exception("Operative system is not compatible")

"""
Configuración del entorno de pruebas para Behave.
"""
from django.test.runner import DiscoverRunner
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command

def before_all(context):
    """
    Configura el entorno antes de ejecutar cualquier prueba.
    """
    context.test_runner = DiscoverRunner()
    context.old_db_config = context.test_runner.setup_databases()

def after_all(context):
    """
    Limpia el entorno después de ejecutar todas las pruebas.
    """
    context.test_runner.teardown_databases(context.old_db_config)

def before_scenario(context, scenario):
    """
    Limpia la base de datos antes de cada escenario.
    """
    call_command('flush', verbosity=0, interactive=False)

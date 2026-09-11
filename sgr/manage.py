#!/usr/bin/env python
"""Punto de entrada para ejecutar comandos administrativos de Django."""
import os
import sys


def main():
    """Carga la configuracion y ejecuta el comando recibido en la consola."""
    # Este valor indica a Django donde encontrar settings.py.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgr.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # sys.argv contiene el comando escrito, por ejemplo: runserver o check.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

from core.database import crear_tablas
from ui.main_window import MainWindow


def main():
    crear_tablas()  # Inicializa infraestructura
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
from app.commands.settings import SettingsCommand


class CommandHandler:
    """
    Handles all terminal commands.

    Commands begin with "/".
    """

    def __init__(self):

        self.settings = SettingsCommand()

    def handle(
        self,
        command: str
    ) -> bool:
        """
        Execute a command.

        Returns
        -------
        bool

        True  -> command handled

        False -> not a command
        """

        command = command.strip().lower()

        if not command.startswith("/"):

            return False

        match command:

            case "/provider":

                self.settings.change_provider()

            case "/model":

                self.settings.change_model()

            case "/config":

                self.settings.show_configuration()

            case "/settings":

                self.settings.menu()

            case _:

                print(
                    f"\nUnknown command : {command}"
                )

                print(
                    "Available commands:"
                )

                print(
                    "/provider"
                )

                print(
                    "/model"
                )

                print(
                    "/config"
                )

                print(
                    "/settings"
                )

        return True
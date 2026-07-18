from app.configurations.selector import RuntimeSelector


class SettingsCommand:
    """
    Handles runtime configuration commands.
    """

    def __init__(self):

        self.selector = RuntimeSelector()

    # ======================================================
    # /provider
    # ======================================================

    def change_provider(self) -> None:

        print("\nChanging Provider...\n")

        self.selector.select_provider()

        print("\n✓ Provider updated successfully.")

    # ======================================================
    # /model
    # ======================================================

    def change_model(self) -> None:

        print("\nChanging Model...\n")

        self.selector.select_model()

        print("\n✓ Model updated successfully.")

    # ======================================================
    # /config
    # ======================================================

    def show_configuration(self) -> None:

        self.selector.show_current()

    # ======================================================
    # /settings
    # ======================================================

    def menu(self) -> None:

        while True:

            print("\n" + "=" * 50)
            print("Settings")
            print("=" * 50)

            print("1. Change Provider")
            print("2. Change Model")
            print("3. Show Configuration")
            print("4. Back")

            try:
                choice = input("\nSelect Option : ").strip()

                match choice:

                    case "1":

                        self.change_provider()

                    case "2":

                        self.change_model()

                    case "3":

                        self.show_configuration()

                    case "4":

                        print()

                        return

                    case _:

                        print("\nInvalid option.")

            except KeyboardInterrupt:
                print("\n\nExiting settings.")
                return
import builtins

class BeautifulTerminal:
    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "white": "\033[97m",
    }

    def __init__(self):
        self.original_print = builtins.print
        self.enable()

    def enable(self):
        """Überschreibt die Standard-`print()`-Funktion mit farbiger Ausgabe."""
        builtins.print = self.custom_print

    def disable(self):
        """Stellt die Original-`print()`-Funktion wieder her."""
        builtins.print = self.original_print

    def custom_print(self, *args, **kwargs):
        """Unsere angepasste Print-Funktion, die automatisch Farben hinzufügt."""
        message = " ".join(map(str, args))

        if "error" in message.lower():
            color = self.COLORS['red']
        elif "warn" in message.lower():
            color = self.COLORS['yellow']
        elif "success" in message.lower():
            color = self.COLORS['green']
        else:
            color = self.COLORS['white']

        self.original_print(f"{color}{message}{self.COLORS['reset']}", **kwargs)

bt = BeautifulTerminal()

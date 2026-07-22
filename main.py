"""Starting point for the Silver Screen Cinema application."""

import tkinter as tk
from tkinter import messagebox

from cinema import CinemaService
from storage import StorageError
from ui import CinemaApp


def main():
    """Load application data and start the graphical interface."""
    root = tk.Tk()
    try:
        service = CinemaService()
    except (StorageError, ValueError) as error:
        root.withdraw()
        messagebox.showerror("Cinema data error", str(error))
        root.destroy()
        return
    CinemaApp(root, service)
    root.mainloop()


if __name__ == "__main__":
    main()

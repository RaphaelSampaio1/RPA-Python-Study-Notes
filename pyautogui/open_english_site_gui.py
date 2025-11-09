#!/usr/bin/env python3
"""Small Tkinter GUI to open an English study site in the default browser.

Usage: run this file with Python. The window contains a single entry (pre-filled)
and a button to open the URL in your default browser. Press Enter to trigger the
button as well.
"""

import tkinter as tk
from tkinter import messagebox
import webbrowser

DEFAULT_URL = "https://learnenglish.britishcouncil.org/"


def open_site(url_text: str | None = None) -> None:
    """Open the given URL (or the entry/default). Adds http:// if scheme missing."""
    url = url_text or url_entry.get().strip() or DEFAULT_URL
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url
    try:
        webbrowser.open_new_tab(url)
    except Exception as exc:
        messagebox.showerror("Error", f"Could not open URL:\n{exc}")


def on_open_click() -> None:
    open_site()


def on_enter(event) -> None:
    on_open_click()


def main() -> None:
    global url_entry
    root = tk.Tk()
    root.title("Open English Study Site")
    root.resizable(False, False)
    # Small, simple window
    root.geometry("380x120")

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    label = tk.Label(frame, text="URL to open:")
    label.pack(anchor="w")

    url_entry = tk.Entry(frame, width=60)
    url_entry.insert(0, DEFAULT_URL)
    url_entry.pack(fill="x", pady=(4, 10))

    open_btn = tk.Button(frame, text="Open English Study Site", width=30, command=on_open_click)
    open_btn.pack()

    root.bind("<Return>", on_enter)
    root.mainloop()


if __name__ == "__main__":
    main()

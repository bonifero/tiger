"""Стартовое окно будущего практикума: Матричные игры и смешанные стратегии."""
import tkinter as tk
from tkinter import ttk

TITLE = 'Игры'
DESCRIPTION = 'Матричные игры и смешанные стратегии'
STATUS = "Заготовка: функциональность пока не реализована."


def create_window():
    root = tk.Tk()
    root.title(TITLE)
    root.geometry("640x220")
    frame = ttk.Frame(root, padding=24)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text=DESCRIPTION, wraplength=580).pack(pady=12)
    ttk.Label(frame, text=STATUS, wraplength=580).pack(pady=12)
    ttk.Button(frame, text="Закрыть", command=root.destroy).pack(pady=12)
    return root


def main():
    create_window().mainloop()


if __name__ == "__main__":
    main()

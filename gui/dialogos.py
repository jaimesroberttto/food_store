"""Helpers de Tkinter para mostrar mensajes y pedir confirmaciones desde la GUI."""

from tkinter import messagebox


def mostrar_error(mensaje: str) -> None:
    messagebox.showerror("Food Store", mensaje)


def mostrar_info(mensaje: str) -> None:
    messagebox.showinfo("Food Store", mensaje)


def confirmar(mensaje: str) -> bool:
    return messagebox.askyesno("Food Store", mensaje)

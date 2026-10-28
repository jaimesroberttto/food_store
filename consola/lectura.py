"""Helpers de lectura validada desde teclado, usados por los menús de consola."""

from enum import Enum
from typing import TypeVar

E = TypeVar("E", bound=Enum)


def leer_texto(mensaje: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("Este dato no puede estar vacío.")


def leer_opcional(mensaje: str) -> str | None:
    valor = input(mensaje).strip()
    return valor if valor else None


def leer_entero(mensaje: str, minimo: int | None = None) -> int:
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("Ingresá un número entero válido.")
            continue
        if minimo is not None and valor < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return valor


def leer_entero_opcional(mensaje: str) -> int | None:
    texto = input(mensaje).strip()
    if not texto:
        return None
    try:
        return int(texto)
    except ValueError:
        print("Valor inválido, se conserva el actual.")
        return None


def leer_flotante(mensaje: str, minimo: float | None = None) -> float:
    while True:
        texto = input(mensaje).strip()
        try:
            valor = float(texto)
        except ValueError:
            print("Ingresá un número válido.")
            continue
        if minimo is not None and valor < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return valor


def leer_flotante_opcional(mensaje: str) -> float | None:
    texto = input(mensaje).strip()
    if not texto:
        return None
    try:
        return float(texto)
    except ValueError:
        print("Valor inválido, se conserva el actual.")
        return None


def leer_confirmacion(mensaje: str) -> bool:
    while True:
        texto = input(f"{mensaje} (S/N): ").strip().upper()
        if texto in ("S", "N"):
            return texto == "S"
        print("Respondé con S o N.")


def leer_opcion_enum(mensaje: str, enum_cls: type[E]) -> E:
    opciones = list(enum_cls)
    print(mensaje)
    for indice, opcion in enumerate(opciones, start=1):
        print(f"{indice}. {opcion.value}")
    while True:
        indice = leer_entero("Seleccione: ")
        if 1 <= indice <= len(opciones):
            return opciones[indice - 1]
        print("Opción fuera de rango.")

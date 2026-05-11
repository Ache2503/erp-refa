# app/repositories/__init__.py
"""
Repositorio de datoss: acceso a la base de datos, consultas, filtros.
"""
from .categoria_repository import CategoriaRepository
__all__ = [
    "CategoriaRepository",
]

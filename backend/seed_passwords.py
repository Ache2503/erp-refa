"""
Script para asignar contraseñas iniciales a empleados existentes.
Uso: python seed_passwords.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import bcrypt
from app.core.database import SessionLocal
from app.models.empleados import Empleados

CREDENTIALS = [
    ("admin@erp.com", "admin123"),
    ("juan@test.com", "admin123"),
    ("maria@test.com", "admin123"),
    ("carlos@test.com", "admin123"),
    ("ana@test.com", "admin123"),
    ("pedro@test.com", "admin123"),
]


def main():
    db = SessionLocal()
    try:
        for email, password in CREDENTIALS:
            emp = db.query(Empleados).filter(Empleados.email == email).first()
            if emp:
                emp.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                print(f"  ✓ {email} → contraseña asignada")
            else:
                print(f"  ✗ {email} → no encontrado en BD")
        db.commit()
        print("\n✅ Contraseñas asignadas correctamente.")
        print("   Usuarios: admin@erp.com / juan@test.com / maria@test.com / carlos@test.com / ana@test.com / pedro@test.com")
        print("   Contraseña: admin123 (para todos)")
    finally:
        db.close()


if __name__ == "__main__":
    main()

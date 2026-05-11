# split_models.py
import os
import re

MODELS_DIR = "app/models"
GENERATED_FILE = os.path.join(MODELS_DIR, "generated.py")

def split_models():
    # Asegurar que el directorio existe
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    with open(GENERATED_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Buscar todas las definiciones de clase que heredan de Base
    pattern = r'class (\w+)\(Base\):(.*?)(?=\n\nclass |\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    imports = [
        "from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint\n",
        "from sqlalchemy.orm import relationship\n",
        "from app.core.database import Base\n\n"
    ]
    
    # Lista para acumular nombres de clase para __init__
    class_names = []
    
    for class_name, class_body in matches:
        class_names.append(class_name)
        # Nombre de archivo en snake_case (ej: PedidoCliente -> pedido_cliente)
        filename = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower() + ".py"
        filepath = os.path.join(MODELS_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(imports)
            f.write(f"class {class_name}(Base):\n")
            f.write(class_body)
            if not class_body.strip().endswith('\n'):
                f.write('\n')
        
        print(f"✅ Creado: {filename}")
    
    # Crear __init__.py
    init_path = os.path.join(MODELS_DIR, "__init__.py")
    with open(init_path, "w", encoding="utf-8") as f:
        f.write("# Importa todos los modelos para que SQLAlchemy los registre\n")
        f.write("from app.core.database import Base\n\n")
        for name in class_names:
            # Convertir PascalCase a snake_case para el módulo
            module = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
            f.write(f"from .{module} import {name}\n")
    
    print(f"\n📦 __init__.py actualizado con {len(class_names)} modelos.")
    print("Ahora puedes eliminar generated.py si lo deseas.")

if __name__ == "__main__":
    split_models()
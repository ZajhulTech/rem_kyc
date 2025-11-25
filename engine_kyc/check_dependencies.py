"""
Script para verificar dependencias del proyecto
"""

import importlib
import sys

def check_module(module_name, pip_name=None):
    """Verifica si un módulo está instalado"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        pip_name = pip_name or module_name
        print(f"❌ {module_name} - Error: {e}")
        print(f"   Ejecuta: pip install {pip_name}")
        return False

def main():
    print("🔍 Verificando dependencias del proyecto KYC...")
    print("=" * 50)
    
    modules_to_check = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn[standard]"),
        ("sqlalchemy", "sqlalchemy"),
        ("asyncpg", "asyncpg"),
        ("motor", "motor"),
        ("pydantic", "pydantic"),
        ("email_validator", "email-validator"),
        ("pymongo", "pymongo"),
        ("dotenv", "python-dotenv"),
        ("alembic", "alembic"),
    ]
    
    all_ok = True
    for module_name, pip_name in modules_to_check:
        if not check_module(module_name, pip_name):
            all_ok = False
    
    print("=" * 50)
    if all_ok:
        print("🎉 Todas las dependencias están instaladas correctamente!")
    else:
        print("⚠️  Algunas dependencias faltan. Ejecuta los comandos sugeridos.")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
Script para ejecutar el motor de reglas de verificación KYC
"""

import asyncio
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dependencies.postgres_dependencies import get_postgres_unit_of_work
from dependencies.mongo_dependencies import get_mongo_unit_of_work
from core.userstorys.rule_engine_story import RuleEngineStory


async def run_single_execution():
    """
    Ejecuta una sola pasada del motor de reglas
    """
    print("🚀 Iniciando motor de reglas KYC...")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Obtener unidades de trabajo
        uow_postgres = get_postgres_unit_of_work()
        uow_mongo = get_mongo_unit_of_work()
        
        # Crear instancia del motor
        rule_engine = RuleEngineStory(uow_postgres, uow_mongo)
        
        # Procesar verificaciones pendientes
        print("🔍 Buscando verificaciones pendientes...")
        stats = await rule_engine.process_pending_verifications(batch_size=50)
        
        # Mostrar resultados
        print("\n📊 RESULTADOS DEL PROCESAMIENTO:")
        print(f"   ✅ Procesadas: {stats['processed']}")
        print(f"   ✅ Actualizadas: {stats['updated']}")
        print(f"   ❌ Errores: {stats['errors']}")
        
        if stats['processed'] == 0:
            print("   ℹ️  No hay verificaciones pendientes para procesar")
            
    except Exception as e:
        print(f"💥 Error durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("🎯 Procesamiento completado exitosamente!")
    return 0


def main():
    """
    Función principal con interfaz de línea de comandos
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Motor de reglas KYC')
    parser.add_argument(
        '--mode', 
        choices=['single', 'continuous'], 
        default='single',
        help='Modo de ejecución: single (una vez) o continuous (worker)'
    )
    parser.add_argument(
        '--interval', 
        type=int, 
        default=5,
        help='Intervalo en minutos para modo continuous (default: 5)'
    )
    
    args = parser.parse_args()
    
    return asyncio.run(run_single_execution())

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
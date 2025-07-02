#!/usr/bin/env python3
"""
Script de Prueba Multi-Escala (versión corta)
Solo ejecuta 1K y 10K para verificar funcionamiento
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime

# Importar la clase principal
sys.path.append('.')
from multi_scale_test import MultiScalePerformanceTester

class TestMultiScaleTester(MultiScalePerformanceTester):
    def __init__(self):
        # Solo las dos primeras escalas para prueba rápida
        self.scales = [1000, 10000]
        self.scale_names = ["1K", "10K"]
        self.results = {}

def main():
    print("🧪 PRUEBA RÁPIDA - Script Multi-Escala")
    print("📊 Solo ejecutará 1K y 10K para verificar funcionamiento")
    print("-" * 50)
    
    response = input("¿Ejecutar prueba rápida (1K + 10K)? (y/N): ")
    if response.lower() != 'y':
        print("❌ Prueba cancelada")
        return
    
    tester = TestMultiScaleTester()
    
    try:
        tester.run_full_multi_scale_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

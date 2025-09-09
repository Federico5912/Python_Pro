import os 
import json
import time
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Data')
os.makedirs(DATA_DIR, exist_ok=True)
TASKS_DIR = os.path.join(DATA_DIR, 'Tasks.json')

def cargar_tareas():
    if not os.path.exists(TASKS_DIR):
        return[]
    else:
        with open(TASKS_DIR, 'r', encoding = "utf-8") as f:
            tareas = json.load(f)
            for t in tareas:
                if "notificado_en" not in t:
                    t["notificado_en"] = None
            return tareas

def guardar_tareas(tareas):
    with open(TASKS_DIR, 'w', encoding = "utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

def validar_hora(hhmm):
    try:
        datetime.datetime.strptime(hhmm, "%H:%M")
        return True
    except ValueError:
        return False

def mostrar_tareas(tareas):
    if not tareas:
        print("No hay tareas pendientes.")
    else:
        print("Tareas pendientes:")
        for i, t in enumerate(tareas, start=1):
            print(f"{i}. {t['texto']} ⏰ {t['hora']}")

def agregar_tarea(tareas):
    print("--------------------------------")
    texto = input("Ingrese la descripción de la tarea: ").strip()
    if not texto:
        
        print("La descripción no puede estar vacía.")
        return
    
    hora = input("Ingrese la hora de la tarea (HH:MM): ").strip()
    if not validar_hora(hora):
        print("Formato de hora inválido. Use HH:MM.")
        return
    
    tarea = {"texto": texto, "hora": hora, "notificado_en": None}
    tareas.append(tarea)
    guardar_tareas(tareas)
    print("--------------------------------")
    print("Tarea agregada exitosamente.")

def eliminar_tarea(tareas):
    if not tareas:
        print("No hay tareas para eliminar.")
        return
    mostrar_tareas(tareas)
    try:
        idx = int(input("Ingrese el número de la tarea a eliminar: "))
        if 1 <= idx <= len(tareas):
            tarea_eliminada = tareas.pop(idx - 1)
            guardar_tareas(tareas)
            print(f"Tarea '{tarea_eliminada['texto']}' eliminada.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")

def editar_tarea(tareas):
    if not tareas:
        print("No hay tareas para editar.")
        return
    mostrar_tareas(tareas)
    try:
        idx = int(input("Ingrese el número de la tarea a editar: "))
        
        if 1 <= idx <= len(tareas):
            t = tareas[idx - 1]
            nuevo_texto = input(f"Nuevo texto: ")
            if nuevo_texto:
                t['texto'] = nuevo_texto
            
            nueva_hora = input(f"Nueva hora (HH:MM): ")            
            if nueva_hora:
                if validar_hora(nueva_hora):
                    t['hora'] = nueva_hora
                else:
                    print("Formato de hora inválido. Use HH:MM.")
                    return
            
            guardar_tareas(tareas)
            print("Tarea editada exitosamente.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")

def revisar_notificaciones(tareas):
    ahora_hhmm = datetime.datetime.now().strftime("%H:%M")
    hoy = datetime.datetime.today().isoformat()
    for t in tareas:
        if t['hora'] == ahora_hhmm and t.get("notificado_en") != hoy:
            print(f"\n🔔 Recordatorio: {t['texto']} ⏰ {t['hora']}\n")
            t["notificado_en"] = hoy
    guardar_tareas(tareas)

def marcar_completada(tareas):
    if not tareas:
        print("--------------------------------")
        print("No hay tareas para marcar como completadas.")
        return
    mostrar_tareas(tareas)
    try:
        print("--------------------------------")
        idx = int(input("Ingrese el número de la tarea completada: "))
        if 1 <= idx <= len(tareas):
            tarea = tareas.pop(idx - 1)
            tarea['completada_en'] = datetime.datetime.now().isoformat()
            completadas = cargar_completadas()
            completadas.append(tarea)
            guardar_completadas(completadas)
            guardar_tareas(tareas)
            print(f"Tarea '{tarea['texto']}' marcada como completada.")
        else:
            print("--------------------------------")
            print("Número inválido.")
    except ValueError:
        print("--------------------------------")
        print("Entrada inválida. Por favor ingrese un número.")

COMPLETADAS_DIR = os.path.join(DATA_DIR, 'Completadas.json')

def cargar_completadas():
    if not os.path.exists(COMPLETADAS_DIR):
        return []
    with open(COMPLETADAS_DIR, 'r', encoding="utf-8") as f:
        return json.load(f)

def guardar_completadas(completadas):
    with open(COMPLETADAS_DIR, 'w', encoding="utf-8") as f:
        json.dump(completadas, f, ensure_ascii=False, indent=2)

def mostrar_completadas():
    completadas = cargar_completadas()
    if not completadas:
        print("--------------------------------")
        print("No hay tareas completadas.")
    else:
        print("--------------------------------")
        print("Tareas completadas:")
        for i, t in enumerate(completadas, start=1):
            fecha = t.get('completada_en', 'N/A')
            print(f"{i}. {t['texto']} ⏰ {t['hora']} ✅ ({fecha})")

def buscar_tareas(tareas):
    print("--------------------------------")
    query = input("Buscar tareas por texto: ").strip().lower()
    resultados = [t for t in tareas if query in t['texto'].lower()]
    if not resultados:
        print("--------------------------------")
        print("No se encontraron tareas que coincidan.")
    else:
        print("--------------------------------")
        print("Resultados de búsqueda:")
        for i, t in enumerate(resultados, start=1):
            print(f"{i}. {t['texto']} ⏰ {t['hora']}")

def menu():
    tareas = cargar_tareas()
    while True:
        print("\n--- Menú de tareas ---")
        print("1. Mostrar tareas")
        print("2. Agregar tarea")
        print("3. Eliminar tarea")
        print("4. Editar tarea")
        print("5. Marcar tarea como completada")
        print("6. Mostrar tareas completadas")
        print("7. Buscar tarea")
        print("8. Salir")
        revisar_notificaciones(tareas)
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            mostrar_tareas(tareas)
        elif opcion == "2":
            agregar_tarea(tareas)
        elif opcion == "3":
            eliminar_tarea(tareas)
        elif opcion == "4":
            editar_tarea(tareas)
        elif opcion == "5":
            marcar_completada(tareas)
        elif opcion == "6":
            mostrar_completadas()
        elif opcion == "7":
            buscar_tareas(tareas)
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()

import random

def pedir_numero(mensaje: str) -> int:
    """Solicita un número entero y evita errores si el usuario escribe texto"""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Error: Se debe ingresar un número entero válido.")

def generar_numero_unico():
    print("\n--- GENERADOR DE UN SÓLO NÚMERO ---")
    minimo = pedir_numero("Ingresar el valor mínimo: ")
    maximo = pedir_numero("Ingresar el valor máximo: ")

    if minimo > maximo:
        print("El valor mínimo no puede ser mayor que el máximo. Invirtiendo valores.")
        minimo, maximo = maximo, minimo

    resultado = random.randint(minimo, maximo)
    print(f"\nNúmero generado entre {minimo} y {maximo}: {resultado}")

def generar_lista_numeros():
    print("\n--- GENERADOR DE VARIOS NÚMEROS ---")
    cantidad = pedir_numero("¿Cuántos números deseas generar?: ")

    if cantidad <= 0:
        print("Error: La cantidad debe ser mayor a cero.")
        return

    minimo = pedir_numero("Ingresar el valor mínimo del rango: ")
    maximo = pedir_numero("Ingresar el valor máximo del rango: ")

    if minimo > maximo:
        print("El valor mínimo no puede ser mayor que el máximo. Invirtiendo valores.")
        minimo, maximo = maximo, minimo

    # Genera una lista de números aleatorios
    numeros = [random.randint(minimo, maximo) for _ in range(cantidad)]

    print("\nResultados Obtenidos:")
    print(numeros)

def main():
    while True:
        print("\n" + "=" * 40)
        print("GENERADOR DE NÚMEROS ALEATORIOS")
        print("=" * 40)
        print("1. Generar un único número")
        print("2. Generar una lista de números")
        print("3. Salir")

        opcion = input("\Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            generar_numero_unico()
        elif opcion == "2":
            generar_lista_numeros()
        elif opcion == "3":
            print("Gracias por usar el generador de números. Hasta luego.")
            break
        else:
            print("Error: Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
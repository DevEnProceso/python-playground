def celsius_a_fahrenheit(celsius: float) -> float:
    return (celsius * 9/5) + 32

def fahrenheit_a_celsius(farenheit: float) -> float:
    return (farenheit - 32) * 5/9

def kilometros_a_millas(km: float) -> float:
    return km * 0.621371

def millas_a_kilometros(millas: float) -> float:
    return millas / 0.621371

def solicitar_numero(mensaje: str) -> float:
    """Pide un número evitando que el programa falle si se digita algo inválido"""
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("Error: Dato inválido. Favor ingresar un número válido.")

def menu_temperatura():
    print("\n--- CONVERSOR DE TEMPERATURA ---")
    print("1. Celsius a Fahrenheit")
    print("2. Fahrenheit a Celsius")
    op = input("Selecciona una opción (1-2): ").strip()

    if op == "1":
        c = solicitar_numero("Ingresa grados Celsius: ")
        print(f"{c} °C equivale a {celsius_a_fahrenheit(c):.2f} °F")
    elif op == "2":
        f = solicitar_numero("Ingresa grados Fahrenheit: ")
        print(f" {f} °F equivlae a {fahrenheit_a_celsius(f):.2f} °C")
    else:
        print("Error: Opción Inválida. Intente de nuevo")

def menu_distancia():
    print("\n--- CONVERSOR DE DISTANCIA ---")
    print("1. Kilómetros a Millas")
    print("2. Millas a Kilómetros")
    op = input("Selecciona una opción (1-2): ").strip()

    if op == "1":
        km = solicitar_numero("Ingresa kilómetros: ")
        print(f"{km} km equivale a {kilometros_a_millas(km):.2f} millas")
    elif op == "2":
        millas = solicitar_numero("Ingrese millas: ")
        print(f"{millas} millas equivale a {millas_a_kilometros(millas):.2f} km")
    else:
        print("Error: Opción Inválida. Intente de nuevo")

def main():
    while True:
        print("\n" + "=" *40)
        print("CONVERSOR MULTIUSOS DE UNIDADES")
        print("=" *40)
        print("1. Convertir Temperatura (°C / °F)")
        print("2. Convertir Distancia (km / millas)")
        print("3. Salir")

        opcion = input("\nSelecciona una opción (1-3): ").strip()

        if opcion == "1":
            menu_temperatura()
        elif opcion == "2":
            menu_distancia()
        elif opcion == "3":
            print("\nGracias por usar el conversor. Hasta pronto.")
            break
        else:
            print("Error: Opción Inválida. Intente de nuevo")

if __name__ == "__main__":
    main()
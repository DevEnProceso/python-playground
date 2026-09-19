def calcular_imc(peso_kg: float, altura_m: float) -> float:
    """Calcula el IMC usando la fórmula: peso / (altura^2)"""
    return peso_kg / (altura_m ** 2)

def clasificar_imc(imc: float) -> str:
    """Clasifica el resultado del IMC según los rangos estándar de salud."""
    if imc < 16.0:
        return "Delgadez severa."
    elif 16.0 <= imc < 17.0:
        return "Delgadez moderada."
    elif 17.0 <= imc < 18.5:
        return "Delgadez leve."
    elif 18.5 <= imc < 25.0:
        return "Peso normal (Saludable)."
    elif 25.0 <= imc < 30.0:
        return "Preobesidad (Sobrepeso)."
    elif 30.0 <= imc < 35.0:
        return "Obesidad Grado I (Leve)."
    elif 35.0 <= imc < 40.0:
        return "Obesidad Grado II (Moderada)."
    else:
        return "Obesidad Grado III (Mórbida)."

def obtener_numero_positivo(mensaje: str) -> float:
    """Solicita un número al usuario y revisa que sea positivo y numérico."""
    while True:
        try:
            valor = float(input(mensaje).strip())
            if valor > 0:
                return valor
            print("Error: Por favor, ingresar un valor mayor a cero (0).")
        except ValueError:
            print("Error: Entrada inválida. Ingresar un número válido (ejemplo: 1.71 o 84)")

def main():
    print("=" * 45)
    print("CALCULADORA DE ÍNDICE DE MASA CORPORAL (IMC)")
    print("=" * 45)

    peso = obtener_numero_positivo("Ingresar el peso en kilogramos (kg): ")
    altura = obtener_numero_positivo("Ingresar la altura en metros (m): ")

    imc = calcular_imc(peso, altura)
    categoria  = clasificar_imc(imc)

    print("\n" + "-" * 35)
    print("RESULTADO DE ANÁLISIS")
    print("-" * 35)
    print(f" ° Peso ingresado: {peso:.2f} kg")
    print(f" ° Estatura ingresada: {altura:.2f} m")
    print(f" ° Tu IMC calculado: {imc:.2f}")
    print(f" ° Clasificación: {categoria}")
    print("-" * 35)

if __name__ == "__main__":
    main()
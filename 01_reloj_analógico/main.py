import tkinter as tk
import time
import math

def actualizar_reloj(canvas, ventana):
    # Quita las manecillas anteriores.
    canvas.delete("manecillas")

    # Obtiene la hora actual
    ahora = time.localtime()
    horas = ahora.tm_hour % 12
    minutos = ahora.tm_min
    segundos = ahora.tm_sec

    # Calcula los ángulos en radiales para las manecillas
    angulo_seg = math.radians(segundos * 6-90)
    angulo_min = math.radians((minutos + segundos / 60)* 6-90)
    angulo_hor = math.radians((horas + minutos / 60)* 30-90)

    #Dibuja las manecillas
    canvas.create_line(150,150,150+50 * math.cos(angulo_hor), 150+50*math.sin(angulo_hor), fill="white", width=4, tags="manecillas")
    canvas.create_line(150,150,150+75 * math.cos(angulo_min), 150+75*math.sin(angulo_min), fill="#00adb5", width=3, tags="manecillas")
    canvas.create_line(150,150,150+90 * math.cos(angulo_seg), 150+90*math.sin(angulo_seg), fill="#ff2e63", width=1.5, tags="manecillas")
    ventana.after(1000, lambda: actualizar_reloj(canvas,ventana))

def main():
    # Crea una ventana principal
    ventana = tk.Tk()
    ventana.title("Reloj Analógico - Python Playground")
    ventana.geometry("320x320")
    ventana.configure(bg="#222831")

    # Crea un canvas
    canvas = tk.Canvas(ventana, width=300, height=300, bg="#222831", highlightthickness=0)
    canvas.pack(pady=10)

    # Marco exterior del reloj
    canvas.create_oval(10,10,290,290, outline="#00adb5", width=3)
    canvas.create_oval(145,145,155,155, fill="white")

    # Inicia la animación
    actualizar_reloj(canvas, ventana)

    # Mantiene la ventana abierta
    ventana.mainloop()

if __name__ == "__main__":
    main()
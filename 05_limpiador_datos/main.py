import os
import pandas as pd
import unicodedata
from itertools import combinations

VALORES_NULOS = ["", "nan", "NaN", "Sin Registro", "Sin_Correo", "N/A", "n/a", "NA", "sin_correo"]

VALORES_VERDADEROS = {"si", "sí", "yes", "y", "true", "1", "activo", "verdadero", "s"}

FORMATOS_FECHA = [
    # Año primero (nunca es ambiguo)
    "%Y-%m-%d", "%Y/%m/%d",
    # Día primero (el orden que se usa en Costa Rica)
    "%d-%m-%Y", "%d/%m/%Y",
    # Mes primero (estilo de Estados Unidos)
    "%m-%d-%Y", "%m/%d/%Y",
    # Lo mismo con año de 2 dígitos
    "%d-%m-%y", "%d/%m/%y",
    "%m-%d-%y", "%m/%d/%y",
]

VALOR_VACIO = "N/A"

# ---- FUNCIONES DE LIMPIEZA -------
def limpiar_booleanos(col: pd.Series) -> pd.Series:
    texto = col.astype("string").str.strip().str.lower()
    resultado = texto.isin(VALORES_VERDADEROS).astype("boolean")
    return resultado.where(texto.notna(), pd.NA)

def limpiar_moneda(col: pd.Series) -> pd.Series:
    texto = col.astype("string").str.replace(r"[^\d,.\-]", "", regex=True)
    tiene_coma = texto.str.contains(",", na=False)
    con_formato_latino = texto.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    texto = texto.where(~tiene_coma, con_formato_latino)
    return pd.to_numeric(texto, errors="coerce")

def limpiar_fechas(col: pd.Series) -> pd.Series:
    col = col.astype("string")
    resultado = pd.to_datetime(col, format=FORMATOS_FECHA[0], errors="coerce")
    for formato in FORMATOS_FECHA[1:]:
        intento = pd.to_datetime(col, format=formato, errors="coerce")
        resultado = resultado.fillna(intento)
    return resultado.dt.strftime("%Y-%m-%d")

def limpiar_nombres(col: pd.Series) -> pd.Series:
    #Corrige "Apellido, Nombre" a "Nombre Apellido" y elimina espacios innecesarios
    col = col.astype("string")
    col = col.str.replace(r"^\s*(.+?)\s*,\s*(.+?)\s*$", r"\2 \1", regex=True)
    return col.str.replace(r"\s+", " ", regex=True).str.strip().str.title()

def limpiar_numero(col: pd.Series) -> pd.Series:
    texto = col.astype("string").str.replace(",", ".", regex=False)
    return pd.to_numeric(texto, errors="coerce")

def limpiar_email(col: pd.Series) -> pd.Series:
    #Correos en minúscula y sin espacios
    return col.astype("string").str.strip().str.lower()

def quitar_tildes(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normalizado if not unicodedata.combining(c))

def marcar_posibles_duplicados(df: pd.DataFrame, columnas: list, minimo: int = 3) -> pd.DataFrame:
    df = df.copy()
    sospechosos = pd.Series(False, index=df.index)

    for combo in combinations(columnas, minimo):
        subset = df[list(combo)]
        validas = subset.notna().all(axis=1) # ninguna es nula en este grupo de columnas
        repetidas = subset.duplicated(keep=False) # coinciden en TODAS las columnas del combo
        sospechosos |= (validas & repetidas)

    df["posible_duplicado"] = sospechosos
    return df

def rellenar_vacios (df: pd.DataFrame) -> pd.DataFrame:
    # Rellena vacios de columnas, exceptuando los numéricos.
    df = df.copy()
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(VALOR_VACIO)
    return df

LIMPIEZA_POR_COLUMNA = {
    "nombre": limpiar_nombres,
    "activo": limpiar_booleanos,
    "salario": limpiar_moneda,
    "fecha_registro": limpiar_fechas,
    "puntuacion": limpiar_numero,
    "edad": limpiar_numero,
    "email": limpiar_email
}

def limpiar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # df es DataFrame
    df = df.copy()

    #1. Encabezados uniformes
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    df.columns = [quitar_tildes(c) for c in df.columns]

    #2 Quita los espacios de los textos y convierte los vacíos en nulos reales
    for col in df.columns:
        if df[col].dtype == "object" or pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].astype("string").str.strip()
    df = df.replace(VALORES_NULOS, pd.NA)

    #3. Borra filas vacías
    columnas_datos = [c for c in df.columns if c != "id"]
    df = df.dropna(how="all", subset=columnas_datos)
    
    #4. Limpieza de cada columna
    for columna, funcion in LIMPIEZA_POR_COLUMNA.items():
        if columna in df.columns:
            df[columna] = funcion(df[columna])

    #5. Duplicados exactos al final, ignorando el id
    df = df.drop_duplicates(subset=columnas_datos)

    #6. Marcar posibles duplicados (3 o más columnas iguales, sin contar vacíos)
    return marcar_posibles_duplicados(df, columnas_datos, minimo=3)

def cargar_archivo(ruta_archivo: str) -> pd.DataFrame | None:
    """Carga un archivo CSV o Excel y lo convierte en un DataFrame de Pandas"""
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return None

    # Detecta la extensión del archivo para saber como leerlo.
    ext = os.path.splitext(ruta_archivo)[1].lower()

    try:
        if ext == ".csv": 
            try:
                return pd.read_csv(ruta_archivo, encoding="utf-8", on_bad_lines="warn")
            except UnicodeDecodeError: #El CSV de Excel suele venir en latin-1
                return pd.read_csv(ruta_archivo, encoding="latin-1", on_bad_lines="warn")
            
        if ext in (".xls", ".xlsx"):
            return pd.read_excel(ruta_archivo)
        print("Error: Formato no soportado. El archivo debe ser .csv, .xls o .xlsx")
    except Exception as e:
        print(f"Error: El archivo no se pudo abrir: {e}")
    return None

def guardar_archivo(df: pd.DataFrame, ruta_original: str) -> None:
    """Guarda los datos limpios en un nuevo archivo para no sobrescribir el original."""
    nombre_base, ext = os.path.splitext(ruta_original)
    ext = ext.lower()
    if ext == ".xls":
        ext = ".xlsx"
    ruta_salida = f"{nombre_base}_LIMPIO{ext}"

    try:
        if ext == ".csv":
            df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
        else:
            df.to_excel(ruta_salida, index=False)

        print("Proceso finalizado exitósamente.")
        print(f"Archivo limpio guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error: No se pudo guardar el archivo: {e}")

def main():
    print("\n" + "=" * 50)
    print("LIMPIADOR AUTOMÁTICO DE DATOS (CSV / EXCEL)")
    print("=" * 50)

    # Le pide la ruta del archivo al usuario y Quita las comillas de ser necesario
    ruta = input("\nIngrese la ruta o nombre del archivo (.csv, .xls o .xlsx): ").strip().strip("\"'")

    #1. Cargar
    datos = cargar_archivo(ruta)

    if datos is None:
        return

    #2. Limpiar
    limpios = limpiar_dataframe(datos)
    limpios = rellenar_vacios(limpios)
    print(f"Filas: {len(datos)} -> {len(limpios)} ({len(datos) - len(limpios)} eliminadas.)")

    #3. Guardar
    guardar_archivo(limpios, ruta)

if __name__ == "__main__":
    main()
import pandas as pd

def user_based_recommendation(file_path):
    try:
        user_df = pd.read_csv(file_path, on_bad_lines='skip')
        
    except FileNotFoundError:
        print("Error: El archivo no existe en esa ruta.")
        return None
    except Exception as e:
        print(f"Ocurrió un error leyendo el CSV: {e}")
        return None

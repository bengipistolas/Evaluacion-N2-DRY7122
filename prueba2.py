import requests
import json

API_KEY = 'e70e0504-c80d-4d3a-989e-9e1338a55b9a'
BASE_URL = 'https://graphhopper.com/api/1'

def obtener_cordenadas(city):
    url = f"{BASE_URL}/geocode?q={city}&locale=es&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if len(data['hits']) > 0:
        lat = data['hits'][0]['point']['lat']
        lng = data['hits'][0]['point']['lng']
        return lat, lng
    else:
        raise Exception("No se encontraron coordenadas para la ciudad proporcionada.")

def obtener_ruta(from_coords, to_coords):
    url = f"{BASE_URL}/route"
    params = {
        'point': [f"{from_coords[0]},{from_coords[1]}", f"{to_coords[0]},{to_coords[1]}"],
        'vehicle': 'car',
        'locale': 'es',
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def calcular_combustible(distance_km, fuel_consumption_per_100km=8.5):
    return (distance_km * fuel_consumption_per_100km) / 100

def main():
    while True:
        print("Menu de opciones:")
        print("1. Medir la distancia entre dos ciudades")
        print("q. Salir del programa")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            ciudad_origen = input("Ingrese Ciudad de Origen: ")
            ciudad_destino = input("Ingrese Ciudad de Destino: ")

            try:
                from_coords = obtener_cordenadas(ciudad_origen)
                to_coords = obtener_cordenadas(ciudad_destino)
                route_data = obtener_ruta(from_coords, to_coords)

                distance_km = route_data['paths'][0]['distance'] / 1000
                time_seconds = route_data['paths'][0]['time'] / 1000
                fuel_needed = calcular_combustible(distance_km)

                hours, remainder = divmod(time_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                print(f"\nDistancia: {distance_km:.2f} km")
                print(f"Duración del viaje: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos")
                print(f"Combustible requerido: {fuel_needed:.2f} litros")

                for instruction in route_data['paths'][0]['instructions']:
                    print(instruction['text'])

            except Exception as e:
                print(f"Error: {e}")

        elif choice == 'q':
            print("Saliendo del programa ")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
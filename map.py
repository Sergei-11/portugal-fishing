import folium
import requests
import ephem
from datetime import datetime
import webbrowser

# Локации с приблизительной глубиной
locations = {
    "Тежу (Лиссабон)": {"lat": 38.705, "lon": -9.135, "depth": "10-15 м"},
    "Кашкайш (Cascais)": {"lat": 38.693, "lon": -9.428, "depth": "5-10 м"},
    "Гиншу (Guincho)": {"lat": 38.733, "lon": -9.473, "depth": "20-30 м"},
    "Синтра (Praia Grande)": {"lat": 38.820, "lon": -9.475, "depth": "15-25 м"},
    "Сетубал (Setúbal)": {"lat": 38.510, "lon": -8.900, "depth": "10-20 м"},
    "Пенише (Peniche)": {"lat": 39.355, "lon": -9.380, "depth": "25-40 м"},
    "Лейрия (Nazaré)": {"lat": 39.602, "lon": -9.070, "depth": "30-50 м"},
    "Синиш (Sines)": {"lat": 37.955, "lon": -8.870, "depth": "40-60 м"},
    "Лагуш (Lagos)": {"lat": 37.100, "lon": -8.670, "depth": "15-25 м"},
    "Фару (Faro)": {"lat": 37.010, "lon": -7.930, "depth": "5-10 м"}
}

print("Собираем данные о погоде и воде. Пожалуйста, подождите...")

# Создаем карту
m = folium.Map(location=[38.72, -9.14], zoom_start=9, tiles="Esri WorldImagery")

for name, data in locations.items():
    lat, lon = data["lat"], data["lon"]
    
    try:
        # Погода
        r = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude": lat, "longitude": lon, "current": "wind_speed_10m,pressure_msl,temperature_2m", "timezone": "Europe/Lisbon"}).json()
        # Море
        r_m = requests.get("https://marine-api.open-meteo.com/v1/marine", params={"latitude": lat, "longitude": lon, "current": "wave_height,sea_surface_temperature", "timezone": "Europe/Lisbon"}).json()
        
        wind = r["current"]["wind_speed_10m"]
        pres = r["current"]["pressure_msl"]
        temp = r["current"]["temperature_2m"]
        wave = r_m["current"]["wave_height"]
        sst = r_m["current"]["sea_surface_temperature"]
        
        # HTML-код окошка (появляется при наведении)
        tooltip_html = f"""
        <div style="font-family: Arial; font-size: 14px; min-width: 180px;">
            <h4 style="margin:0; color: #d35400;">{name}</h4>
            <hr style="margin: 5px 0;">
            <b>Глубина:</b> {data['depth']}<br>
            <b>Темп. воды:</b> {sst} °C<br>
            <b>Ветер:</b> {wind} км/ч<br>
            <b>Волна:</b> {wave} м<br>
            <b>Давление:</b> {pres} гПа<br>
            <b>Темп. воздуха:</b> {temp} °C
        </div>
        """
        
        # Ставим маркер
        folium.Marker(
            [lat, lon],
            tooltip=folium.Tooltip(tooltip_html, permanent=False),
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        
    except Exception as e:
        print(f"Ошибка для {name}: {e}")

# Сохраняем в HTML
file_name = "map_final.html"
m.save(file_name)
print(f"Готово! Карта сохранена в файл: {file_name}")

# Открываем в браузере
webbrowser.open(file_name)

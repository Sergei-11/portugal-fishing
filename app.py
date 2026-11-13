import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import ephem
from datetime import datetime
import json

st.set_page_config(layout="wide")
st.title("🎣 Карта рыбалки (Лиссабон)")

if "active_lat" not in st.session_state:
    st.session_state.active_lat = 38.705
    st.session_state.active_lon = -9.135

# Функции для получения данных
@st.cache_data(ttl=600)
def get_weather(lat, lon):
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude": lat, "longitude": lon, "current": "wind_speed_10m,pressure_msl", "timezone": "Europe/Lisbon"}).json()
        r_m = requests.get("https://marine-api.open-meteo.com/v1/marine", params={"latitude": lat, "longitude": lon, "current": "wave_height", "timezone": "Europe/Lisbon"}).json()
        return {"wind": r["current"]["wind_speed_10m"], "pres": r["current"]["pressure_msl"], "wave": r_m["current"]["wave_height"]}
    except:
        return {"wind": "?", "pres": "?", "wave": "?"}

def get_depth(lat, lon):
    if 38.65 < lat < 38.80 and -9.30 < lon < -9.00: return "10-15 м (Тежу)"
    elif lon < -9.30: return "30-50 м (Океан)"
    return "н/д"

moon_phase = ephem.Moon(datetime.now()).phase
m = folium.Map(location=[38.72, -9.14], zoom_start=11, tiles="Esri WorldImagery")

# Данные для текущей точки
active_data = get_weather(st.session_state.active_lat, st.session_state.active_lon)
active_depth = get_depth(st.session_state.active_lat, st.session_state.active_lon)
active_tooltip = f"<b>Выбранная точка</b><br>Ветер: {active_data['wind']} км/ч<br>Волна: {active_data['wave']} м<br>Давление: {active_data['pres']} гПа<br>Глубина: {active_depth}<br>Луна: {moon_phase:.0f}%"

# Добавляем маркер
folium.Marker(
    [st.session_state.active_lat, st.session_state.active_lon],
    tooltip=folium.Tooltip(active_tooltip, permanent=False),
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# ВНЕДРЯЕМ JAVASCRIPT ДЛЯ ПЕРЕХВАТА КЛИКА
# Это заставит карту работать как в Google Maps без перезагрузки страницы
m.add_child(folium.Element("""
<script>
    var map = document.querySelector('.folium-map');
    // Ждем загрузки карты
    setTimeout(function() {
        // Находим все карты на странице (Leaflet)
        var leafletMap = window[Object.keys(window).find(k => k.startsWith('map_'))];
        if (leafletMap) {
            leafletMap.on('click', function(e) {
                var lat = e.latlng.lat;
                var lng = e.latlng.lng;
                // Отправляем координаты в Streamlit
                window.parent.postMessage({
                    isStreamlitMessage: true,
                    type: "streamlit:setComponentValue",
                    value: {last_clicked: {lat: lat, lng: lng}}
                }, "*");
            });
        }
    }, 1000);
</script>
"""))

map_data = st_folium(m, use_container_width=True, height=600, returned_objects=["last_clicked"])

if map_data.get("last_clicked"):
    st.session_state.active_lat = map_data["last_clicked"]["lat"]
    st.session_state.active_lon = map_data["last_clicked"]["lng"]
    st.rerun()

st.success(f"Текущая точка: {st.session_state.active_lat:.4f}, {st.session_state.active_lon:.4f}")

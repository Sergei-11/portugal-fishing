import json, re, os, shutil, datetime

base = r"C:\fishing"
cat_path = os.path.join(base, "catalog_full.html")

# Бэкап
bak = os.path.join(base, "backups", "GLOBAL_REBUILD_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
os.makedirs(bak, exist_ok=True)
shutil.copyfile(cat_path, os.path.join(bak, "catalog_full.html"))
print("Backup:", bak)

# ==========================================
# 1. ЧИТАЕМ ЧИСТЫЕ ДАННЫЕ ИЗ fish_data.js
# ==========================================
fish_js = open(os.path.join(base, "fish_data.js"), encoding="utf-8").read()
start = fish_js.find("window.FISH_DATA = ")
json_str = fish_js[start + len("window.FISH_DATA = "):].strip()
if json_str.endswith(";"): json_str = json_str[:-1]
data = json.loads(json_str)

# ==========================================
# 2. ГЕНЕРИРУЕМ ИДЕАЛЬНЫЙ HTML ДЛЯ КАЖДОГО ЯЗЫКА
# ==========================================
links = {
    'pt': {'Camarão': 'Camarão+pesca', 'Minhoca': 'Minhoca+pesca', 'Amêijoa': 'Amêijoa+pesca', 'Sardinha': 'Sardinha+pesca', 'Lula': 'Lula+pesca', 'Caranguejo': 'Caranguejo+pesca', 'Polvo': 'Polvo+pesca', 'Choco': 'Choco+pesca'},
    'es': {'Camarón': 'Camarón+pesca', 'Gusano': 'Gusano+pesca', 'Almeja': 'Almeja+pesca', 'Sardina': 'Sardina+pesca', 'Calamar': 'Calamar+pesca', 'Cangrejo': 'Cangrejo+pesca', 'Pulpo': 'Pulpo+pesca', 'Choco': 'Choco+pesca'},
    'en': {'Shrimp': 'Shrimp+fishing', 'Worm': 'Worm+fishing', 'Clam': 'Clam+fishing', 'Sardine': 'Sardine+fishing', 'Squid': 'Squid+fishing', 'Crab': 'Crab+fishing', 'Octopus': 'Octopus+fishing', 'Cuttlefish': 'Cuttlefish+fishing'},
    'ru': {'Креветка': 'Креветка+наживка', 'Червь': 'Червь+наживка', 'Мидия': 'Мидия+наживка', 'Сардина': 'Сардина+наживка', 'Кальмар': 'Кальмар+наживка', 'Краб': 'Краб+наживка', 'Осьминог': 'Осьминог+наживка', 'Каракатица': 'Каракатица+наживка'}
}

labels = {
    'pt': {'title': 'O que pescar', 'gear': 'Equipamento', 'baits': 'Melhores iscas', 'cond': 'Condições de pesca', 'when': 'Quando e porquê', 'swell': 'Onda', 'wind': 'Vento', 'relief': 'Relevo', 'season': 'Época', 'time': 'Hora', 'tide': 'Maré', 'moon': 'Lua', 'tip': 'Importante'},
    'es': {'title': 'Qué pescar', 'gear': 'Equipo', 'baits': 'Mejores cebos', 'cond': 'Condiciones de pesca', 'when': 'Cuándo y por qué', 'swell': 'Oleaje', 'wind': 'Viento', 'relief': 'Relieve', 'season': 'Temporada', 'time': 'Hora', 'tide': 'Marea', 'moon': 'Luna', 'tip': 'Importante'},
    'en': {'title': 'What to catch', 'gear': 'Equipment', 'baits': 'Best baits', 'cond': 'Fishing conditions', 'when': 'When and why', 'swell': 'Swell', 'wind': 'Wind', 'relief': 'Relief', 'season': 'Season', 'time': 'Time', 'tide': 'Tide', 'moon': 'Moon', 'tip': 'Important'},
    'ru': {'title': 'На что ловится', 'gear': 'Снасти', 'baits': 'Лучшие наживки', 'cond': 'Условия ловли', 'when': 'Когда и почему', 'swell': 'Волна', 'wind': 'Ветер', 'relief': 'Рельеф', 'season': 'Сезон', 'time': 'Время', 'tide': 'Прилив', 'moon': 'Луна', 'tip': 'Важно'}
}

def get_val(field, lang):
    if field not in data_ex: return "-"
    val = data_ex[field]
    if isinstance(val, dict): return val.get(lang, val.get('ru', '-'))
    return str(val)

for lang in ['pt', 'es', 'en', 'ru']:
    out_data = {}
    lab = labels[lang]
    
    for fish_id, fish_info in data.items():
        # Собираем наживки со ссылками
        baits_text = get_val('baits', lang)
        baits_html = ""
        for word, query in links[lang].items():
            url = f"https://www.google.com/search?q={query}&tbm=isch"
            # Заменяем слово на ссылку (игнорируя регистр)
            baits_text = re.sub(rf'\b({word})\b', f'<a href="{url}" target="_blank" style="color:#007bff; font-weight:bold; text-decoration:none;">\\1 ↗</a>', baits_text, flags=re.IGNORECASE)
        
        # Собираем идеальный HTML (как в японском блоке)
        html = f"""
        <h3 style="margin-bottom:10px;">🎣 {lab['title']} ({lab['gear']} e {lab['baits'].lower()})</h3>
        <p><b>{lab['gear']}:</b> {get_val('gear', lang)}</p>
        <p><b>{lab['baits']}:</b> {baits_text}</p>
        <h3 style="margin-top:15px; margin-bottom:10px;">🌊 {lab['cond']}</h3>
        <p><b>{lab['swell']}:</b> {get_val('swell', lang)}</p>
        <p><b>{lab['wind']}:</b> {get_val('wind', lang)}</p>
        <p><b>{lab['relief']}:</b> {get_val('relief', lang)}</p>
        <h3 style="margin-top:15px; margin-bottom:10px;">🕒 {lab['when']}</h3>
        <p><b>{lab['season']}:</b> {get_val('season', lang)}</p>
        <p><b>{lab['time']}:</b> {get_val('time', lang)}</p>
        <p><b>{lab['tide']}:</b> {get_val('tide', lang)}</p>
        <p><b>{lab['moon']}:</b> {get_val('moon', lang)}</p>
        <p style="margin-top:10px;"><b>{lab['tip']}:</b> {get_val('tip', lang)}</p>
        """
        out_data[fish_id] = html.strip()

    # Сохраняем в нужный файл
    var_name = f"window.FISH_DETAILS_{lang.upper()}"
    filename = f"fish_details_{lang}.js"
    with open(os.path.join(base, filename), "w", encoding="utf-8") as f:
        f.write(var_name + ' = ' + json.dumps(out_data, ensure_ascii=False) + ';')
    print(f"✅ Сгенерирован файл: {filename}")

# ==========================================
# 3. ЧИСТИМ HTML ОТ ВРЕДНЫХ СКРИПТОВ И ВНЕДРЯЕМ НОВУЮ ЛОГИКУ
# ==========================================
html = open(cat_path, encoding="utf-8").read()

# Удаляем скрипт, который срабатывал через 2 секунды
html = re.sub(r'<script>\s*function applyLinksToCards\(\).*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'setTimeout\(applyLinksToCards.*?\);', '', html)

# Переписываем логику выбора языка
old_logic = r"if \(lang === 'ru'\) \{.*?\} else \{.*?\}"

new_logic = """
        if (lang === 'ru') {
            expPt = (window.FISH_DETAILS_RU && window.FISH_DETAILS_RU[id]) ? window.FISH_DETAILS_RU[id] : '<p>Нет данных</p>';
            expEs = (window.FISH_DETAILS_RU && window.FISH_DETAILS_RU[id]) ? window.FISH_DETAILS_RU[id] : '<p>Нет данных</p>';
        } else if (lang === 'en') {
            expPt = (window.FISH_DETAILS_EN && window.FISH_DETAILS_EN[id]) ? window.FISH_DETAILS_EN[id] : '<p>No data</p>';
            expEs = (window.FISH_DETAILS_EN && window.FISH_DETAILS_EN[id]) ? window.FISH_DETAILS_EN[id] : '<p>No data</p>';
        } else if (lang === 'es') {
            expPt = (window.FISH_DETAILS_ES && window.FISH_DETAILS_ES[id]) ? window.FISH_DETAILS_ES[id] : '<p>Sin datos</p>';
            expEs = (window.FISH_DETAILS_ES && window.FISH_DETAILS_ES[id]) ? window.FISH_DETAILS_ES[id] : '<p>Sin datos</p>';
        } else {
            expPt = (window.FISH_DETAILS_PT && window.FISH_DETAILS_PT[id]) ? window.FISH_DETAILS_PT[id] : '<p>Sem dados</p>';
            expEs = (window.FISH_DETAILS_PT && window.FISH_DETAILS_PT[id]) ? window.FISH_DETAILS_PT[id] : '<p>Sem dados</p>';
        }
"""
if re.search(old_logic, html, flags=re.DOTALL):
    html = re.sub(old_logic, new_logic.strip(), html, flags=re.DOTALL)
else:
    print("⚠️ Не нашли старую логику, вставляем принудительно перед `var card = document.createElement`")
    html = html.replace("var card = document.createElement('div');", new_logic + "\n        var card = document.createElement('div');")

# Сбрасываем кэш
html = re.sub(r'src="(fish_details_[a-z_]+\.js)(\?v=\d+)?"', r'src="\1?v=4444"', html)

# Записываем HTML
open(cat_path, "w", encoding="utf-8").write(html)
print("✅ catalog_full.html обновлен: вредные скрипты удалены, логика языков исправлена.")
print("======================================================")
print("ГОТОВО! Теперь текст будет идеальным на всех 4 языках, с переносами строк и ссылками.")

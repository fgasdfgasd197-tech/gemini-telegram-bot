import json
from countryinfo import CountryInfo

country_data = []

print("=== Davlatlar haqida ma'lumot to'plash dasturi ===")
print("Dasturni to'xtatish uchun 'stop' deb yozing.\n")

while True:
    country_name = input("Davlat nomini kiriting: ").strip()
    
    if country_name.lower() == "stop":
        print("Dastur to'xtatildi!")
        with open("information.json", mode='w', encoding='utf-8') as file:
            json.dump(country_data, file, indent=4, ensure_ascii=False)
        print("Ma'lumotlar 'information.json' fayliga muvaffaqiyatli saqlandi.")
        break

    try:
        get_country = CountryInfo(country_name)
        data = get_country.info()

        name = data.get('name', country_name)
        area = data.get('area', "Ma'lumot yo'q")
        borders = data.get('borders', [])
        capital = data.get('capital', "Ma'lumot yo'q")
        currencies = data.get('currencies', [])
        region = data.get('region', "Ma'lumot yo'q")
        languages = data.get('languages', [])
        timezones = data.get('timezones', [])
        population = data.get('population', "Ma'lumot yo'q")

        print(f"\n📍 {name} davlati haqida ma'lumot:")
        print(f"• Qit'a: {region}")
        print(f"• Maydoni: {area} km²")
        print(f"• Chegaralari: {', '.join(borders) if borders else 'Yoq'}")
        print(f"• Poytaxti: {capital}")
        print(f"• Pul birligi: {', '.join(currencies)}")
        print(f"• Tillari: {', '.join(languages)}")
        print(f"• Vaqt mintaqalari: {', '.join(timezones)}")
        print(f"• Aholisi: {population} kishi\n")

        country_data.append({
            'name': name,
            'region': region,
            'area': area,
            'borders': borders,
            'capital': capital,
            'currencies': currencies,
            'languages': languages,
            'timezones': timezones,
            'population': population,
        })

    except Exception:
        print("⚠️ Siz davlat nomini noto'g'ri kiritdingiz yoki ma'lumot topilmadi!\n")

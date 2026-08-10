import json
from countryinfo import CountryInfo
# 50 ta davlat va ularning milliy salomlashuv iboralari






countries_data = [
    {"name": "Uzbekistan", "greeting": "Assalomu alaykum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "China", "greeting": "Nǐ hǎo (你好)", "meaning": "Salom"},
    {"name": "India", "greeting": "Namaste (नमस्ते)", "meaning": "Sizga ta'zim qilaman"},
    {"name": "United States", "greeting": "Hello / Hi", "meaning": "Salom"},
    {"name": "Indonesia", "greeting": "Halo / Selamat", "meaning": "Salom / Xayrli kun"},
    {"name": "Pakistan", "greeting": "Assalam-o-Alaikum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "Brazil", "greeting": "Olá / Oi", "meaning": "Salom"},
    {"name": "Nigeria", "greeting": "Hello / Bawo", "meaning": "Salom / Qandaysiz"},
    {"name": "Bangladesh", "greeting": "Assalamu Alaikum / Namaskar", "meaning": "Tinchlik / Salom"},
    {"name": "Russia", "greeting": "Zdravstvuyte (Здравствуйте)", "meaning": "Sog'lik tilayman / Salom"},
    {"name": "Mexico", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Japan", "greeting": "Konnichiwa (こんにちは)", "meaning": "Xayrli kun"},
    {"name": "Ethiopia", "greeting": "Tadiyas (ታዲያስ)", "meaning": "Nima gap / Salom"},
    {"name": "Philippines", "greeting": "Kamusta", "meaning": "Qandaysiz"},
    {"name": "Egypt", "greeting": "Ahlan wa Sahlan", "meaning": "Xush kelibsiz / Salom"},
    {"name": "Vietnam", "greeting": "Xin chào", "meaning": "Salom"},
    {"name": "Iran", "greeting": "Salam (سلام)", "meaning": "Salom"},
    {"name": "Turkey", "greeting": "Merhaba", "meaning": "Salom"},
    {"name": "Germany", "greeting": "Hallo / Guten Tag", "meaning": "Salom / Xayrli kun"},
    {"name": "Thailand", "greeting": "Sawatdee (สวัสดี)", "meaning": "Salom"},
    {"name": "United Kingdom", "greeting": "Hello / Good day", "meaning": "Salom / Xayrli kun"},
    {"name": "Tanzania", "greeting": "Jambo / Habari", "meaning": "Salom / Nima gap"},
    {"name": "France", "greeting": "Bonjour / Salut", "meaning": "Xayrli kun / Salom"},
    {"name": "South Africa", "greeting": "Howzit / Sawubona", "meaning": "Qandaysiz / Sizni ko'rib turganimdan xursandman"},
    {"name": "Italy", "greeting": "Ciao / Salve", "meaning": "Salom"},
    {"name": "Kenya", "greeting": "Jambo", "meaning": "Salom"},
    {"name": "Myanmar", "greeting": "Mingalaba", "meaning": "Ezgulik tilayman"},
    {"name": "Colombia", "greeting": "Hola", "meaning": "Salom"},
    {"name": "South Korea", "greeting": "Annyeonghaseyo (안녕하세요)", "meaning": "Tinchlikdamisiz / Salom"},
    {"name": "Uganda", "greeting": "Oli otya", "meaning": "Qandaysiz"},
    {"name": "Sudan", "greeting": "Salam Alaykum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "Spain", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Argentina", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Algeria", "greeting": "Salam", "meaning": "Salom"},
    {"name": "Iraq", "greeting": "Marhaba", "meaning": "Salom"},
    {"name": "Afghanistan", "greeting": "Salam", "meaning": "Salom"},
    {"name": "Poland", "greeting": "Cześć / Dzień dobry", "meaning": "Salom / Xayrli kun"},
    {"name": "Canada", "greeting": "Hello / Bonjour", "meaning": "Salom / Xayrli kun"},
    {"name": "Morocco", "greeting": "Salam Alaykum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "Saudi Arabia", "greeting": "Marhaban / As-salamu 'alaykum", "meaning": "Xush kelibsiz / Tinchlik bo'lsin"},
    {"name": "Ukraine", "greeting": "Pryvit (Привіт)", "meaning": "Salom"},
    {"name": "Angola", "greeting": "Olá", "meaning": "Salom"},
    {"name": "Yemen", "greeting": "Salam", "meaning": "Salom"},
    {"name": "Peru", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Malaysia", "greeting": "Selamat pagi / Helo", "meaning": "Xayrli tong / Salom"},
    {"name": "Ghana", "greeting": "Eti sen", "meaning": "Ahvollar qanday"},
    {"name": "Mozambique", "greeting": "Olá", "meaning": "Salom"},
    {"name": "Australia", "greeting": "G'day / Hello", "meaning": "Xayrli kun / Salom"},
    {"name": "Madagascar", "greeting": "Salama", "meaning": "Salom"},
    {"name": "Kazakhstan", "greeting": "Sälemetsiz be (Сəлеметсіз бе)", "meaning": "Salom / Assalomu alaykum"}
]

country_data = []

print("=== 50 TA DAVLAT HAQIDA MA'LUMOT TO'PLASH DASTURI ===\n")

for idx, item in enumerate(countries_data, start=1):
    country_name = item["name"]
    greeting = item["greeting"]
    meaning = item["meaning"]

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

        # Aholi sonini formatlash (masalan: 34,232,050)
        formatted_pop = f"{population:,}" if isinstance(population, int) else population

        print(f"📍 [{idx}/50] {name} davlati haqida ma'lumot:")
        print(f"• Qit'a: {region}")
        print(f"• Maydoni: {area} km²")
        print(f"• Chegaralari: {', '.join(borders) if borders else 'Yoq'}")
        print(f"• Poytaxti: {capital}")
        print(f"• Pul birligi: {', '.join(currencies)}")
        print(f"• Tillari: {', '.join(languages)}")
        print(f"• Vaqt mintaqalari: {', '.join(timezones)}")
        print(f"• Aholisi: {formatted_pop} kishi")
        print(f"• 💬 Salomlashuvi: \"{greeting}\" (Ma'nosi: {meaning})\n" + "-"*50 + "\n")

        country_data.append({
            'tartib': idx,
            'name': name,
            'region': region,
            'area': area,
            'borders': borders,
            'capital': capital,
            'currencies': currencies,
            'languages': languages,
            'timezones': timezones,
            'population': population,
            'salomlashuv': greeting,
            'salomlashuv_manosi': meaning
        })

    except Exception:
        print(f"⚠️ [{idx}/50] {country_name} haqida ma'lumot topilmadi!\n")

# Ma'lumotlarni JSON fayliga saqlash
with open("information.json", mode='w', encoding='utf-8') as file:
    json.dump(country_data, file, indent=4, ensure_ascii=False)

print("="*50)
print("✅ Barcha 50 ta davlat haqidagi ma'lumotlar 'information.json' fayliga saqlandi!")
print("😊 Dastur ishini yakunladi. E'tiboringiz uchun rahmat va xayr!")
print("="*50)

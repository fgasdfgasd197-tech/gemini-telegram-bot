import json
from countryinfo import CountryInfo

# 50 ta davlat va ularning milliy salomlashuv iboralari
# 'search_name' — CountryInfo kutubxonasi to'g'ri topishi uchun ishlatiladi
countries_data = [
    {"name": "Uzbekistan", "search_name": "Uzbekistan", "greeting": "Assalomu alaykum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "China", "search_name": "China", "greeting": "Nǐ hǎo (你好)", "meaning": "Salom"},
    {"name": "India", "search_name": "India", "greeting": "Namaste (नमस्ते)", "meaning": "Sizga ta'zim qilaman"},
    {"name": "United States", "search_name": "USA", "greeting": "Hello / Hi", "meaning": "Salom"},
    {"name": "Indonesia", "search_name": "Indonesia", "greeting": "Halo / Selamat", "meaning": "Salom / Xayrli kun"},
    {"name": "Pakistan", "search_name": "Pakistan", "greeting": "Assalam-o-Alaikum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "Brazil", "search_name": "Brazil", "greeting": "Olá / Oi", "meaning": "Salom"},
    {"name": "Nigeria", "search_name": "Nigeria", "greeting": "Hello / Bawo", "meaning": "Salom / Qandaysiz"},
    {"name": "Bangladesh", "search_name": "Bangladesh", "greeting": "Assalamu Alaikum / Namaskar", "meaning": "Tinchlik / Salom"},
    {"name": "Russia", "search_name": "Russia", "greeting": "Zdravstvuyte (Здравствуйте)", "meaning": "Sog'lik tilayman / Salom"},
    {"name": "Mexico", "search_name": "Mexico", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Japan", "search_name": "Japan", "greeting": "Konnichiwa (こんにちは)", "meaning": "Xayrli kun"},
    {"name": "Ethiopia", "search_name": "Ethiopia", "greeting": "Tadiyas (ታዲያስ)", "meaning": "Nima gap / Salom"},
    {"name": "Philippines", "search_name": "Philippines", "greeting": "Kamusta", "meaning": "Qandaysiz"},
    {"name": "Egypt", "search_name": "Egypt", "greeting": "Ahlan wa Sahlan", "meaning": "Xush kelibsiz / Salom"},
    {"name": "Vietnam", "search_name": "Vietnam", "greeting": "Xin chào", "meaning": "Salom"},
    {"name": "Iran", "search_name": "Iran", "greeting": "Salam (سلام)", "meaning": "Salom"},
    {"name": "Turkey", "search_name": "Turkey", "greeting": "Merhaba", "meaning": "Salom"},
    {"name": "Germany", "search_name": "Germany", "greeting": "Hallo / Guten Tag", "meaning": "Salom / Xayrli kun"},
    {"name": "Thailand", "search_name": "Thailand", "greeting": "Sawatdee (สวัสดี)", "meaning": "Salom"},
    {"name": "United Kingdom", "search_name": "Great Britain", "greeting": "Hello / Good day", "meaning": "Salom / Xayrli kun"},
    {"name": "Tanzania", "search_name": "Tanzania", "greeting": "Jambo / Habari", "meaning": "Salom / Nima gap"},
    {"name": "France", "search_name": "France", "greeting": "Bonjour / Salut", "meaning": "Xayrli kun / Salom"},
    {"name": "South Africa", "search_name": "South Africa", "greeting": "Howzit / Sawubona", "meaning": "Qandaysiz / Sizni ko'rib turganimdan xursandman"},
    {"name": "Italy", "search_name": "Italy", "greeting": "Ciao / Salve", "meaning": "Salom"},
    {"name": "Kenya", "search_name": "Kenya", "greeting": "Jambo", "meaning": "Salom"},
    {"name": "Myanmar", "search_name": "Myanmar", "greeting": "Mingalaba", "meaning": "Ezgulik tilayman"},
    {"name": "Colombia", "search_name": "Colombia", "greeting": "Hola", "meaning": "Salom"},
    {"name": "South Korea", "search_name": "Korea", "greeting": "Annyeonghaseyo (안녕하세요)", "meaning": "Tinchlikdamisiz / Salom"},
    {"name": "Uganda", "search_name": "Uganda", "greeting": "Oli otya", "meaning": "Qandaysiz"},
    {"name": "Sudan", "search_name": "Sudan", "greeting": "Salam Alaykum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "Spain", "search_name": "Spain", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Argentina", "search_name": "Argentina", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Algeria", "search_name": "Algeria", "greeting": "Salam", "meaning": "Salom"},
    {"name": "Iraq", "search_name": "Iraq", "greeting": "Marhaba", "meaning": "Salom"},
    {"name": "Afghanistan", "search_name": "Afghanistan", "greeting": "Salam", "meaning": "Salom"},
    {"name": "Poland", "search_name": "Poland", "greeting": "Cześć / Dzień dobry", "meaning": "Salom / Xayrli kun"},
    {"name": "Canada", "search_name": "Canada", "greeting": "Hello / Bonjour", "meaning": "Salom / Xayrli kun"},
    {"name": "Morocco", "search_name": "Morocco", "greeting": "Salam Alaykum", "meaning": "Sizga tinchlik bo'lsin"},
    {"name": "Saudi Arabia", "search_name": "Saudi Arabia", "greeting": "Marhaban / As-salamu 'alaykum", "meaning": "Xush kelibsiz / Tinchlik bo'lsin"},
    {"name": "Ukraine", "search_name": "Ukraine", "greeting": "Pryvit (Привіт)", "meaning": "Salom"},
    {"name": "Angola", "search_name": "Angola", "greeting": "Olá", "meaning": "Salom"},
    {"name": "Yemen", "search_name": "Yemen", "greeting": "Salam", "meaning": "Salom"},
    {"name": "Peru", "search_name": "Peru", "greeting": "Hola", "meaning": "Salom"},
    {"name": "Malaysia", "search_name": "Malaysia", "greeting": "Selamat pagi / Helo", "meaning": "Xayrli tong / Salom"},
    {"name": "Ghana", "search_name": "Ghana", "greeting": "Eti sen", "meaning": "Ahvollar qanday"},
    {"name": "Mozambique", "search_name": "Mozambique", "greeting": "Olá", "meaning": "Salom"},
    {"name": "Australia", "search_name": "Australia", "greeting": "G'day / Hello", "meaning": "Xayrli kun / Salom"},
    {"name": "Madagascar", "search_name": "Madagascar", "greeting": "Salama", "meaning": "Salom"},
    {"name": "Kazakhstan", "search_name": "Kazakhstan", "greeting": "Sälemetsiz be (Сəлеметсіз бе)", "meaning": "Salom / Assalomu alaykum"}
]

country_data = []

print("=== 50 TA DAVLAT HAQIDA MA'LUMOT TO'PLASH DASTURI ===\n")

for idx, item in enumerate(countries_data, start=1):
    country_name = item["name"]
    search_name = item["search_name"]
    greeting = item["greeting"]
    meaning = item["meaning"]

    try:
        get_country = CountryInfo(search_name)
        data = get_country.info()

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

        print(f"📍 [{idx}/50] {country_name} davlati haqida ma'lumot:")
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
            'name': country_name,
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

    except Exception as e:
        print(f"⚠️ [{idx}/50] {country_name} haqida ma'lumot topilmadi! Xatolik: {e}\n")

# Ma'lumotlarni JSON fayliga saqlash
with open("information.json", mode='w', encoding='utf-8') as file:
    json.dump(country_data, file, indent=4, ensure_ascii=False)

print("="*50)
print("✅ Barcha 50 ta davlat haqidagi ma'lumotlar 'information.json' fayliga saqlandi!")
print("😊 Dastur ishini yakunladi.")
print("="*50)

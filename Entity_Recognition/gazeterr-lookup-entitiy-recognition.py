# Daftar entity (dictionary / gazetteer)
cities = ["Jakarta", "Bandung", "Surabaya"]
universities = ["Universitas Indonesia", "University of Indonesia", "Institut Teknologi Bandung", "Universitas Gadjah Mada"]
programs = ["Informatika", "Kedokteran", "Hukum"]

# Contoh teks input

texts = [
"Contact me at john.doe@gmail.com or call +1-202-555-0147 on 12/06/2025. My website is https://example.com.",
"My name is Ahmad Putra. You can contact me at andi@gmail.com or call me at +628123456789.I want to apply for Informatics at University of Indonesia.The exam will be held on 12/06/2025 and the fee is Rp 500.000.",
"Saya ingin mendaftar di Universitas Indonesia jurusan Informatika, tapi saya tinggal di Bandung."
]



# Fungsi Entity Recognition berbasis dictionary
def dictionary_entity_recognition(text, cities, universities, programs):
    entities = []

    for city in cities:
        if city in text:
            entities.append({"entity": "CITY", "value": city})
    for univ in universities:
        if univ in text:
            entities.append({"entity": "UNIVERSITY", "value": univ})
    for prog in programs:
        if prog in text:
            entities.append({"entity": "PROGRAM", "value": prog})

    return entities

# ============= Jalankan

for text in texts:
    entities = dictionary_entity_recognition(text, cities, universities, programs)

    # Tampilkan hasil
    print("Original Text:", text)
    print("\nRecognized Entities:")
    for ent in entities:
        print(f"- {ent['entity']}: {ent['value']}")
    print ()




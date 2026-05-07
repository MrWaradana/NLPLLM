import re

# Contoh teks
texts = [
"Contact me at john.doe@gmail.com or call +1-202-555-0147 on 12/06/2025. My website is https://example.com.",
"My name is Ahmad Putra. You can contact me at andi@gmail.com or call me at +628123456789.I want to apply for Informatics at University of Indonesia.The exam will be held on 12/06/2025 and the fee is Rp 500.000."
]

# Kumpulan pola regex untuk entity
patterns = {
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "PHONE": r"\+?\d[\d -]{8,}\d",
    "DATE": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "URL": r"https?:\/\/[^\s]+",
}

# Fungsi Entity Recognition dengan Regex
def regex_entity_recognition(text, patterns):
    entities = []
    for label, pattern in patterns.items():
        matches = re.findall(pattern, text)
        for match in matches:
            entities.append({"entity": label, "value": match})
    return entities

# ============== Jalankan ER

for text in texts:
    entities = regex_entity_recognition(text, patterns)

    # Tampilkan hasil
    print("Original Text:", text)
    print("\nRecognized Entities:")
    for ent in entities:
        print(f"- {ent['entity']}: {ent['value']}")
    print ()

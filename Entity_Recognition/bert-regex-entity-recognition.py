from transformers import pipeline
import re

def hybrid_entity_recognition(text):
    # 1. BERT-based NER
    ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
    bert_entities = ner_pipeline(text)

    # Standardisasi key dari BERT ke format seragam
    standardized_bert_entities = [
        {
            "entity": ent["entity_group"],
            "word": ent["word"],
            "score": ent["score"],
            "start": ent["start"],
            "end": ent["end"],
        }
        for ent in bert_entities
    ]

    # 2. Regex-based NER
    regex_patterns = {
        "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "PHONE": r"\+?\d{1,3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{4}",
        "DATE": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        "URL": r"https?://[^\s]+",
    }

    regex_entities = []
    for label, pattern in regex_patterns.items():
        for match in re.finditer(pattern, text):
            regex_entities.append({
                "entity": label,
                "word": match.group(),
                "score": 1.0,   # Regex tidak pakai probabilitas
                "start": match.start(),
                "end": match.end(),
            })

    # 3. Gabungkan hasil BERT + Regex
    all_entities = standardized_bert_entities + regex_entities

    return all_entities


# ==== Contoh Pemakaian ====

texts = [
"My name is John Doe, contact me at john.doe@gmail.com or call +1-202-555-0147 on 12/06/2025. My website is https://example.com. Meet Alice at Google HQ around 10.15 AM before lunch.",
"My name is Ahmad Putra. You can contact me at andi@gmail.com or call me at +628123456789.I want to apply for Informatics at University of Indonesia.The exam will be held on 12/06/2025 and the fee is Rp 500.000.",
"Saya ingin mendaftar di Universitas Indonesia jurusan Informatika, tapi saya tinggal di Bandung."
]

for text in texts:
    entities = hybrid_entity_recognition(text)

    for ent in entities:
        print(f"{ent['word']:<30} --> {ent['entity']} (start={ent['start']}, end={ent['end']})")
    print ()



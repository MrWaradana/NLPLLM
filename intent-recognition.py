import torch
from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)

# ========= 1. Dataset Percakapan Intent =========
data = {
    "text": [
        "Hai", "Halo", "Selamat pagi",
        "Siapa namamu?", "Kamu siapa?",
        "Terima kasih", "Thanks", "Makasih",
        "Tolong bantu saya", "Saya butuh bantuan"
    ],
    "label": [
        "greeting", "greeting", "greeting",
        "ask_name", "ask_name",
        "thanks", "thanks", "thanks",
        "help", "help"
    ]
}

# ========= 2. Encode Label & Dataset =========
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data["label_enc"] = le.fit_transform(data["label"])

dataset = Dataset.from_dict({
    "text": data["text"],
    "label": data["label_enc"]
}).train_test_split(test_size=0.2)

# ========= 3. Tokenisasi =========
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
dataset = dataset.map(lambda x: tokenizer(x["text"], padding=True, truncation=True), batched=True)

# ========= 4. Load Model & Fine-tuning =========
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=len(le.classes_)
)

training_args = TrainingArguments(
    output_dir="./intent-model",
    num_train_epochs=50,
    per_device_train_batch_size=4,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="no",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

trainer.train()

# ========= 5. Inference / Chatbot =========
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

responses = {
    "greeting": "Halo juga! Senang bertemu denganmu.",
    "ask_name": "Saya adalah asisten AI sederhana berbasis DistilBERT.",
    "thanks": "Sama-sama! Senang bisa membantu.",
    "help": "Tentu, beri tahu apa yang kamu butuhkan."
}

print("\n🤖 Chatbot aktif! Ketik 'exit' untuk berhenti.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: See you later!")
        break

    inputs = tokenizer(user_input, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model(**inputs)
        pred = output.logits.argmax(dim=-1).item()
    
    intent = le.inverse_transform([pred])[0]
    print("Bot:", responses.get(intent, "Maaf, saya tidak mengerti maksudmu."))


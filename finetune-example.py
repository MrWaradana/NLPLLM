from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
import pickle

model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# --- Penting: set pad_token ke eos_token ---
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

# Dataset contoh (pakai dataset besar untuk hasil nyata)
train_data = [
    {"input": "Halo", "response": "Hai, ada yang bisa saya bantu?"},
    {"input": "Siapa kamu?", "response": "Saya chatbot yang dibuat untuk membantu Anda."},
    {"input": "Apa hobimu?", "response": "Saya suka ngobrol dengan manusia!"},
]

# with open("airdialog_train.pkl", "rb") as f:
#     train_data = pickle.load(f)

print("Jumlah pasangan data:", len(train_data))
print("Contoh:", train_data[:3])


raw_ds = Dataset.from_list(train_data)

# Tokenisasi + buat labels; padding aktif & label pad -> -100
def encode_batch(batch):
    enc_inp  = tokenizer(batch["input"],   padding="max_length", truncation=True, max_length=64)
    enc_out  = tokenizer(batch["response"], padding="max_length", truncation=True, max_length=64)

    labels = []
    for ids in enc_out["input_ids"]:
        labels.append([(-100 if t == tokenizer.pad_token_id else t) for t in ids])

    enc_inp["labels"] = labels
    return enc_inp

ds = raw_ds.map(encode_batch, batched=True, remove_columns=raw_ds.column_names)

args = TrainingArguments(
    output_dir="./airdialogpt-finetuned",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=200,
    save_total_limit=2,
    # evaluation_strategy="no",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=ds,
    # tidak perlu data collator khusus karena kita sudah pad ke max_length
)

trainer.train()
trainer.save_model("./airdialogpt-finetuned")
tokenizer.save_pretrained("./airdialogpt-finetuned")

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model yang sudah fine-tuned untuk dialog
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Simulasi percakapan sederhana
chat_history_ids = None


mytext = [
"Hi, how are you?",
"I’m studying AI, can you help me?",
"Who are you?"
]

for step in range(3):
    user_input = mytext[step]  #input("User: ")
    print (f"User: {user_input}")   
    
    # Encode user input + history
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = (
        torch.cat([chat_history_ids, new_input_ids], dim=-1)
        if chat_history_ids is not None else new_input_ids
    )

    # Generate jawaban dari bot
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )

    # Decode jawaban terakhir
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    print(f"Bot: {bot_response}")



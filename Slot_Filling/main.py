# Definisi state
STATE_START = "START"
STATE_TANYA_TUJUAN = "TANYA_TUJUAN"
STATE_TANYA_TANGGAL = "TANYA_TANGGAL"
STATE_TANYA_PENUMPANG = "TANYA_PENUMPANG"
STATE_KONFIRMASI = "KONFIRMASI"
STATE_SELESAI = "SELESAI"

# Inisialisasi variabel
state = STATE_START
slots = {"tujuan": None, "tanggal": None, "penumpang": None}

def chatbot(user_input):
    global state, slots

    if state == STATE_START:
        state = STATE_TANYA_TUJUAN
        return "Halo! Mau pesan tiket ke mana?"

    elif state == STATE_TANYA_TUJUAN:
        slots["tujuan"] = user_input
        state = STATE_TANYA_TANGGAL
        return f"Baik, ke {slots['tujuan']}. Kapan tanggal berangkatnya?"

    elif state == STATE_TANYA_TANGGAL:
        slots["tanggal"] = user_input
        state = STATE_TANYA_PENUMPANG
        return "Untuk berapa orang?"

    elif state == STATE_TANYA_PENUMPANG:
        slots["penumpang"] = user_input
        state = STATE_KONFIRMASI
        return (f"Konfirmasi: tiket ke {slots['tujuan']} pada {slots['tanggal']} "
                f"untuk {slots['penumpang']} orang. Benar? (ya/tidak)")

    elif state == STATE_KONFIRMASI:
        if user_input.lower() in ["ya", "betul", "oke"]:
            state = STATE_SELESAI
            return "Pesanan tiket Anda sudah dicatat. Terima kasih!"
        else:
            # Reset untuk ulangi
            slots = {"tujuan": None, "tanggal": None, "penumpang": None}
            state = STATE_TANYA_TUJUAN
            return "Baik, mari kita ulangi. Mau pesan tiket ke mana?"

    elif state == STATE_SELESAI:
        return "Percakapan selesai. Sampai jumpa!"

# --- Simulasi Percakapan ---
if __name__ == "__main__":
    print("Ketik 'exit' untuk keluar.\n")
    while True:
        user = input("User: ")
        if user.lower() == "exit":
            break
        bot = chatbot(user)
        print("Bot :", bot)


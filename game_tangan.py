import cv2
import mediapipe as mp
import time
import random

# --- KONFIGURASI MEDIAPIPE ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

LIST_GERAKAN = ["BATU", "KERTAS", "PEACE", "SATU"]

# --- VARIABEL GLOBAL ---
state = "MENU"
skor = 0
waktu_main = 60
mulai_waktu = 0
target_sekarang = ""
pesan_status = ""
warna_status = (255, 255, 255)

# Variabel untuk menyimpan ukuran layar tombol (agar bisa diklik)
btn_x1, btn_y1, btn_x2, btn_y2 = 0, 0, 0, 0

# --- FUNGSI DETEKSI JARI ---
def hitung_jari(hand_landmarks):
    jari_terbuka = []
    tips_ids = [8, 12, 16, 20] # Telunjuk s/d Kelingking
    
    # Cek 4 jari
    for tip_id in tips_ids:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            jari_terbuka.append(1)
        else:
            jari_terbuka.append(0)
    
    total = sum(jari_terbuka)
    if total == 0: return "BATU"
    elif total == 4: return "KERTAS"
    elif total == 2: return "PEACE"
    elif total == 1: return "SATU"
    else: return "..."

# --- FUNGSI MOUSE CLICK ---
def mouse_click(event, x, y, flags, param):
    global state, skor, mulai_waktu, target_sekarang, btn_x1, btn_y1, btn_x2, btn_y2
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Cek apakah klik berada di dalam area tombol
        if btn_x1 < x < btn_x2 and btn_y1 < y < btn_y2:
            if state == "MENU":
                print("Game Dimulai!")
                reset_game()
                state = "MAIN"
            elif state == "GAMEOVER":
                print("Game Diulangi!")
                reset_game()
                state = "MAIN"

def reset_game():
    global skor, mulai_waktu, target_sekarang, pesan_status
    skor = 0
    mulai_waktu = time.time()
    target_sekarang = random.choice(LIST_GERAKAN)
    pesan_status = "SIAP..."

# --- SETUP WINDOW FULLSCREEN ---
window_name = "Game Refleks Jari Fullscreen"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback(window_name, mouse_click)

# Buka Kamera
cap = cv2.VideoCapture(0)

# Coba set resolusi ke HD (1280x720) agar tajam di fullscreen
# Jika kamera tidak support, dia akan pakai resolusi default
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Tekan 'q' untuk keluar dari Fullscreen/Program.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Balik gambar & ubah warna
    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Dapatkan ukuran layar aktual
    height, width, _ = frame.shape
    center_x = width // 2
    center_y = height // 2

    # ==========================================
    # LOGIKA: HALAMAN MENU
    # ==========================================
    if state == "MENU":
        # Gelapkan layar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

        # Judul Besar
        judul = "GAME REFLEKS JARI"
        ukuran_font = 2.0
        (text_w, text_h), _ = cv2.getTextSize(judul, cv2.FONT_HERSHEY_SIMPLEX, ukuran_font, 3)
        cv2.putText(frame, judul, (center_x - text_w // 2, center_y - 100), cv2.FONT_HERSHEY_SIMPLEX, ukuran_font, (0, 255, 255), 4)
        
        # Tombol MULAI (Dinamis di Tengah)
        btn_w, btn_h = 300, 100
        btn_x1 = center_x - btn_w // 2
        btn_y1 = center_y
        btn_x2 = center_x + btn_w // 2
        btn_y2 = center_y + btn_h
        
        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (0, 200, 0), -1) # Hijau
        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (255, 255, 255), 3) # Border Putih
        
        text_btn = "MULAI"
        (t_w, t_h), _ = cv2.getTextSize(text_btn, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
        cv2.putText(frame, text_btn, (center_x - t_w // 2, center_y + 65), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # ==========================================
    # LOGIKA: HALAMAN MAIN (GAMEPLAY)
    # ==========================================
    elif state == "MAIN":
        # Hitung waktu
        waktu_berjalan = time.time() - mulai_waktu
        sisa_waktu = int(waktu_main - waktu_berjalan)

        if sisa_waktu <= 0:
            state = "GAMEOVER"
        
        # --- TAMPILAN WAKTU (BESAR DI ATAS) ---
        # Warna berubah merah jika waktu < 10 detik
        warna_waktu = (0, 255, 0) if sisa_waktu > 10 else (0, 0, 255)
        
        # Background Waktu (Semi transparan hitam di atas)
        cv2.rectangle(frame, (center_x - 100, 0), (center_x + 100, 80), (0,0,0), -1)
        
        text_waktu = f"{sisa_waktu}"
        (tw, th), _ = cv2.getTextSize(text_waktu, cv2.FONT_HERSHEY_SIMPLEX, 2, 5)
        # Tampilkan angka waktu besar di tengah atas
        cv2.putText(frame, text_waktu, (center_x - tw // 2, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, warna_waktu, 5)
        
        # Proses MediaPipe
        results = hands.process(img_rgb)
        gerakan_user = "..."
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gerakan_user = hitung_jari(hand_landmarks)

                # Cek Jawaban
                if gerakan_user == target_sekarang:
                    skor += 10
                    pesan_status = "BENAR! +10"
                    warna_status = (0, 255, 0)
                    temp_list = list(LIST_GERAKAN)
                    if target_sekarang in temp_list: temp_list.remove(target_sekarang)
                    target_sekarang = random.choice(temp_list) if temp_list else "BATU"
                else:
                    pesan_status = "SALAH..."
                    warna_status = (0, 0, 255)

        # UI Game (HUD)
        # Kotak info kiri atas
        cv2.rectangle(frame, (20, 20), (350, 150), (50, 50, 50), -1)
        cv2.putText(frame, f"TARGET:", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        cv2.putText(frame, f"{target_sekarang}", (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)
        
        # Kotak skor kanan atas
        cv2.rectangle(frame, (width - 250, 20), (width - 20, 100), (50, 50, 50), -1)
        cv2.putText(frame, f"SKOR: {skor}", (width - 230, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Teks Status Deteksi (Bawah)
        cv2.putText(frame, f"Deteksi: {gerakan_user}", (50, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, pesan_status, (center_x - 100, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, warna_status, 2)

    # ==========================================
    # LOGIKA: HALAMAN GAME OVER
    # ==========================================
    elif state == "GAMEOVER":
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.8, frame, 0.2, 0)
        
        cv2.putText(frame, "WAKTU HABIS!", (center_x - 200, center_y - 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        
        text_skor = f"SKOR AKHIR: {skor}"
        (ts, th), _ = cv2.getTextSize(text_skor, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
        cv2.putText(frame, text_skor, (center_x - ts // 2, center_y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
        
        # Tombol ULANGI (Dinamis di Tengah)
        btn_w, btn_h = 300, 100
        btn_x1 = center_x - btn_w // 2
        btn_y1 = center_y + 50
        btn_x2 = center_x + btn_w // 2
        btn_y2 = center_y + 50 + btn_h
        
        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (255, 0, 0), -1) # Biru
        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (255, 255, 255), 3)
        
        text_btn = "ULANGI"
        (t_w, t_h), _ = cv2.getTextSize(text_btn, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
        cv2.putText(frame, text_btn, (center_x - t_w // 2, center_y + 115), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    cv2.imshow(window_name, frame)
    
    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
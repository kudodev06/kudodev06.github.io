import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import webbrowser

# Khởi tạo pygame mixer và hệ thống video để xử lý sự kiện
pygame.mixer.init()
pygame.display.init()

# Biến kiểm soát lặp lại
is_repeating = False

# Biến kiểm soát ngôn ngữ (mặc định là Tiếng Việt)
current_language = 'vi'

# Từ điển chứa các văn bản cho các ngôn ngữ
language_texts = {
    'vi': {
        'choose_directory': 'Chọn thư mục',
        'play': 'Phát',
        'stop': 'Dừng',
        'repeat': 'Lặp lại',
        'volume': 'Âm lượng: {}',
        'no_song': 'Chưa có bài hát nào được chọn',
        'copyright': '© 2024 kudomp3.',
        'version': 'Version beta-0.0.2',
        'website': 'Website',
        'github': 'GitHub'
    },
    'en': {
        'choose_directory': 'Choose Directory',
        'play': 'Play',
        'stop': 'Stop',
        'repeat': 'Repeat',
        'volume': 'Volume: {}',
        'no_song': 'No song selected',
        'copyright': '© 2024 kudomp3.',
        'version': 'Version beta-0.0.2',
        'website': 'Website',
        'github': 'GitHub'
    }
}

# Hàm cập nhật giao diện theo ngôn ngữ
def update_language():
    choose_button.config(text=language_texts[current_language]['choose_directory'])
    play_button.config(text=language_texts[current_language]['play'])
    stop_button.config(text=language_texts[current_language]['stop'])
    repeat_button.config(text=language_texts[current_language]['repeat'])
    volume_label.config(text=language_texts[current_language]['volume'].format(volume_scale.get()))
    song_label.config(text=language_texts[current_language]['no_song'])
    website_button.config(text=language_texts[current_language]['website'])
    github_button.config(text=language_texts[current_language]['github'])
    copyright_label.config(text=language_texts[current_language]['copyright'])
    version_label.config(text=language_texts[current_language]['version'])

# Hàm chọn thư mục chứa nhạc
def choose_directory():
    directory = filedialog.askdirectory()
    if directory:
        load_songs(directory)

# Hàm tải các bài hát trong thư mục
def load_songs(directory):
    song_list.delete(0, tk.END)
    global song_paths
    song_paths = []
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            song_list.insert(tk.END, filename)
            song_paths.append(os.path.join(directory, filename))

# Hàm phát nhạc
def play_music():
    selected_song = song_list.curselection()
    if selected_song:
        song_path = song_paths[selected_song[0]]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        song_label.config(text=f"{'Đang phát: ' if current_language == 'vi' else 'Playing: '}{os.path.basename(song_path)}")

# Hàm dừng nhạc
def stop_music():
    pygame.mixer.music.stop()

# Hàm điều chỉnh âm lượng
def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)
    volume_label.config(text=language_texts[current_language]['volume'].format(int(val)))

# Hàm lặp lại bài hát
def toggle_repeat():
    global is_repeating
    is_repeating = not is_repeating
    repeat_button.config(bg='#28a745' if is_repeating else '#6c757d')
    pygame.mixer.music.set_endevent(pygame.USEREVENT if is_repeating else pygame.NOEVENT)

# Hàm mở website
def open_website():
    webbrowser.open("https://kudodev06.github.io")

# Hàm mở GitHub
def open_github():
    webbrowser.open("https://github.com/kudodev06/kudodev06.github.io")

# Hàm xử lý sự kiện pygame
def check_music_end():
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT and is_repeating:
            play_music()

# Hàm chuyển đổi ngôn ngữ sang Tiếng Việt
def switch_to_vietnamese():
    global current_language
    current_language = 'vi'
    update_language()

# Hàm chuyển đổi ngôn ngữ sang Tiếng Anh
def switch_to_english():
    global current_language
    current_language = 'en'
    update_language()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("kudomp3")
root.geometry("600x800")
root.configure(bg='black')  # Đặt màu nền cho cửa sổ chính
root.iconbitmap('assets/icon.ico')  # Thay đổi đường dẫn đến file biểu tượng của bạn

# Hàm tạo nút với kiểu dáng đẹp
def create_button(parent, text, command, bg_color, hover_color):
    button = tk.Button(parent, text=text, command=command, font=("Helvetica", 12, "bold"), bg=bg_color, fg='white', relief='flat', height=2, width=12)
    button.bind("<Enter>", lambda e: button.config(bg=hover_color))
    button.bind("<Leave>", lambda e: button.config(bg=bg_color))
    return button

# Tạo khung chứa danh sách bài hát
frame_song_list = tk.Frame(root, bg='black', bd=2)
frame_song_list.pack(pady=10)

# Tạo các widget giao diện
choose_button = create_button(frame_song_list, language_texts[current_language]['choose_directory'], choose_directory, '#007bff', '#0056b3')
choose_button.pack(pady=10)

song_list = tk.Listbox(frame_song_list, selectmode=tk.SINGLE, width=50, height=10, font=("Helvetica", 12), bg='black', fg='#ffffff')
song_list.pack(pady=10)

play_button = create_button(frame_song_list, language_texts[current_language]['play'], play_music, '#28a745', '#218838')
play_button.pack(pady=5)

stop_button = create_button(frame_song_list, language_texts[current_language]['stop'], stop_music, '#dc3545', '#c82333')
stop_button.pack(pady=5)

repeat_button = create_button(frame_song_list, language_texts[current_language]['repeat'], toggle_repeat, '#6c757d', '#5a6268')
repeat_button.pack(pady=5)

volume_label = tk.Label(frame_song_list, text=language_texts[current_language]['volume'].format(50), font=("Helvetica", 12), bg='black', fg='#ffffff')
volume_label.pack(pady=5)

volume_scale = tk.Scale(frame_song_list, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, bg='black', fg='#ffffff', highlightbackground='black', troughcolor='gray')
volume_scale.set(50)
volume_scale.pack(pady=5)

song_label = tk.Label(root, text=language_texts[current_language]['no_song'], font=("Helvetica", 12), bg='black', fg='#ffffff')
song_label.pack(pady=10)

# Tạo khung chứa các nút chức năng khác
frame_buttons = tk.Frame(root, bg='black')
frame_buttons.pack(pady=10)

website_button = create_button(frame_buttons, language_texts[current_language]['website'], open_website, '#ffc107', '#e0a800')
website_button.pack(side=tk.LEFT, padx=10)

github_button = create_button(frame_buttons, language_texts[current_language]['github'], open_github, '#17a2b8', '#138496')
github_button.pack(side=tk.LEFT, padx=10)

switch_vietnamese_button = create_button(frame_buttons, "Tiếng Việt", switch_to_vietnamese, '#ffc107', '#e0a800')
switch_vietnamese_button.pack(side=tk.LEFT, padx=10)

switch_english_button = create_button(frame_buttons, "English", switch_to_english, '#17a2b8', '#138496')
switch_english_button.pack(side=tk.LEFT, padx=10)

# Thêm thông tin bản quyền và phiên bản
copyright_label = tk.Label(root, text=language_texts[current_language]['copyright'], font=("Helvetica", 10), bg='black', fg='#ffffff')
copyright_label.pack(side=tk.BOTTOM, pady=5)

version_label = tk.Label(root, text=language_texts[current_language]['version'], font=("Helvetica", 10), bg='black', fg='#ffffff')
version_label.pack(side=tk.BOTTOM, pady=5)

# Vòng lặp chính để kiểm tra sự kiện pygame
def main_loop():
    check_music_end()
    root.after(100, main_loop)

main_loop()
root.mainloop()

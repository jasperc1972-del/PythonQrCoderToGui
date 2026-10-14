import tkinter as tk
from tkinter import messagebox

import qrcode
from PIL import Image, ImageTk

DEFAULT_URL = "https://www.youtube.com/@javapresent1344"
OUTPUT_FILE = "google_qr.png"
TARGET_SIZE = 120  # QR Code 本體（不含額外白邊）的目標邊長（像素）
BORDER = 4         # 外圍留白格數（QR 標準建議值）
PADDING = 60       # QR Code 外再加的白邊（像素，每邊）
WHITE = (255, 255, 255)


class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code 產生器")
        self.root.resizable(False, False)

        tk.Label(root, text="請輸入網址或文字：", font=("Microsoft JhengHei", 11)).pack(pady=(12, 4))

        self.entry = tk.Entry(root, width=50, font=("Consolas", 11))
        self.entry.insert(0, DEFAULT_URL)
        self.entry.pack(padx=12)
        self.entry.bind("<Return>", lambda e: self.generate())

        tk.Button(root, text="產生 QR Code", font=("Microsoft JhengHei", 11),
                  command=self.generate).pack(pady=8)

        self.image_label = tk.Label(root)
        self.image_label.pack(padx=12)

        self.status = tk.Label(root, text="", fg="gray", font=("Microsoft JhengHei", 9))
        self.status.pack(pady=(4, 12))

        self.photo = None  # 保留參考，避免圖片被垃圾回收
        self.generate()

    def generate(self):
        data = self.entry.get().strip()
        if not data:
            messagebox.showwarning("提示", "請先輸入網址或文字")
            return

        qr = qrcode.QRCode(border=BORDER,
                           error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(data)
        qr.make(fit=True)

        # 依模組數計算每格像素，讓輸出圖片接近 TARGET_SIZE
        modules = qr.modules_count + BORDER * 2
        qr.box_size = max(1, round(TARGET_SIZE / modules))
        qr_img = qr.make_image(fill_color="black", back_color=WHITE).convert("RGB")

        # 貼到更大的純白畫布中央，四周留出大量白邊，避免上傳裁切切到圖案
        size = qr_img.width + PADDING * 2
        img = Image.new("RGB", (size, size), WHITE)
        img.paste(qr_img, (PADDING, PADDING))

        img.save(OUTPUT_FILE)

        # 視窗中放大顯示，用 NEAREST 保持邊緣銳利
        self.photo = ImageTk.PhotoImage(img.resize((300, 300), Image.NEAREST))
        self.image_label.config(image=self.photo)
        self.status.config(text=f"已儲存為 {OUTPUT_FILE}（{img.width}x{img.height} 像素）")


if __name__ == "__main__":
    root = tk.Tk()
    QRApp(root)
    root.mainloop()

import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from urllib.parse import urljoin
import threading

def get_download_links():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Hata", "Lütfen geçerli bir URL girin.")
        return

    # Disable button while processing
    get_links_button.config(state=tk.DISABLED)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Bağlantılar alınıyor...\n")

    # Run scraping in separate thread to avoid freezing UI
    threading.Thread(target=scrape_and_download, args=(url,), daemon=True).start()

def scrape_and_download(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        output_text.insert(tk.END, f"Hata oluştu: {e}\n")
        get_links_button.config(state=tk.NORMAL)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> with onclick containing "testeGit"
    links = []
    for a in soup.find_all("a", onclick=True):
        if "testeGit" in a["onclick"]:
            onclick_value = a["onclick"]
            try:
                # Extract numbers between quotes
                numbers = onclick_value.split("'")[1]
                question_numbers = numbers.split(",")
                download_link = "https://ogmmateryal.eba.gov.tr/panel/SoruWord.aspx?Id=" + ",".join(question_numbers)
                links.append(download_link)
            except Exception:
                continue

    if not links:
        output_text.insert(tk.END, "Test linkleri bulunamadı.\n")
        get_links_button.config(state=tk.NORMAL)
        return

    output_text.insert(tk.END, f"{len(links)} adet test linki bulundu.\n\n")

    # Prepare download directory
    home_dir = os.path.expanduser("~")
    download_dir = os.path.join(home_dir, "OGMDownloads")
    os.makedirs(download_dir, exist_ok=True)

    # Download files
    for idx, link in enumerate(links, 1):
        output_text.insert(tk.END, f"{idx}. Test indiriliyor: {link}\n")
        output_text.see(tk.END)
        try:
            file_resp = requests.get(link, headers=headers)
            file_resp.raise_for_status()
            file_path = os.path.join(download_dir, f"test_{idx}.docx")
            with open(file_path, "wb") as f:
                f.write(file_resp.content)
            output_text.insert(tk.END, f"İndirildi: {file_path}\n\n")
        except Exception as e:
            output_text.insert(tk.END, f"İndirme başarısız: {e}\n\n")

    output_text.insert(tk.END, f"Tüm dosyalar indirildi. Klasör: {download_dir}\n")
    get_links_button.config(state=tk.NORMAL)

# Setup main window
window = tk.Tk()
window.title("OGM Materyal Soru Bankası Test Link Çıkarıcı")
window.geometry("900x700")
window.configure(bg="#121212")

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background="#121212", foreground="white", font=("Segoe UI", 14))
style.configure('TButton', background="#1f1f1f", foreground="white", font=("Segoe UI", 14))
style.map('TButton', background=[('active', '#333333')])
style.configure('TEntry', fieldbackground="#1f1f1f", foreground="white", font=("Segoe UI", 14))
style.configure('TCombobox', fieldbackground="#1f1f1f", foreground="white", font=("Segoe UI", 14))

# URL input
url_label = ttk.Label(window, text="Sayfa URL'si:")
url_label.pack(padx=10, pady=(20, 5), anchor="w")

url_entry = ttk.Entry(window, width=70)
url_entry.pack(padx=10, pady=5, fill="x")

# Browser choice (kept for UI, but no effect in scraping now)
browser_label = ttk.Label(window, text="Tarayıcı (sadece görsel):")
browser_label.pack(padx=10, pady=(20, 5), anchor="w")

browser_var = tk.StringVar(value="Firefox")
browser_options = ttk.Combobox(window, textvariable=browser_var, values=["Firefox", "Chrome", "Edge"], state="readonly", width=20)
browser_options.pack(padx=10, pady=5, anchor="w")

# Get Links button
get_links_button = ttk.Button(window, text="Linkleri Al ve İndir", command=get_download_links)
get_links_button.pack(padx=10, pady=20)

# Output box
output_text = ScrolledText(window, bg="#1f1f1f", fg="white", font=("Consolas", 12))
output_text.pack(padx=10, pady=10, fill="both", expand=True)

window.mainloop()

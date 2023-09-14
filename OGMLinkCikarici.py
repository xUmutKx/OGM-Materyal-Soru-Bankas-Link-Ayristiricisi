from tkinter import Tk, Text, Button, Label, Entry, StringVar, OptionMenu
from tkinter.scrolledtext import ScrolledText
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import time
import tkinter as tk
import pathlib
import csv
import os
import requests

def get_download_links():
    main_page_url = url_entry.get()
    browser_choice = browser_var.get()
    if browser_choice == "Firefox":
        driver_path = pathlib.Path(__file__).parent / 'geckodriver.exe'
        options = FirefoxOptions()
        service = FirefoxService(executable_path=str(driver_path))
        driver = webdriver.Firefox(service=service, options=options)
    elif browser_choice == "Chrome":
        driver_path = pathlib.Path(__file__).parent / 'chromedriver.exe'
        options = ChromeOptions()
        service = ChromeService(executable_path=str(driver_path))
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_choice == "Edge":
        driver_path = pathlib.Path(__file__).parent / 'msedgedriver.exe'
        options = EdgeOptions()
        service = EdgeService(executable_path=str(driver_path))
        driver = webdriver.Edge(service=service, options=options)
    driver.get(main_page_url)
    time.sleep(1)
    test_links = driver.find_elements("xpath", '//a[contains(@onclick, "testeGit")]')
    download_links = []
    for idx, test_link in enumerate(test_links, start=1):
        onclick_value = test_link.get_attribute("onclick")
        numbers = onclick_value.split("'")[1]
        test_number = test_link.text.split("-")[-1].strip()
        question_numbers = numbers.split(",")
        download_link = "https://ogmmateryal.eba.gov.tr/panel/SoruWord.aspx?Id=" + ",".join(question_numbers)
        download_links.append(download_link)
        output_text.insert("end", f"Test {idx} Download Link: {download_link}\n")
    driver.quit()
    download_files(download_links)

def download_files(download_links):
    download_dir = os.path.expanduser('~')  # Get user's home directory
    for idx, download_link in enumerate(download_links, start=1):
        response = requests.get(download_link)
        if response.status_code == 200:
            file_name = f"downloaded_file_{idx}.docx"  # Customize the file name if needed
            file_path = os.path.join(download_dir, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            output_text.insert("end", f"Downloaded: {file_name}\n")
        else:
            output_text.insert("end", f"Failed to download: {download_link}\n")

window = Tk()
window.title("OGM Materyal Soru Bankası Test Link Çıkarıcı")
window.geometry("950x1080")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (950 / 2))
y = int((screen_height / 2) - (1080 / 2))
window.geometry(f"880x1080+{x}+{y}")
window.configure(bg="gray10")

url_label = Label(window, text="Sayfa URL'si:", fg="white", bg="gray10", font=("Arial", 18))
url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

url_entry = Entry(window, width=50, font=("Arial", 18))
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

browser_label = Label(window, text="Tarayıcı:", fg="white", bg="gray10", font=("Arial", 18))
browser_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

browser_var = StringVar()
browser_var.set("Firefox")
browser_choices = ["Firefox", "Chrome", "Edge"]
browser_option_menu = OptionMenu(window, browser_var, *browser_choices)
browser_option_menu.config(font=("Arial", 18))
browser_option_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

get_links_button = Button(window, text="Get Links", command=get_download_links, fg="white", bg="gray20", font=("Arial", 18))
get_links_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

output_text = ScrolledText(window, width=50, height=25, bg="gray10", fg="white", font=("Arial", 18))
output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()

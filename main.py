from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sqlite3

# Kullanıcıdan kelime al
cumle = "araba kuş kazak manifatura bavul çemkirmek veto meclis tarif maymun meşrubat helva yılan bardak tarak kürek kapı kazık kestane bıçak sürücü top topaç kaval karpuz peçete market bakkal poşet kalem bilgisayar çarçaf yorgan "
kelimeler = cumle.split()

tableName = "#"
dbName = "#"

def VeriTemizleme(text):

    if("1. isim" in text):
        index = text.find("isim")
        text = text[index + len("isim")+1:]

    if("1. nesnesiz " in text):
        index = text.find("nesnesiz ")
        text = text[index + len("nesnesiz ")+1:]

    if(":" in text):
        index = text.find(":")
        text = text[:index]
    
    return text

def SqlEkle(kelime,anlam):
    connection = sqlite3.connect(dbName)
    command = connection.cursor()
    command.execute(f"INSERT INTO {tableName} (kelime, anlam) VALUES (?, ?)", (kelime, anlam))
    connection.commit()
    connection.close()

for kelime in kelimeler: 
    # Bağlantılı olmayan sürücü seçeneklerini ayarla
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı gizli modda çalıştır

    # Bağlantılı olmayan sürücüyü başlat
    driver = webdriver.Chrome(options=chrome_options)

    # TDK sayfasını aç
    driver.get("https://sozluk.gov.tr/")

    # Kelimeyi siteye gir
    search_input = driver.find_element(By.CLASS_NAME, "tdk-search-input")
    search_input.send_keys(kelime)

    # Ara butonuna tıkla
    submit_button = driver.find_element(By.CLASS_NAME, "tdk-search-btn")
    submit_button.click()

    try:
        # Sonuç sayfasının yüklenmesini bekle
        wait = WebDriverWait(driver, 10)
        anlam_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#anlamlar-gts0 p")))

        # İlk paragrafı al
        paragraf = anlam_element.text
        if(len(paragraf)<=15):
            print("Kelime anlamı çok kısa")
            continue
        paragraf = VeriTemizleme(paragraf)
        SqlEkle(kelime,paragraf)
        
        # WebDriver'ı kapat
        driver.quit()

    except TimeoutException:
        # Zaman aşımı durumunda geç
        print("Anlam elementi bulunamadı. Geçiliyor.")
        driver.quit()
        continue

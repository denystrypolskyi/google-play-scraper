Instalacja wymaganych pakietów:
- pip install selenium
- pip install pyinstaller
- pip install webdriver-manager

Instrukcje uruchomienia:
- Skrypt można uruchomić za pomocą komendy: python play_store_scraper.py

Składniki:
- Inicjalizacja (metoda __init__):
    - Parametry:
        - app_id: Unikalny identyfikator aplikacji w Google Play Store.
        - chrome_driver_path: Ścieżka do pliku wykonywalnego ChromeDriver.
        - desired_comment_count: Liczba komentarzy użytkowników do pobrania (domyślnie 2).
        - timeout: Maksymalny czas oczekiwania na załadowanie elementów (domyślnie 5 sekund).
    - Atrybuty:
        - self.url: URL strony aplikacji w Google Play Store.
        - self.service: Konfiguruje usługę ChromeDriver.
        - self.options: Ustawia opcje Chrome (uruchamia Chrome w trybie headless).
        - self.driver: Inicjalizuje WebDriver Chrome.
        - self.wait: Konfiguruje explicite oczekiwanie na elementy.

- Metody pomocnicze:
    - get_element_text: Pobiera tekstową zawartość elementu zlokalizowanego za pomocą określonego selektora.
    - get_visible_element_text: Pobiera tekstową zawartość widocznego elementu.
    - get_element_attribute: Pobiera określony atrybut elementu.
    - click_element: Kliknięcie elementu, który jest klikalny.

- Metody scrapujące:
    - scrape_app_details: Zbiera szczegóły aplikacji, takie jak tytuł, opis, URL obrazu, ocena gwiazdkowa, ocena treści, liczba pobrań, data aktualizacji, informacje o reklamach, zakupy w aplikacji, data wydania oraz deweloper.
    - scrape_comments: Zbiera komentarze użytkowników, przewijając stronę i ładując więcej recenzji w miarę potrzeb.

- Główna metoda scrapująca:
    - scrape: Koordynuje scrapowanie zarówno szczegółów aplikacji, jak i komentarzy użytkowników. Zapewnia,
    że WebDriver jest poprawnie zamknięty po zakończeniu scrapowania.

Opis:
Google Play Scraper to narzędzie do automatycznego zbierania szczegółowych informacji o aplikacjach oraz komentarzy 
użytkowników z Google Play Store. Skrypt wykorzystuje Selenium WebDriver do interakcji z witryną, pozwalając na pobieranie 
danych takich jak tytuł aplikacji, opis, ocena gwiazdkowa, liczba pobrań oraz komentarze użytkowników.

Skrypt zwraca dane w formacie JSON, który zawiera następujące informacje:
• title: Tytuł aplikacji
• description: Opis aplikacji
• image: URL obrazu aplikacji
• starRating: Ocena gwiazdkowa aplikacji
• contentRating: Ocena treści
• downloads: Liczba pobrań
• updatedOn: Data ostatniej aktualizacji
• containsAds: Informacja czy aplikacja zawiera reklamy
• inAppPurchases: Informacja o zakupach w aplikacji
• releasedOn: Data wydania aplikacji
• developer: Nazwa dewelopera
• comments: Lista komentarzy użytkowników

Instalacja wymaganych pakietów:
• pip install selenium

Instrukcje uruchomienia:
• Skrypt można uruchomić za pomocą komendy: python google_play_scraper.py

Ważna uwaga: 
Wersja ChromeDriver musi odpowiadać zainstalowanej wersji Google Chrome.

Składniki:
Inicjalizacja (metoda __init__):
    Parametry:
        • app_id: Unikalny identyfikator aplikacji w Google Play Store.
        • chrome_driver_path: Ścieżka do pliku wykonywalnego ChromeDriver.
        • desired_comment_count: Liczba komentarzy użytkowników do pobrania (domyślnie 2).
        • timeout: Maksymalny czas oczekiwania na załadowanie elementów (domyślnie 5 sekund).
    Atrybuty:
        • self.url: URL strony aplikacji w Google Play Store.
        • self.service: Konfiguruje usługę ChromeDriver.
        • self.options: Ustawia opcje Chrome (uruchamia Chrome w trybie headless).
        • self.driver: Inicjalizuje WebDriver Chrome.
        • self.wait: Konfiguruje explicite oczekiwanie na elementy.

Metody pomocnicze:
    • get_element_text: Pobiera tekstową zawartość elementu zlokalizowanego za pomocą określonego selektora.
    • get_visible_element_text: Pobiera tekstową zawartość widocznego elementu.
    • get_element_attribute: Pobiera określony atrybut elementu.
    • click_element: Kliknięcie elementu, który jest klikalny.

Metody scrapujące:
    • scrape_app_details: Zbiera szczegóły aplikacji, takie jak tytuł, opis, URL obrazu, ocena gwiazdkowa, ocena treści, liczba pobrań, data aktualizacji, informacje o reklamach, zakupy w aplikacji, data wydania oraz deweloper.
    • scrape_comments: Zbiera komentarze użytkowników, przewijając stronę i ładując więcej recenzji w miarę potrzeb.

Główna metoda scrapująca:
    • scrape: Koordynuje scrapowanie zarówno szczegółów aplikacji, jak i komentarzy użytkowników. Zapewnia,
    że WebDriver jest poprawnie zamknięty po zakończeniu scrapowania.

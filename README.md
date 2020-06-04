# ODGUI
Object Detection Guided User Interface

# Środowisko
Środowisko można zbudować wykorzystując plik environment.yml.
Polecenie `conda env create -f environment.yml` stworzy nowe środowiski o nazwie ODGUI.
Wszystkie zależności można podejrzeć w pliku environment.yml.

# Przydatne strony
Zbiór przydatnych stron, z których korzystano:
- https://www.edureka.co/blog/tensorflow-object-detection-tutorial/
- https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
- https://stackoverflow.com/questions/56586304/how-to-use-tensorflows-object-detection-model-zoo-with-pretrained-models-but-mis
- https://github.com/tensorflow/models/issues/4450

# Harmonogram:
###### 1. 10 III - Zatwierdzenie tematów i harmonogram prac
  - Patryk:
    - [x] Przygotowanie repozytorium i schematu harmonogramu.
    - [x] Opis swojego harmonogramu prac.
    
  - Mateusz:
    - [x] Opis swojego harmonogramu prac.
    - [x] Wydruk harmonogramu.
    
###### 2. 24 III - Zarys systemu
  - Patryk:
    - [x] Wstępna implementacja modułu odpowiedzialnego za detekcje. 
      - [x] Schemat interfejsów klas obsługujących modele sieci neuronowych.
      - [x] Stworzenie zarysu biblioteki funkcji do przetwarzania obrazu pod kąte sieci neuronowych.
    - [x] Implementacja gotowego modelu detekcji.
      - [x] Przygotowanie modelu wraz z wagami.
      - [x] Implementacja obsługujących go metod.
      
  - Mateusz:
    - [x] Wstępna implementacja moduł odpowiedzialnego za import obrazów.
      - [x] Schemat interfejsów klas obsługujących import
    - [x] Przygotowanie GUI
    - [x] Implementacja modułu importującego obrazy z ścieżki

###### 3. 7 IV - Przedstawienie postępów, problemów, ciekawostek
  - Patryk:
    - [x] Przetestowanie działania modelu.
      - [x] Weryfikacja, czy zaimplementowane metody działają zgodnie z oczekiwaniami.
      - [x] Weryfikacja poprawności detekcji.
    - [x] Integracja z modułem odpowiedzialnym za GUI.
      - [x] Dostosowanie przygotowanego modułu do uruchomienia z poziomu GUI.
      - [x] Weryfikacja poprawności zrealizowanej integracji.
      
  - Mateusz:
    - [x] Implementacja modułu importującego obraz z kamery
      - [x] Przetwarzenie obrazu z kamery do odpowiedniej rozdzielczości i częstości odświeżania
      - [x] Weryfikacja poprawności importu

###### 4. 28 IV - Przedstawienie postępów, problemów, ciekawostek
  - Patryk:
    - [x] Implementacja dodatkowych modeli detekcji.
      - [x] Dodanie kolejnych modeli sieci neuronowych.
      - [x] Przygotowanie klasy obsługującej każdy z nich.
      - [x] Dodanie systemu przetwarzania obrazu dla każdego modelu.
      
  - Mateusz:
    - [x] Implementacja modułu importującego obrazy z adresu internetowego
      - [x] Przeszukiwanie strony internetowej w poszukiwanie obrazów 
      - [x] Przekształcenie obrazów do odpowiedniej rozdzialczości
      - [x] Weryfikacja poprawności importu
      - [x] Integracja z GUI

###### 5. 12 V - Prezentacja "gotowego" systemu
  - Patryk:
    - [x] Weryfikacja poprawności działania systemu pod kątem działania modułu detekcji.
      - [x] Weryfikacja prztwarzania danych o obrazach.
      - [x] Weryfikacja działania dostępnych modeli sieci neuronowych.
      - [x] Weryfikacja działania integralności wszystkich modeli z GUI.
      
  - Mateusz:
    - [x] Weryfikacja poprawności działania systemu pod kątem działania modułu importu.
      - [x] Weryfikacjia działania importu z ścieżki, kamery, adresu internetowego
      - [x] Weryfikacja integralności wszystkich modułów importu z GUI
    

###### 6. 26 V - Oddanie projektu, podsumowanie
  - Patryk:
    - [x] Zastosowanie uwag otrzymacyh podczas wstępnej prezentacji rozwiązania.
    
  - Mateusz:
    - [x] Zastosowanie uwag otrzymacyh podczas wstępnej prezentacji rozwiązania.

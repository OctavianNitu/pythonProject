Toate acestea sunt rulate pe o unitate care are sistemul de operare Windows 10 x64

  Instalare:

1.git
2.pycharm profesional
3.python 3.11.4

  Librarii:

1.pip install -U selenium            # Selenium Python API 
2.python -m pip install pyaudio      # PyAudio 
3.pip install opencv-python          # OpenCV 
4.py -m pip install pyautogui        # PyAutoGUI 
5.pip install numpy                  # numpy 
6.pip install moviepy                # moviepy
7.python -m pip install requests     # requests
8.python3 -m pip install sounddevice # sounddevice 
9.pip install soundfile              # soundfile
10.python3 -m pip install soundcard  # soundcard
11.pip install librosa               # librosa
12.python3 -m pip install threading  # threading

  Erori:

1. Mozila nu se inchide, chrome are nevoie de "browser.implicitly_wait" si are nevoie de input pentru a nu se inchide dupa exectarea programului 
2. Daca avem mai multe butoane de skip, programul se opreste
3. Daca nu avem buton de skip, record-ul porneste dupa inchiderea pagini web
4. Daca marim numarul de FPS, videoclipul este putin pe repede inainte, din cauza lipsei performantei, iar pentru inregistrare sunt necesare secunde suplimentare
5. Inregistrarea audio a desktop-ului nu merge intotdeauna din cauza incapacitatii functiei sc.get_microphone() de a vedea microfonul
        Posibile cauze :
            * Participarea in cadrul unei conferinte
            * Folosirea unui microfon/speaker wireless
            * Rularea mai multor procese ce implica un output al speaker-ului in acelasi timp
6. Inregistrarea audio a desktop-ului este putin pe repede inainte in primele secunde
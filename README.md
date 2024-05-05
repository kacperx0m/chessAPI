# REST Chess solver

Projekt polega na utworzeniu prostej aplikacji REST wspomagającej grę w szachy.

# Instrukcja

Projekt uruchomić za pomocą polecenia "flask --app .\Flask.py run" z aktywnego wirtualnego środowiska.
To odpali lokalny serwer na porcie 5000. Link wygląda następująco: http://127.0.0.1:5000.
Aby przejść do szczegółów figury, należy dopisać `/api/v1/{nazwa-figury}/{pole-figury}` do podstawowego adresu.
Aby przejść do weryfikacji ruchu, należy dopisać `/api/v1/{nazwa-figury}/{pole-figury}/{pole-docelowe}` do podstawowego adresu.
Każda odpowiedź serwera zwraca odpowiedni response code:
- 200 jeśli wszystko jest ok
- 409 w przypadku złego pola
- 404 jeśli odpytamy o nieistniejącą figurę
- 500 w przypadku błędu serwera
# Własny serwer VPS z prostym REST API

# Kroki

1. Wykupienie VPS.
2. Instalacja systemu (preferowane systemy UNIX-owe).
3. Stworzenie użytkownika dla aplikacji: 

```shell
adduser myapp
```

4. Nadanie użytkownikowi dostępów administratora:

```shell
usermod -aG sudo myapp
```

5. (Opcjonalnie) Konfiguracja SSH do łączenia się z serwerem.
6. (Opcjonalnie) Instalacja Pythona, jeśli nie jest zainstalowany.
7. (Opcjonalnie) Instalacja `pip` jeśli nie jest zainstalowany, przykładowo w systemie Ubuntu **22.04**:

```shell
sudo apt install pip -y
```

8. Instalacja `Virtualenv` jeśli nie jest zainstalowany:

```shell
sudo apt install python3-venv -y
```

9. Instalacja `git` jeśli nie jest zainstalowany.

```shell
sudo apt install git
```

10. Podłączenie kluczy SSH z naszego serwera np.: do GitHuba (komenda `ssh-keygen`).
11. Stworzenie struktury katalogów. Przykładowa struktura:

- `/home/myapp/` - to jest katalog domowy
  - `/programs/` - tutaj znajduje się kod źródłowy algorytmu
  - `/models/` - tutaj znajduje się zarchiwizowany model
  - `/logs/` - tutaj zbieramy logi z serwera
  - `/venvs/` - tutaj są środowiska wirtualne

12. Stworzenie modelu i zapisanie go w formacie `pickle` albo (preferowany) `joblib`.
13. Transfer modelu do katalogu `models` (może być przez GitHub).
14. Napisanie programu w `FastAPI` albo `Flask` do serwowania modelu (zobacz kod w katalogu `vps`).
15. Zabezpieczenie przed nieautoryzowanym dostępem (przykładowo customowy token).
16. Ustawienie wersji paczek i wersji Pythona.
17. Testy aplikacji lokalnie.
18. Wysłanie aplikacji na serwer.
19. Stworzenie wirtualnego środowiska z `requirements.txt`.
20. Uzupełnienie zmiennych środowiskowych na serwerze w pliku `.env`. 
21. Dodanie `gunicorn` do środowiska produkcyjnego w celu obsługi zapytań do API.
22. Instalacja `nginx` na serwerze.

```shell
sudo apt install nginx
```

23. Konfiguracja `nginx`:


**Sprawdź czy serwer działa**

```shell
systemctl status nginx
```

**Skonfiguruj serwer - dostępne aplikacje**

```shell
sudo nano /etc/nginx/sites-available/{name-of-your-app}
```

```text
server{
       server_name {your-server-ip-address}; 
       location / {
           include proxy_params;
           proxy_pass http://127.0.0.1:8000;
       }
}

```

24. Utwórz symlink do katalogu `/etc/nginx/sites-enabled`.

```shell
sudo ln -s /etc/nginx/sites-available/{name-of-your-app} /etc/nginx/sites-enabled/
```

25. Zrestartuj `nginx`

```shell
sudo systemctl restart nginx.service
```

26. Przetestuj aplikację (pamiętaj o tym, że musisz być w wirtualnym środowisku i katalogu z aplikacją)

**Uruchom aplikację**

```shell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

**Wyślij zapytanie z innego komputera**

```shell
curl -X POST http://{your-server-ip-address}/predict \
  --header "${ACCESS_TOKEN_HEADER_NAME}: ${ACCESS_TOKEN}" \
  --header 'Content-Type: application/json' \
  --data '{"ds": [101, -66.4, 3, 1]}'
```

Jeśli wszystko działa poprawnie uruchom serwis predykcyjny.

27. Stwórz serwis obsługujący Gunicorn non-stop używając do tego `systemd`

```shell
sudo nano /etc/systemd/system/{your-app-name}.service
```

```shell
[Unit]
Description=Gunicorn instance to serve {your-app}
After=network.target

[Service]
User=<username>
WorkingDirectory={path to the directory with app.py file}
Environment={path to the venv bin}
ExecStart={path to the venv bin}/gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app

[Install]
WantedBy=multi-user.target
```

28. Uruchom serwis!

```shell
sudo systemctl start {your-app-name}.service
```

29. Przetestuj aplikację!

```shell
curl -X POST http://{your-server-ip-address}/predict \
  --header "${ACCESS_TOKEN_HEADER_NAME}: ${ACCESS_TOKEN}" \
  --header 'Content-Type: application/json' \
  --data '{"ds": [101, -66.4, 3, 1]}'
```


# Dodatkowe rady

- zawsze uzupełniaj i aktualizuj `README.md` opisując jak instalować paczkę, jak wygląda wejście i jak wygląda wyjście API
- nigdy nie udostępniaj zmiennych środowiskowych w publicznych repozytoriach (najlepiej w ogóle nie wysyłać plików `.env` do repozytoriów)
- jeśli nie używasz serwisu, to usuń go z `/etc/nginx/sites-enabled/` i `/etc/systemd/system/{your-app-name}.service`, zresetuj `nginx` i `systemd`
- sprawdzaj logi
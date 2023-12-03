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
16. Dodanie `uvicorn` w celu obsługi zapytań do API.
17. Ustawienie wersji paczek i wersji Pythona (fixed).
18. Testy aplikacji lokalnie.
19. Wysłanie aplikacji na serwer.
20. Stworzenie wirtualnego środowiska z `requirements.txt`.
21. Uzupełnienie zmiennych środowiskowych na serwerze w pliku `.env`.


# Dodatkowe rady

- zawsze uzupełniaj i aktualizuj `README.md` opisując jak instalować paczkę, jak wygląda wejście i jak wygląda wyjście API
- 
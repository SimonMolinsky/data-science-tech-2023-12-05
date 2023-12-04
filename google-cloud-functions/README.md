# Serwer automatycznie łączący się z BigQuery który zrzuca wyniki do Google Cloud Storage i BigQuery

## Kroki

1. Wczytaj dane z `BigQuery`
2. Transformacja danych (szeroko pojęta)
3. Zapis wyników jako surowych danych w `Cloud Storage`

## Instalacja

1. Stwórz nowy projekt na Google Cloud Platform albo wykorzystaj istniejący
2. Pozwól na używanie następujących serwisów w projekcie:
    - Cloud Functions
    - Cloud Build
    - Cloud Run
    - Artifact Registry
    - BigQuery
    - Google Cloud Storage
    - Cloud Scheduler
3. Zainstaluj Google Cloud CLI na swojej lokalnej maszynie.
4. (Opcjonalnie) Instalacja Pythona, pip i Dockera na lokalnej maszynie.

## Kodowanie

Stwórz i przetestuj funkcję do transformacji danych, do reszty elementów możesz wykorzystać szablon z repozytorium.

## Ustawienia projektu

1. Tabela `BigQuery` wejściowa.
2. Tabela `BigQuery` wyjściowa.
3. Bucket w `Cloud Storage` na dane wyjściowe.
4. Uzupełnij zmienne środowiskowe w pliku `.env`: nazwę tabeli wyjściowej i nazwę wyjściowego Bucketu.

## Deploy

- Zobacz `deploy_function_and_scheduler.sh`
- Stack usuwaj z `remove_function_and_scheduler.sh`

## Bucket

- określ wzorzec w jakim zapisywane są pliki, przydatne jest zapisywanie predykcji albo danych w taki sposób, żeby sama nazwa pliku stanowiła metadane
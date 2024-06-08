Topics kafki w naszej aplikacji

* topic główny producenta: project_straming
* topic poboczny do któego trafiają wyniki: output_streaming


# Uruchomienie flaska wewnątrz środowiska analizy danych w czasie rzeczywistym:

1. dodać linijkę 
- 5000:5000 w pliku docker-compose.yml i zapisać
2. zrobić w terminalu swojego komputera docker compose up w ścieżce katalogu jupiter-lab
3.  w apce wpisać hosta 
4. i uruchamiać plik linijką:
flask run --host 0.0.0.0

# requirements.txt
*  dodatkowe paczki do zainstalowania poza wgranymi środowiskowymi z kontenera

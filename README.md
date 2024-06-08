Topics kafki w naszej aplikacji
* topic główny producenta: project_straming
* topic poboczny do którego trafiają wyniki: output_streaming

# Uruchamianie działania projektu
### odwołanie do: https://sebkaz-teaching.github.io/RTA_2024/lab/cw2.html

1. najpierw utworzyć dwa topici: project_straming i output_streaming\
     a. w tym celu uruchomić terminal i zmienić ścieżkę na:\
    cd ~\
     b. dodać topic:\
   kafka/bin/kafka-topics.sh --bootstrap-server broker:9092 --create --topic project_streaming\
   kafka/bin/kafka-topics.sh --bootstrap-server broker:9092 --create --topic output_streaming\
   


### Uruchomienie flaska wewnątrz środowiska analizy danych w czasie rzeczywistym:

1. dodać linijkę 
- 5000:5000 w pliku docker-compose.yml i zapisać
2. zrobić w terminalu swojego komputera docker compose up w ścieżce katalogu jupiter-lab
3.  w apce wpisać hosta 
4. i uruchamiać aplikację flaska linijką:
flask run --host 0.0.0.0

# requirements.txt
*  dodatkowe paczki do zainstalowania poza wgranymi środowiskowymi z kontenera

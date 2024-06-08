Topics kafki w naszej aplikacji
* topic główny producenta: project_straming
* topic poboczny do którego trafiają wyniki: output_streaming

# Uruchamianie działania projektu
### odwołanie do: https://sebkaz-teaching.github.io/RTA_2024/lab/cw2.html

1. Na początku pracy najpierw utworzyć dwa topici: project_straming i output_streaming\
*  w tym celu uruchomić terminal i zmienić ścieżkę na:
    cd ~\
* dodać topici:\
   kafka/bin/kafka-topics.sh --bootstrap-server broker:9092 --create --topic project_streaming
   kafka/bin/kafka-topics.sh --bootstrap-server broker:9092 --create --topic output_streaming
* utworzyć producenta generującego dane nr 1 - nieprzetworzone:
   kafka/bin/kafka-console-producer.sh --bootstrap-server broker:9092 --topic project_streaming\

* uruchomić sobie na innym terminalu żeby sprawdzić, czy działa na printach:\
     python producer.py\
3. otworzyć nowe okno terminala i sprawdzić, czy producent nr 1 generuje dane:\
  kafka/bin/kafka-console-consumer.sh --bootstrap-server broker:9092 --topic project_streaming --from-beginning\
   powinny generować się dane\
4.  I w nastęnej konsoli można też w ten sposób działanie reguły decyzyjnej - danych przetworzonych:\
* w jednej konsoli można uruchomić sobie:
python consumer.py żeby zobaczyć wydruk\
* w drugiej konsoli można wyrzucić sobie kafkę:\
kafka/bin/kafka-console-consumer.sh --bootstrap-server broker:9092 --topic output_streaming --from-beginning


    
   
   


### Uruchomienie flaska wewnątrz środowiska analizy danych w czasie rzeczywistym:

1. dodać linijkę 
- 5000:5000 w pliku docker-compose.yml i zapisać
2. zrobić w terminalu swojego komputera docker compose up w ścieżce katalogu jupiter-lab
3.  w apce wpisać hosta 
4. i uruchamiać aplikację flaska linijką:
flask run --host 0.0.0.0

# requirements.txt
*  dodatkowe paczki do zainstalowania poza wgranymi środowiskowymi z kontenera

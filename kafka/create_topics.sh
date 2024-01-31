# wait for kafka to be ready to accept new topics
while ! /bin/kafka-topics --bootstrap-server localhost:9092 --list; do
    sleep 1
done

for topic in rdf-parse-events; do
    kafka-topics --bootstrap-server localhost:9092 \
        --create --if-not-exists \
        --partitions 4 \
        --topic "${topic}"
done

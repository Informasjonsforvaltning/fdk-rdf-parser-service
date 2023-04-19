#!/bin/bash

# Start parser process
poetry run python -u fdk_rdf_parser_service/app.py &

# Start the rabbit consumer
poetry run python -u fdk_rdf_parser_service/rabbit/consumer/consumer.py &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?

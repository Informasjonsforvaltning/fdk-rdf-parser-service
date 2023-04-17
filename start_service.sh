#!/bin/bash

# Start parser process
# python fdk_rdf_parser_service/parser.py

# Start the rabbit consumer
python -m fdk_rdf_parser_service.rabbit.consumer &

# Start API/service
# gunicorn "fdk_rdf_parser_service:create_app" \
#          --config=fdk_rdf_parser_service/gunicorn_config.py \
#          --worker-class aiohttp.GunicornWebWorker \
#          --workers 2 \
#          --log-level=debug

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?

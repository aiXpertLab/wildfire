sudo docker run -it --name wildfire -v $(pwd):/app -w /app python:3.11-slim bash

docker start -ai wildfire
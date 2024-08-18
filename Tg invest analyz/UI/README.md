% docker build -t telega_mvp:v1 -f Dockerfile .
% docker run --net telegram --ip 172.24.0.14 -d --name mvp-v1 -v "$PWD":/usr/src -p 9878:8501  telega_mvp:v1

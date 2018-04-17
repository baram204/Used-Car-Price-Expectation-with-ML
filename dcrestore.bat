:configureDocker
 FOR /f "tokens=*" %%i IN ('docker-machine env default') DO %%i

:eod
cd docker\dockerimage
docker load -i ./mysql.tar
docker load -i ./adminer.tar
docker load -i ./flask.tar
docker load -i ./jupyter.tar

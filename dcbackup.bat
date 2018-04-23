:configureDocker
 FOR /f "tokens=*" %%i IN ('docker-machine env default') DO %%i

:eod
cd docker\dockerimage
docker save -o ./mysql.tar mysql
docker save -o ./adminer.tar adminer
docker save -o  ./flask.tar docker_flask
docker save -o ./jupyter.tar docker_jupyter

:configureDocker
 FOR /f "tokens=*" %%i IN ('docker-machine env default') DO %%i

:eod
cd docker
docker-compose %1 %2
cd ..

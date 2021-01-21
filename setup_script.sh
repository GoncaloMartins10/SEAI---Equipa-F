#!/bin/bash
source activate seai_env


# iniciar o docker
cd db
docker-compose up > /dev/null 2>&1 &
sleep 1
IFS=$'\n' dockerComposeProcesses=($(ps -ef | grep docker | awk '{if ($(NF-1)=="docker-compose") print $2}'))
echo "docker-compose running in processes: ${dockerComposeProcesses[@]}"
cd - > /dev/null 2>&1

# iniciar o servidor django
cd src/interface/
python manage.py runserver > /dev/null 2>&1 &
sleep 1
djangoProcess="$(ps -ef | grep manage | awk '{if(index($(NF-2), "miniconda3")) print $2}')"
echo "django running in process: $djangoProcess"
cd - > /dev/null 2>&1

# iniciar o servidor frontend
cd src/frontend/
yarn start > /dev/null 2>&1 &
sleep 10
yarnProcess="$(ps -ef | grep start | awk '{if(index($NF, "start.js")) print $2}')"
echo "frontend running in process: $yarnProcess"
cd - > /dev/null 2>&1

# iniciar o tensorboard
#tensorboard --logdir "$(pwd)"/interface/logs/fit &


printf "\n\npress [ENTER] to quit all processes\n"
read 

kill -9 ${dockerComposeProcesses[@]}
kill -9 $djangoProcess
kill -9 $yarnProcess

#!/bin/bash

A=$1
OLLAMA_MODELS=${HOME}/models ollama serve &
sleep 5
if [ "$A" == "develop" ];
then
	jupyter notebook --allow-root --no-browser --port 8888 --ip=0.0.0.0 --NotebookApp.token=''
elif [ "$A" == "deploy" ];
then
	voila --no-browser --template vuetify-default --enable_nbextensions=True frontend/Interface.ipynb --Voila.ip=0.0.0.0 --port 8888
elif [ "$A" == "debug" ];
then 	
	bash
elif [ "$A" == "model" ];
then 
	i=1
	while [[ "$i" != "0" ]]
	do
		ollama pull $2
		i=$?
		echo $i
	done
else
	echo "unknown input"
fi


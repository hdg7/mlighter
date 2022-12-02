#! /bin/bash

#jupyter notebook --allow-root --no-browser --port 8888 --ip=0.0.0.0 --NotebookApp.token=''
voila --template vuetify-default --enable_nbextensions=True frontend/WholeInterface.ipynb --Voila.ip=0.0.0.0 --port 8888 --no-browser

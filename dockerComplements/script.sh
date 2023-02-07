#/bin/bash

rm -r mlighter
cp -r  ../../mlighter .
sed -i'.orig' -e 's3Users/hector1/mltest3home/advml3g'  mlighter/WholeInterface.ipynb
docker build . --tag mlighter

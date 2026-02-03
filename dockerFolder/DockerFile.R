FROM debian:12

RUN apt-get -y update
RUN apt-get install -yq --fix-missing build-essential emacs-nox vim-tiny git inkscape jed libsm6 libxext-dev libxrender1 lmodern netcat-openbsd python3-dev tzdata unzip nano emacs ca-certificates wget gcc-12 gcc-12-plugin-dev curl screen  nginx clang llvm lld gdb

#Extras for R
RUN apt-get install -yq gfortran libreadline-dev zlib1g-dev librust-bzip2-dev liblzma-dev libpcre2-dev libcurl4-openssl-dev

#Support packages for Python
RUN apt-get install -y libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev

RUN useradd -ms /bin/bash advml 

USER advml
WORKDIR /home/advml

#Install AFL++
RUN git clone https://github.com/AFLplusplus/AFLplusplus.git
WORKDIR /home/advml/AFLplusplus
RUN make
USER root
RUN make install

#Install the R-project
USER advml
WORKDIR /home/advml/
RUN wget https://cloud.r-project.org/src/base/R-4/R-4.4.3.tar.gz
RUN tar xvzf R-4.4.3.tar.gz
WORKDIR /home/advml/R-4.4.3
RUN CC=/home/advml/AFLplusplus/afl-clang-lto CXX=/home/advml/AFLplusplus/afl-clang-lto++ CFLAGS="-g -O0" ./configure --with-x=no --enable-static --disable-shared
#Docker might not allow to compile R with ASAN
#RUN AFL_USE_ASAN=1 make
#RUN AFL_IGNORE_PROBLEMS=1  AFL_IGNORE_PROBLEMS_COVERAGE=1 make
RUN make
USER root
#RUN AFL_IGNORE_PROBLEMS=1  AFL_IGNORE_PROBLEMS_COVERAGE=1 make install
RUN make install

#Install R packages
RUN Rscript -e 'install.packages(c("e1071","party","caret","nnet","randomForest","rpart","xgboost"), repos="https://cloud.r-project.org")'
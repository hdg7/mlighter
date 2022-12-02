FROM debian:11

RUN apt-get update
RUN apt-get install -yq --fix-missing build-essential emacs-nox vim-tiny git inkscape jed libsm6 libxext-dev libxrender1 lmodern netcat python-dev tzdata unzip nano emacs ca-certificates wget gcc curl screen  nginx 

#Extras for R
RUN apt-get install -yq gfortran libreadline-dev zlib1g-dev librust-bzip2-dev liblzma-dev libpcre2-dev libcurl4-openssl-dev

#Support packages for Python
RUN apt-get install -y libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev

RUN useradd -ms /bin/bash advml 

USER advml
WORKDIR /home/advml

#Install AFL
RUN git clone https://github.com/google/AFL.git
WORKDIR /home/advml/AFL
RUN make
USER root
RUN make install
#RUN 

#Install the R-project
USER advml
WORKDIR /home/advml/
RUN wget https://cloud.r-project.org/src/base/R-4/R-4.0.4.tar.gz
RUN tar xvzf R-4.0.4.tar.gz
WORKDIR /home/advml/R-4.0.4
#RUN CC=/home/advml/AFL/afl-gcc CXX=/home/advml/AFL/afl-g++ ./configure --with-x=no --enable-static --disable-shared
#RUN AFL_USE_ASAN=1 make
#USER root
#RUN make install


#Install Python
USER advml
WORKDIR /home/advml
RUN curl -O https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
RUN tar -xvzf Python-3.10.0.tgz
WORKDIR /home/advml/Python-3.10.0
RUN CC=/home/advml/AFL/afl-gcc CXX=/home/advml/AFL/afl-g++ ./configure --enable-static --disable-shared
RUN make
USER root
RUN make install


#Installing the jupyter interface
USER root
RUN pip3 install --upgrade pip
RUN pip3 install numpy jupyter pandas joblib scikit-image sklearn python-afl voila ipyvuetify jupyter_contrib_nbextensions voila-vuetify
WORKDIR /home/advml/
ADD initScript.bash /home/advml/initScript.bash 
COPY mlighter /home/advml/mlighter
WORKDIR /home/advml/mlighter
EXPOSE 8888
RUN chmod 755 /home/advml/initScript.bash
CMD ["/home/advml/initScript.bash"]
#USER root


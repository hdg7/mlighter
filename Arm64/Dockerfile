FROM debian:11

RUN apt-get update
RUN apt-get install -yq --fix-missing build-essential emacs-nox vim-tiny git inkscape jed libsm6 libxext-dev libxrender1 lmodern netcat python-dev tzdata unzip nano emacs ca-certificates wget gcc curl screen nginx 

#Extras for R
RUN apt-get install -yq gfortran libreadline-dev zlib1g-dev librust-bzip2-dev liblzma-dev libpcre2-dev #libcurl4-openssl-dev

#Support packages for Python
RUN apt-get install -y libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev

RUN useradd -ms /bin/bash advml 

USER advml
WORKDIR /home/advml

#Install AFL
#RUN git clone https://github.com/google/AFL.git
#WORKDIR /home/advml/AFL
#RUN AFL_NO_X86=1 make
#USER root
#RUN AFL_NO_X86=1 make install
#RUN 

#Add missing
USER root
RUN apt-get install -yq libbz2-dev gfortran libcurl4-gnutls-dev default-jre default-jdk libssl-dev afl

#Install the R-project - AFL is incompatible with -static - remove AFL_USE_ASAN
USER advml
RUN export AFL_MAP_SIZE=98864
WORKDIR /home/advml/
RUN wget https://cloud.r-project.org/src/base/R-4/R-4.0.4.tar.gz
RUN tar xvzf R-4.0.4.tar.gz
WORKDIR /home/advml/R-4.0.4
RUN CC=afl-clang-fast CXX=afl-clang-fast++ ./configure --with-x=no --enable-static --disable-shared
RUN make
USER root
RUN make install


#Install Python
USER advml
RUN export AFL_MAP_SIZE=136960
WORKDIR /home/advml
RUN curl -O https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
RUN tar -xvzf Python-3.10.0.tgz
WORKDIR /home/advml/Python-3.10.0
RUN CC=afl-clang-fast CXX=afl-clang-fast++ ./configure --enable-static --disable-shared
RUN make
USER root
RUN make install

#Installing the jupyter interface
USER root
RUN pip3 install --upgrade pip
RUN pip3 install numpy jupyter pandas joblib scikit-image scikit-learn python-afl voila ipyvuetify jupyter_contrib_nbextensions voila-vuetify bqplot deap
RUN pip3 install ipywidgets
WORKDIR /home/advml/
COPY mlighter /home/advml/mlighter
ADD initScript.bash /home/advml/mlighter/initScript.bash 
WORKDIR /home/advml/mlighter
EXPOSE 8888
ENV MLIGHTER_HOME=/home/advml/mlighter
ENV AFL_SKIP_CPUFREQ=1
ENV AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1
RUN chmod 755 /home/advml/mlighter/initScript.bash
#For Windows users
RUN sed -i -e 's/\r$//' /home/advml/mlighter/initScript.bash
CMD ["/home/advml/mlighter/initScript.bash"]
#USER root

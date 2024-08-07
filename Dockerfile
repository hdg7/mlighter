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
RUN wget https://cloud.r-project.org/src/base/R-4/R-4.4.1.tar.gz
RUN tar xvzf R-4.4.1.tar.gz
WORKDIR /home/advml/R-4.4.1
RUN CC=/home/advml/AFLplusplus/afl-gcc CXX=/home/advml/AFLplusplus/afl-g++ CFLAGS="-g -O0" ./configure --with-x=no --enable-static --disable-shared
#Docker might not allow to compile R with ASAN
#RUN AFL_USE_ASAN=1 make
RUN make
USER root
RUN make install


#Install Python
USER advml
WORKDIR /home/advml
RUN curl -O https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
RUN tar -xvzf Python-3.10.12.tgz
WORKDIR /home/advml/Python-3.10.12
RUN CC=/home/advml/AFLplusplus/afl-gcc CXX=/home/advml/AFLplusplus/afl-g++ ./configure --enable-static --disable-shared
RUN make
USER root
RUN make install


#Install Crashwalk

WORKDIR /home/advml
RUN wget https://go.dev/dl/go1.21.3.linux-amd64.tar.gz
USER root
RUN tar -C /usr/local -xzf go1.21.3.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin
RUN git clone https://github.com/jfoote/exploitable.git
USER root
WORKDIR /home/advml/exploitable/
RUN python3 setup.py install
USER advml
ENV CW_EXPLOITABLE=/home/advml/exploitable/exploitable/exploitable.py
RUN go install github.com/bnagy/crashwalk/cmd/...@latest


#Installing the jupyter interface
USER root
RUN pip3 install --upgrade pip
RUN pip3 install numpy jupyter pandas joblib xgboost scikit-image scikit-learn python-afl voila ipyvuetify jupyter_contrib_nbextensions voila-vuetify bqplot deap 
RUN pip3 install ipywidgets
RUN pip3 install transformers torch
RUN pip3 install ipywidgets ollama

#Installing Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN pip3 install ipyflex plotly

WORKDIR /home/advml/
RUN mkdir /home/advml/outputs
COPY mlighter /home/advml/mlighter
RUN mkdir /root/models

#Installing the python mlighter-utils
RUN ./mlighter/utils/install.sh


ADD initScript.bash /home/advml/mlighter/initScript.bash 
WORKDIR /home/advml/mlighter
EXPOSE 8888
ENV MLIGHTER_HOME=/home/advml/mlighter
ENV MLIGHTER_FOLDER=/home/advml/outputs
ENV AFL_SKIP_CPUFREQ=1
ENV AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1
RUN chmod 755 /home/advml/mlighter/initScript.bash
RUN chown -R advml:advml *
#For Windows users
RUN sed -i -e 's/\r$//' /home/advml/mlighter/initScript.bash
ENTRYPOINT ["/home/advml/mlighter/initScript.bash"]
CMD ["echo","Default argument for CMD instruction"]
#USER root


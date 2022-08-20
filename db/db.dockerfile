FROM pgrouting/pgrouting

# dependencies
RUN apt-get update
RUN apt-get install -y git wget gcc build-essential libssl-dev clang-format cmake-curses-gui lcov doxygen libtool postgresql-server-dev-13

# install cmake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.22.0-rc2/cmake-3.22.0-rc2.tar.gz
RUN tar xzf cmake-3.22.0-rc2.tar.gz
WORKDIR cmake-3.22.0-rc2
RUN ./bootstrap
RUN make
RUN make install
WORKDIR ..

# install h3 binding
RUN git clone https://github.com/uber/h3.git
WORKDIR h3
RUN git checkout stable-3.x
RUN mkdir build
WORKDIR build
RUN cmake -DCMAKE_C_FLAGS=-fPIC ..
RUN make
RUN make install
WORKDIR ../../

# install pgh3
RUN git clone https://github.com/dlr-eoc/pgh3.git
WORKDIR pgh3
RUN make
RUN make install
WORKDIR ..
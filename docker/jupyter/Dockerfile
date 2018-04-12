FROM giffordlab/minimal-notebook

MAINTAINER Matt Edwards <matted@mit.edu>

USER root

# Hacky access control for the image
RUN echo "matted ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "thashim ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "zeng ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN apt-get update -qq && apt-get install -qqy software-properties-common && \
    add-apt-repository ppa:marutter/rrutter && \
    add-apt-repository ppa:staticfloat/juliareleases && \
    add-apt-repository ppa:staticfloat/julia-deps && \
    apt-get update

RUN apt-get install -y --no-install-recommends  apt-utils \
    wget && \
    wget http://ftp.au.debian.org/debian/pool/main/n/netselect/netselect_0.3.ds1-26_amd64.deb && \
    dpkg -i netselect_0.3.ds1-26_amd64.deb

RUN apt-get install -y --no-install-recommends  apt-utils \
    emacs24-nox \
    fonts-dejavu \
    gcc \
    gfortran

RUN apt-get install -y --no-install-recommends  apt-utils \
    graphviz \
    julia \
    nano \
    wget \
    zsh
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# extra custom package
RUN apt-get install -y --no-install-recommends  apt-utils\
    python-mysqldb \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3 packages
RUN conda install --yes \
    'ipywidgets=5.2*' \
    'pandas=0.22*' \
    'numexpr=2.6*' \
    'matplotlib=2.1*' \
    'scipy=1.0*'
RUN conda install --yes \
    'seaborn=0.7*' \
    'scikit-learn=0.19*' \
    'pytables=3.4.2*' \
    'sympy=1.0*'
RUN conda install --yes \
    'cython=0.27*' \
    'patsy=0.4*' \
    'statsmodels=0.8*' \
    'cloudpickle=0.5*'
RUN conda install --yes \
    'dill=0.2*' \
    'numba=0.36*' \
    'bokeh=0.12*' \
    'h5py=2.7*' \
    'theano=1.0.1' \
    biopython
#    && conda clean -yat

# extra custom package
RUN conda install --yes \
    'numpy=1.14*' \
    'requests=2.14*' \
    'sqlalchemy=1.1*' \
    'scikit-learn=0.19*' \
    'matplotlib=2.0*' \
    && conda clean -yat

RUN pip --no-cache-dir install tensorflow-gpu

RUN pip install bs4 ConfigParser Flask-SQLAlchemy
RUN apt-get install python-dev

RUN pip install bash_kernel && \
    python -m bash_kernel.install

# set fastest repository server
RUN rm /etc/apt/sources.list
COPY sources.list /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y \
    libmysqlclient-dev \
    python3-mysqldb
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

RUN pip install mysqlclient

RUN git clone --recursive "https://github.com/dmlc/xgboost"

RUN cd xgboost && make -j4

RUN cd xgboost && cd python-package

RUN pip install xgboost

RUN pip install lxml

USER jovyan
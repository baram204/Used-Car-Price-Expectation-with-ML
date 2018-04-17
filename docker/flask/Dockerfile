FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN git clone --recursive "https://github.com/dmlc/xgboost" xgboost/ubuntu

RUN cd xgboost/ubuntu && make -j4 && cd python-package && pip install
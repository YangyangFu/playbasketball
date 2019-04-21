FROM continuumio/anaconda3

RUN pip install buildingspy 
RUN pip install opencv-python
RUN pip install PyPrind
FROM python:latest
FROM openmc/openmc:latest

#working directory
WORKDIR /home/antonio/Documents/Coding/Enviroment/docker/env1

#to COPY the remote file at working directory in container
COPY Simulation Simulation
COPY Data Data
COPY Results Results



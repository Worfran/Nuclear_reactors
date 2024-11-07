# Nuclear Reactors

This repository contains a simulation of nuclear reactors using OpenMC. For more information on OpenMC, visit the [OpenMC documentation](https://docs.openmc.org/en/stable/index.html).

## Project Overview

The first simulation uses a template of a Pressurized Water Reactor (PWR). The template can be retrieved from the [OpenMC examples](https://docs.openmc.org/en/stable/_modules/openmc/examples.html#pwr_assembly).

This project is the final project for the Bachelor of Science in Physics program at Universidad de los Andes, Colombia.

## Project Structure

```
Root
├── Data
│   ├── chain_endfb80_pwr.xml
│   ├── endf-6-16461.txt
│   ├── endfb-vii.1-hdf5
│   └── materials-data.h5
├── dockerfile
├── Plots
│   ├── percentual_change_th232_con_10.png
│   ├── percentual_change_th232_con_50.png
│   ├── percentual_change_th232_Pu239.png
│   ├── percentual_change_th232_U233_10.png
│   ├── percentual_change_th232_U233_5.png
│   ├── percentual_change_th232_U233.png
│   └── U233_Cross_Section.png
├── README.md
├── Results
│   ├── Sruntest
│   ├── Th232
│   ├── Th232_con_10
│   ├── Th232_con_50
│   ├── Th232_Pu239
│   ├── Th232_U233_5
│   ├── Th233_U233_10
│   └── U02
└── Simulation
    ├── log
    ├── plot_sigma.py
    ├── plotter_1.py
    ├── plotter_2.py
    ├── plotter_3.py
    ├── pwr_model_source.py
    ├── __pycache__
    ├── run_reactor_multi_thread.py
    ├── run_reactor.py
    ├── simulator_v1.py
    └── structure_results.py
```
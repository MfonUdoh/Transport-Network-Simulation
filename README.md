# Transport Network Simulation

## Introduction

For most transportation companies; the foundation of its ability to fufill consignments relies on its transportation network. In domestic operation, consignments are usually transported by road if there is no express service requested.

The general basis of a road transport network is a simple exchange between two main elements; Depots and Hubs. Depots are relatively small stations which collect and deliver consignments to and from residential and commercial locations within a catchment area in its local vicinity. Hubs are much larger facilities which recieve consignments from depots, sort them and sends them out to whichever depot is located closest to the desired destination.

Most large transport companies that have the benefit of a UK wide transport network use a 'Hub & Spoke' configuration; this is essentially a system where there is one (or few) centrally located hub that serves all the depots of the country which can be thought of as radiating away from the hub like spokes on a bicycle wheel. 

There are several economic and operational reasons why the centralised approach is usually the method of choice, however the primary reasons are the capital and operational costs associated with each hub. An important consideration is the age of the facilities, for the older companies particulalry, some of the hubs have been in operation for decades meaning they were constructed as part of a traditional transport strategy. In recent years, automation has managed to improve the efficiency of hubs so that their operating costs are declining enough to make a decentralised network much more financially feasible.

## Aims

- Generate and analyse data regarding the network
- Visuallise the operation of the network
- Optimise the geographic configuration of the network elements

## Future Work

- GUI for simulation configuration
- Drag & drop positioning of map elements
- Temporal awareness
    - Implement trailer elements which transport a certain number of consignments at a certain time
    - Generate optimal trailer departure timings for the hubs

## Quick-Start Guide

1. Clone the repository

    `git clone github.com/mfonudoh/transport-network-simulation`

2. Install the requirements

    `pip install -r requirements.txt`

3. Run the main file

    `python3 main.py`

The program will generate text files filled with the generated data along with the visual representation.

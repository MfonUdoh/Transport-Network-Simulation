# Transport Network Simulation

## Introduction

For most transportation companies; the foundation of its ability to fulfil consignments relies on its transportation network. In domestic operation, consignments are usually transported by road if there is no express service requested.

The general basis of a road transport network is a simple exchange between two main elements; Depots and Hubs. Depots are relatively small stations which collect and deliver consignments to and from residential and commercial locations within a catchment area in its local vicinity. Hubs are much larger facilities which receive consignments from depots, sort them and sends them out to whichever depot is located closest to the desired destination.

## Network Configuration

Most large transport companies that have the benefit of a UK wide transport network use a 'Hub & Spoke' configuration; this is essentially a system where there is one (or few) centrally located hub that serves all the depots of the country which can be thought of as radiating away from the hub like spokes on a bicycle wheel.

A modern trend that is becoming popular in many industries is the ethos of decentralisation; in terms of transport network design, this translates to having a larger quantity of smaller sized, regional hubs. The main benefit of decentralisation is increased average efficiency of the network; in general, each consignment will have a higher chance of taking a more direct (and hence more efficient) path to its destination with each additional node (hub) added to the network.

There are several economic and operational reasons why the centralised approach is usually the method of choice, however, the primary reasons are the capital and operational costs associated with each hub. An important consideration is the age of the facilities, for the older companies particularly, some of the hubs have been in operation for decades meaning they were constructed as part of a traditional transport strategy. In recent years, automation has managed to improve the efficiency of hubs so that their operating costs are declining enough to make a decentralised system of regional hubs significantly more financially feasible.

## Project Aims

- Generate and analyse data regarding the network
- Visualise the operation of the network
- Optimise the geographic configuration of the network elements

## Future Work

- GUI for simulation configuration
- Drag & drop positioning of map elements
- Temporal awareness
    - Implement trailer elements which transport a certain number of consignments at a certain time
    - Generate optimal trailer departure timings for the hubs

## Quick-Start Guide

1. Clone the repository

    `git clone https://github.com/mfonudoh/transport-network-simulation`

2. Install the requirements

    `pip install -r requirements.txt`

3. Run the main file

    `python3 Viewer.py`

The program will generate text files filled with the generated data along with the visual representation.

![Transport-Simulation](https://github.com/MfonUdoh/Transport-Network-Simulation/assets/48888128/e9cf4c32-8cc8-4f00-88ba-d03385693e40)


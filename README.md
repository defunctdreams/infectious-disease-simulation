# Infectious Disease Simulation

## Overview

A program to visualise simulations of an infectious disease spreading through a procedurally generated basic town.

This README details (in part) the key components of the program and how they work.

## Run

1. Install poetry with:

    ```bash
    pip install poetry
    ```

2. Navigate to the directory in which the code is saved by:

    ```bash
    cd <PATH>
    ```

3. Run the program using:

    ```bash
    poetry run python -m infectious_disease_simulation.main
    ```

4. Set parameters in the GUI, or load a previous simulation's parameters

5. Run the simulation

6. Use the map window to visualise the movement of people and propagation of the disease, and the graph window to see the live S/E/I/R/D curves

### Run with Nix Flakes

The program is wrapped in a flake, so it can be run with:

    ```bash
    nix run 'github:defunctdreams/infectious_disease_simulation'
    ```



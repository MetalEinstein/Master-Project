# Master-Project

This project presents the development of an algorithm for assigning tasks to a fleet of Autonomous Guided Vehicles (AGV)s also known as a fleet manager. The task assignment is done by using a Genetic Algorithm (GA) to handle the multiple travelling salesmen problem (mTSP). The mTSP is a problem definition, which closely resembles the challenge faced in this project thereby making it a prime target to test the GA against. The GA is inspired by evolution and is divided into five parts; initial population, fitness function, selection process, breeding and mutation. These parts are iterated through for several generation. In this case the GA is programmed to optimise the sequence of tasks present in a pick and place environment over time. Furthermore, decentralisation methods are explored for algorithm optimisation, and it was shown that it could be used as such conceptually.
The project ended out with a GA that was within 20% of the global minimum 90% of the time.

The code produces a solution to a mTSP, for a predefined number of tasks and agents. The main branch include the newest tested working version of the algorithm, while the other braches are different feature implementations.

The output is a nested list containing routes for each AGV.

The algorithm is initialized by running: Main Project/mTSB-Centralized_FixedAgent/mTSP_Main.py

Authors:

Alexander Staal: astaal16@student.aau.dk

Ditte Damgaard Albertsen: dalber16@student.aau.dk

Rasmus Thomsen: rthoms16@student.aau.dk

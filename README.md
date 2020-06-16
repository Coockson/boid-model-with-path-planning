# boid-model-with-path-planning

## How to run the simulator

To run the simulator, the swarm_simulator.py file must be executed. The parameters of the command line can be seen by running

```
python swarm_simulator.py -h
```

### Mandatory fields

```
python swarm_simulator.py <path to configuration space> <starting coordinate> <goal coordinate>
```
### Default parameters

- **Centering factor** 0.12

- **Seperation factor** 0.30

- **Alignment factor** 0.05

- **Obstacle avoidance factor** 0.05

- **Goal follow factor** 0.08

- **Goal distance** 50

- **Minimum drone distance** 4

- **Speed limit** 3

- **Number of boids** 5

- **Visual range** 20

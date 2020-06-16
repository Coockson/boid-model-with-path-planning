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

### Additional fields

#### --path
Selects the path planning algorithm. Type "rrt*" or "a*" for the selection. For example,
```
python swarm_simulation.py "path/to/cs" "0,0" "50,50" --path "a*"
```
**Default** A*

#### --droneInit
Selects the start point of the swarm. Type the coordinates in the form "x,y". For example,
```
python swarm_simulation.py "path/to/cs" "0,0" "50,50" --droneInit "40,40"
```
**Default** (0,0)

#### --droneSpread
Selects the initial random spread of the swarm. Type the int value for radius (in pixels). For example,
```
python swarm_simulation.py "path/to/cs" "0,0" "50,50" --droneSpread 10
```
**Default** 5

#### --aStarReso
Selects the resolution value for the a star algorithm if needed. Type the int value for resolution. For example,
```
python swarm_simulation.py "path/to/cs" "0,0" "50,50" --droneInit "40,40"
```
**Default** 5

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

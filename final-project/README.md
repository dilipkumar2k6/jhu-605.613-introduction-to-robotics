# Final Project

## Project
For the final project you will create a robot which can successfully traverse a mazelike environment in the Gazebo simulation environment. All the instructions on how to download, install, and run the code can be found in the zip file attached to this assignment.

**Mission:** Navigate a robot across an unexplored environment to multiple goal locations

**Assignment:** Write a controller, planner, and mapper in ROS2 to get to the goal

**Template:** Can be found under Final Project course model (`template_with_maps.zip`)
* Launch files for starting Gazebo and ROS
* Default Map
* Default Robot
* Differential Drive
* 2D Lidar Sensor

A robot should be capable of navigating all the maps. `Maze_ql_1`, `Maze_ng`, and `Maze_hr`. These maps can be launched with the following command line arguments. Each map contains 3 goals which the robot must attempt to reach. These goals can be approached in any order.

```bash
ros2 launch gazebo_controller full_simulation.launch.py map_folder:=Maze_hr
```
```bash
ros2 launch gazebo_controller full_simulation.launch.py map_folder:=Maze_ng
```
```bash
ros2 launch gazebo_controller full_simulation.launch.py map_folder:=Maze_ql_1
```

Students will be required to record a video of their robot in action that they will share with the class. This video should each of the 3 scenarios available for different robot starting positions and goal positions. If the robot is significantly slower than real-time then the video should be sped up to take fewer than 2 minutes.

Students will give a short 5 minute presentation to the class covering their approach and sharing the video of their robot. The format:

1. **5 minute presentation**
    1. 3-4 Slides
    2. 1-2 minute video of the robot in action.
2. **Discuss the following**
    1. Any changes you made to the robot model from the default
    2. What algorithm did you use?
    3. What was your ROS node architecture?
    4. What challenges did you encounter?
        1. Technical challenges with ROS
        2. Challenges implementing the algorithm
    5. What would you do to improve your system if you had more time?

You are free to alter the robot in any way you need or introduce elements into the gazebo world to aid in localization. You may not edit the map itself and you may not use third-party packages without instructor approval.

**All Students must submit:**

1. All source code.
2. 1-2 page document explaining the approach, and how to run the code. Please include any information such as run environment or other package dependencies.
3. Videos of the robot in action executing 2 of the 4 scenarios defined by the `README.md` file.
4. Video of the student giving the presentation
5. Slides used for the class presentation.

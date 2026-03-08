# Gazebo Control Package

This ROS 2 package (`gazebo_control`) contains the simulation environment and control nodes for a custom differential drive robot.

## Features
- **Gazebo Simulation:** Spawns a custom `basic_robot` URDF into a simulated world (`my_world.sdf`).
- **RViz2 Visualization:** Automatically loads a pre-configured RViz setup (`my_robot.rviz`) to visualize the robot's odometry, TF tree, and LiDAR data.
- **PID Controller:** Includes a custom PID controller node (`diffdrive_pid`) that allows you to command the robot to a specific location using the "2D Goal Pose" tool in RViz.
- **ROS-Gazebo Bridge:** Seamlessly bridges topics between Gazebo and ROS 2 (e.g., `/cmd_vel`, `/scan`, `/tf`, `/joint_states`).

## Setup ROS2
Launch the ROS2 container with the following command:
```
docker run   -p 6080:80   -p 8888:8888   -v "$PWD/gazebo:/home/ubuntu/gazebo"   --name en613_ros2_jazzy   tiryoh/ros2-desktop-vnc:jazzy
```

Then launch Ubuntu in browser http://127.0.0.1:6080/ 

## How to Run

You can launch the entire simulation (Gazebo, RViz, the ROS-Gazebo bridge, and the PID controller) with a single command. 

1. **Build the workspace** (if you haven't already):
   ```bash
   cd /home/ubuntu/gazebo
   colcon build --packages-select gazebo_control
   ```

2. **Source your workspace:**
   ```bash
   source install/setup.bash
   ```

3. **Launch the simulation:**
   ```bash
   ros2 launch gazebo_control spawn_robot.launch.py
   ```

Once everything is running, use the **"2D Goal Pose"** tool in the RViz window to click and drag a destination for the robot. The PID controller will automatically navigate the robot to that location in Gazebo.

## Demo

Watch the demo video here: [Demo Video](https://www.youtube.com/watch?v=6FtBXFig33U)

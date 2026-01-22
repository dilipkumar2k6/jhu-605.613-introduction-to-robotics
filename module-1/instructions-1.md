 
# ROS2 Jazzy Environment Setup with TurtleBot4 - Instructions (Version 3.0)
## Overview
This guide provides step-by-step instructions for setting up a ROS2 Jazzy environment with TurtleBot4 simulation using Docker and Gazebo Harmonic. These instructions have been tested and validated on Windows with PowerShell.
## Prerequisites
- Windows 10/11 with WSL2 enabled
- Docker Desktop installed and running
- At least 8GB RAM available for Docker
- 10GB free disk space
---
## Step 1: Installing ROS2 Jazzy and TurtleBot3 Sim

#### 1.1 Install Docker on your computer
Download and install Docker Desktop from: https://docs.docker.com/get-docker/
**Verify Docker installation:**
```powershell
docker --version
```
#### 1.2 Create a workspace folder

You will need to create a folder where you will be developing all the code for this course.
This folder will be mounted by the Docker container which will allow you to run the code in the correct environment.
This step is necessary as data inside a docker container does not persist once the docker container is shut down 
unless it is inside a mounted folder. 

#### 1.3 Pull the ROS2 Jazzy Docker image
```powershell
docker pull tiryoh/ros2-desktop-vnc:jazzy
```
This image has Ubuntu and ROS2 Jazzy preinstalled along with a VNC interface that allows you to view the desktop in your browser.
#### 1.4 Start the Docker container
**Windows PowerShell Command:**
```powershell
docker run`
  -p 6080:80 `
  -p 8888:8888 `
  -v "<Class Workspace Folder>:/home/ubuntu/EN613" `
  --name en613_ros2_jazzy `
  tiryoh/ros2-desktop-vnc:jazzy
```

This will launch in non-interactive mode, running in the background. 

**Command Explanation:**
- `-p 6080:80`: Map port 6080 for VNC access
- `-p 8888:8888`: Map port 8888 for jupyter notebook use later in the course
- `-v "C:\EN613:/home/ubuntu/EN613"`: Mount your local folder to the container
- `--name ros2_jazzy_tb4`: Assign a specific name to the container
- `--security-opt seccomp=unconfined`: Required for Ubuntu compatibility

#### 1.5 Access the VNC interface
Open your browser and navigate to: http://127.0.0.1:6080/
You should see the Ubuntu desktop running in Docker.

#### 1.6 Install Gazebo Harmonic and TurtleBot3
##### Option 1. Connect to the terminal via docker exec
**Open a new PowerShell terminal** and connect to the running container:
```powershell
docker exec -it en613_ros2_jazzy bash
```
This will log you in as root so you will need to switch to the ubuntu user account using the following command.
```bash
su ubuntu
```
**Inside the container, run the following commands:**
1. **Update the system:**
```bash
sudo apt update && sudo apt upgrade -y
```
2. **Install Gazebo Harmonic (if not already installed):**
```bash
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
gz sim --version
```
3. **Install ROS2-Gazebo bridge packages:**

```bash
# Install ROS2 Gazebo integration packages
sudo apt install -y ros-${ROS_DISTRO}-ros-gz-*
sudo apt install python3-colcon-common-extensions
```
4. **Install TurtleBot3 simulation packages:**
Follow the instructions here for the version of ROS you have installed. I've replicated them here for your conveinence.
https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/


We will skip the steps for installing Cartographer and Navigation for the moment.

```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src/
git clone -b ${ROS_DISTRO} https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b ${ROS_DISTRO} https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b ${ROS_DISTRO} https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b ${ROS_DISTRO} https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git

cd ~/turtlebot3_ws
colcon build --symlink-install
echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

#### 1.7 Setup environment variables

**Add the following lines to your bashrc:**
```bash
echo 'source /opt/ros/${ROS_DISTRO}/setup.bash' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
echo 'export GZ_VERSION=harmonic' >> ~/.bashrc
source ~/.bashrc
```

#### 1.8 Test the simulator

**Test with Empty world:**
```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
source ~/turtlebot3_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py

```

**Test with TurtleBot3 world:**
```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
source ~/turtlebot3_ws/install/setup.bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

```

Open up a second terminal to drive the robot around.
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

**Expected Output:**
- You should see log messages indicating Gazebo is starting
- The TurtleBot3 robot should spawn in the simulation
- Topics like `/cmd_vel`, `/odom`, `/scan`, `/battery_state` should be available

---
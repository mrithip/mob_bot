# Mobile Robot (mob_bot) - ROS2 Autonomous Navigation

A comprehensive ROS2 mobile robot package featuring SLAM (Simultaneous Localization and Mapping) and Nav2 (Navigation2) integration for autonomous navigation. This package includes support for multiple sensors (LiDAR, Camera, Depth Camera) and provides complete simulation and visualization capabilities.

## Features

- **Multi-Sensor Support**: LiDAR, RGB Camera, Depth Camera
- **SLAM Integration**: Real-time mapping using slam_toolbox
- **Autonomous Navigation**: Nav2 stack for path planning and obstacle avoidance
- **Simulation Ready**: Gazebo simulation with custom worlds
- **Visualization**: Complete RViz configurations for all sensors
- **Teleoperation**: Manual control for testing and mapping
- **GUI Control Interface**: Web-based GUI for robot control ([turtlebot3_gui](https://github.com/mrithip/turtlebot3_gui))

## Prerequisites

### System Requirements
- Ubuntu 20.04/22.04
- ROS2 Humble/Foxy
- Gazebo (installed with ROS2)

### ROS2 Dependencies Installation
```bash
# Update package list
sudo apt update

# Install ROS2 Navigation2 and SLAM Toolbox
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox

# Install teleoperation tools
sudo apt install ros-humble-teleop-twist-keyboard

# Install visualization tools
sudo apt install ros-humble-rviz2
```

## Installation and Setup

### 1. Clone and Build
```bash
# Navigate to your ROS2 workspace
cd ~/ros/dev_ws/src

# Clone this repository
git clone <your-repo-url> mob_bot

# Navigate back to workspace root
cd ~/ros/dev_ws

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build the package
colcon build --packages-select mob_bot

# Source the workspace
source install/setup.bash
```

### 2. Directory Structure
```
mob_bot/
├── config/           # RViz configurations and Nav2 parameters
│   ├── lidar.rviz
│   ├── camera_uncompressed.rviz
│   ├── depth_cam.rviz
│   ├── drive_bot.rviz
│   ├── nav2_params.yaml
│   └── view_bot.rviz
├── description/      # Robot URDF/XACRO files
│   ├── robot.urdf.xacro
│   ├── robot_core.xacro
│   ├── gazebo_control.xacro
│   ├── lidar.xacro
│   ├── camera.xacro
│   └── depth_camera.xacro
├── launch/           # Launch files for different operations
│   ├── rsp.launch.py
│   ├── launch_sim.launch.py
│   ├── slam.launch.py
│   └── navigation.launch.py
├── maps/             # Saved maps from SLAM
├── worlds/           # Gazebo world files
│   ├── empty.world
│   └── obstacles.world
└── CMakeLists.txt
```

## Robot Configuration

### Sensor Options

The robot supports three sensor configurations. Modify `robot.urdf.xacro` to enable/disable sensors:

#### 1. LiDAR Only (Recommended for SLAM)
```xml
<!-- Enable LiDAR -->
<xacro:include filename="lidar.xacro"/>

<!-- Comment out other sensors -->
<!-- <xacro:include filename="camera.xacro"/> -->
<!-- <xacro:include filename="depth_camera.xacro"/> -->
```

#### 2. RGB Camera Only
```xml
<!-- Comment out LiDAR -->
<!-- <xacro:include filename="lidar.xacro"/> -->

<!-- Enable Camera -->
<xacro:include filename="camera.xacro"/>
```

#### 3. Depth Camera Only
```xml
<!-- Comment out LiDAR -->
<!-- <xacro:include filename="lidar.xacro"/> -->

<!-- Enable Depth Camera -->
<xacro:include filename="depth_camera.xacro"/>
```

#### 4. Multi-Sensor Setup
```xml
<xacro:include filename="lidar.xacro"/>
<xacro:include filename="camera.xacro"/>
<xacro:include filename="depth_camera.xacro"/>
```

### Sensor Specifications

#### LiDAR (`lidar.xacro`)
- **Type**: 2D Laser Scanner
- **Range**: 0.3m - 12m
- **Angle**: 360° (full circle)
- **Resolution**: 1° (360 samples)
- **Topic**: `/scan`
- **Message Type**: `sensor_msgs/LaserScan`
- **Update Rate**: 10 Hz

#### RGB Camera (`camera.xacro`)
- **Resolution**: 640x480
- **FOV**: 108.9°
- **Format**: RGB8
- **Topic**: `/camera/image_raw`
- **Message Type**: `sensor_msgs/Image`

#### Depth Camera (`depth_camera.xacro`)
- **Provides**: Depth/pointcloud data
- **Topics**: Various depth-related topics
- **Message Types**: `sensor_msgs/Image`, `sensor_msgs/PointCloud2`

## Running the Robot

### 1. Basic Simulation (Empty World)
```bash
# Terminal 1
cd ~/ros/dev_ws
source install/setup.bash
ros2 launch mob_bot launch_sim.launch.py
```

### 2. Simulation with Obstacles
The launch files automatically use the `obstacles.world` which contains:
- 5 cylindrical obstacles
- 4 box obstacles
- Realistic environment for testing

### 3. Robot State Publisher Only
```bash
ros2 launch mob_bot rsp.launch.py
```

## Sensor Data Visualization in RViz

### LiDAR Visualization
```bash
# Launch simulation first, then in new terminal:
rviz2 -d src/mob_bot/config/lidar.rviz
```
![](https://github.com/mrithip/mob_bot/raw/main/assets/lidar.mp4)

**What you'll see:**
- **Robot Model**: 3D visualization of the robot
- **LaserScan**: Red points showing distance measurements
- **TF Frames**: Coordinate frames for odom, base_link, laser_frame
- **Map**: If SLAM is running, shows the built map

**Key RViz Displays:**
- `LaserScan` → Topic: `/scan`
- `TF` → Show all frames enabled
- `RobotModel` → Description Source: `robot_description`

### RGB Camera Visualization
```bash
# Launch simulation with camera enabled, then:
rviz2 -d src/mob_bot/config/camera_uncompressed.rviz
```

![](https://github.com/mrithip/mob_bot/raw/main/assets/cam.mp4)

**What you'll see:**
- **Camera Image**: Live RGB camera feed
- **Camera Frustum**: Field of view visualization
- **TF Frames**: Camera coordinate frames

**Key RViz Displays:**
- `Image` → Topic: `/camera/image_raw`
- `Camera` → Topic: `/camera/image_raw`

### Depth Camera Visualization
```bash
# Launch simulation with depth camera enabled, then:
rviz2 -d src/mob_bot/config/depth_cam.rviz
```
![](https://github.com/mrithip/mob_bot/raw/main/assets/depthcam.mp4)

**What you'll see:**
- **Depth Cloud**: Point cloud from depth sensor
- **Depth Image**: Grayscale depth visualization

### General Robot View
```bash
rviz2 -d src/mob_bot/config/view_bot.rviz
```

### Teleoperation View
```bash
rviz2 -d src/mob_bot/config/drive_bot.rviz
```

## GUI Control Interface

For a user-friendly desktop GUI control interface, use the companion [turtlebot3_gui](https://github.com/mrithip/turtlebot3_gui) repository. This Python-based GUI using PyQt5 provides:

- **Real-time Odometry Display**: Shows current robot position (x, y coordinates)
- **Velocity Control**: Interactive buttons for forward/backward movement and rotation
- **Speed Control**: Adjustable sliders for linear and angular velocities (0-1.0 m/s, 0-1.0 rad/s)
- **Live Velocity Graphs**: Real-time visualization of linear and angular velocities
- **Trajectory Mapping**: Interactive plot showing robot's movement path over time
- **Dark Theme**: Modern dark UI design for comfortable viewing

### GUI Installation and Usage

1. **Clone the GUI repository**:
   ```bash
   cd ~/ros/dev_ws/src
   git clone https://github.com/mrithip/turtlebot3_gui.git
   ```

2. **Install Python dependencies**:
   ```bash
   pip install PyQt5 matplotlib numpy
   ```

3. **Install GUI ROS2 dependencies**:
   ```bash
   cd ~/ros/dev_ws
   rosdep install --from-paths src --ignore-src -r -y
   colcon build --packages-select tb3_gui
   source install/setup.bash
   ```

4. **Launch the robot simulation**:
   ```bash
   # Terminal 1: Launch robot
   ros2 launch mob_bot launch_sim.launch.py
   ```

5. **Launch the GUI**:
   ```bash
   # Terminal 2: Launch GUI
   ros2 run tb3_gui tb3_gui_node
   ```

### GUI Controls

#### Movement Controls
- **Forward**: Move robot forward at selected linear speed
- **Backward**: Move robot backward at selected linear speed
- **Left**: Rotate robot counter-clockwise at selected angular speed
- **Right**: Rotate robot clockwise at selected angular speed
- **Stop**: Immediately halt all robot movement

#### Speed Adjustment
- **Linear Speed Slider**: Controls forward/backward movement speed (0-1.0 m/s)
- **Angular Speed Slider**: Controls rotation speed (0-1.0 rad/s)

#### Visualization
- **Velocity Graph**: Shows real-time linear and angular velocity
- **Trajectory Plot**: Displays robot's path over time
- **Odometry Display**: Current position coordinates (x, y)

### ROS2 Topics Used
- **Subscribed**: `/odom` (nav_msgs/Odometry) - Robot odometry information
- **Published**: `/cmd_vel` (geometry_msgs/Twist) - Velocity commands to robot

The GUI works seamlessly with the mob_bot package and provides an intuitive alternative to keyboard teleoperation for robot control and monitoring.

## SLAM (Simultaneous Localization and Mapping)

### SLAM Workflow Overview
1. **Mapping Phase**: Drive robot to build map
2. **Localization Phase**: Use existing map for navigation
3. **Save/Load**: Persist maps for later use

### 1. SLAM Mapping (Create New Map)
```bash
# Terminal 1: Launch SLAM with simulation and teleop
cd ~/ros/dev_ws
source install/setup.bash
ros2 launch mob_bot slam.launch.py

# Terminal 2: Optional - Visualize in RViz
rviz2 -d src/mob_bot/config/lidar.rviz
```

**Teleoperation Controls** (in the teleop terminal):
```
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
```

**Mapping Tips:**
- Drive systematically covering all areas
- Go slow for better accuracy
- Cover overlapping areas for loop closure
- Map in both directions for better coverage

### 2. Save the Map
```bash
# In a new terminal (while SLAM is running)
cd ~/ros/dev_ws
source install/setup.bash
ros2 run nav2_map_server map_saver_cli -f my_map
```

This creates:
- `my_map.pgm` - Occupancy grid image
- `my_map.yaml` - Map metadata and configuration

### 3. SLAM Localization (Using Existing Map)
Modify the launch file or create a localization launch:
```bash
# Change mode from 'mapping' to 'localization' in slam.launch.py
# Add map_file_name parameter pointing to your saved map
```

## Autonomous Navigation with Nav2

### Prerequisites
- Completed SLAM map (saved as `my_map.yaml` and `my_map.pgm`)
- Map files placed in `src/mob_bot/maps/` directory

### 1. Launch Autonomous Navigation
```bash
# Terminal 1: Launch navigation stack
cd ~/ros/dev_ws
source install/setup.bash
ros2 launch mob_bot navigation.launch.py

# Terminal 2: Launch RViz for navigation
rviz2 -d src/mob_bot/config/view_bot.rviz
```

### 2. Set Navigation Goal in RViz
1. **Select Tool**: Click "2D Goal Pose" button in RViz toolbar
2. **Set Goal**: Click and drag in the map to set:
   - **Position**: Where you want the robot to go
   - **Orientation**: Direction the robot should face when it arrives
3. **Watch Navigation**: Robot will:
   - Plan a path (green line)
   - Avoid obstacles
   - Navigate autonomously to the goal

### 3. Monitor Navigation Topics
```bash
# Check navigation status
ros2 topic echo /navigate_to_pose/_action/status

# View current goal
ros2 topic echo /goal_pose

# Monitor velocity commands
ros2 topic echo /cmd_vel
```

## 🔧 Configuration Files

### Nav2 Parameters (`config/nav2_params.yaml`)
- **Global Costmap**: Static map layer for known obstacles
- **Local Costmap**: Dynamic obstacle avoidance
- **Controller**: Path following and velocity control
- **Planner**: Global path planning
- **Behavior Tree**: Navigation logic flow

### RViz Configurations
- **`lidar.rviz`**: LiDAR scanning and mapping visualization
- **`camera_uncompressed.rviz`**: RGB camera feed
- **`depth_cam.rviz`**: Depth/pointcloud visualization
- **`drive_bot.rviz`**: Teleoperation interface
- **`view_bot.rviz`**: General robot monitoring

## Troubleshooting

### Common Issues

#### 1. Launch File Not Found
```bash
# Ensure you're in the correct directory and sourced
cd ~/ros/dev_ws
source install/setup.bash
```

#### 2. Gazebo Not Loading World
- Check that world file exists: `ls src/mob_bot/worlds/`
- Ensure Gazebo is properly installed

#### 3. SLAM Not Building Map
- Check LiDAR topic: `ros2 topic list | grep scan`
- Verify robot is moving: check `/odom` topic
- Ensure proper TF tree: `ros2 run tf2_tools view_frames`

#### 4. Navigation Not Working
- Verify map exists in `src/mob_bot/maps/`
- Check Nav2 parameters in `config/nav2_params.yaml`
- Ensure proper sensor data is publishing

#### 5. RViz Not Showing Data
- Check topic names match between publishers and RViz
- Verify QoS settings (reliable vs best effort)
- Ensure proper TF transforms are published

### Useful Debug Commands
```bash
# Check running nodes
ros2 node list

# Check topics
ros2 topic list

# Check TF tree
ros2 run tf2_tools view_frames

# Monitor specific topic
ros2 topic echo /scan

# Check service availability
ros2 service list

# View parameter values
ros2 param list /slam_toolbox
```

## Advanced Usage

### Custom World Creation
Create new worlds in `worlds/` directory and modify launch files to use them.

### Sensor Fusion
Combine multiple sensors by enabling them in `robot.urdf.xacro` and updating configurations.

### Custom Navigation Behaviors
Modify `nav2_params.yaml` to adjust:
- Robot speed limits
- Obstacle avoidance sensitivity
- Path planning algorithms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review ROS2 and Nav2 documentation
3. Open an issue with detailed information about your setup and the problem

---

**Note**: This documentation assumes ROS2 Humble installation. Commands may vary slightly for different ROS2 distributions.

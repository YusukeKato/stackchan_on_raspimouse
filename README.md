# stackchan_on_raspimouse
StackChan on Raspberry Pi Mouse

- [M5Stack/StackChan](https://docs.m5stack.com/en/StackChan)
- [RT/Raspberry Pi Mouse V3](https://rt-net.jp/products/raspberrypimousev3/)

<img width="570" height="478" alt="StackChan on Raspberry Pi Mouse" src="https://github.com/user-attachments/assets/7004b34e-7af4-44ba-b77c-c39a2fbeb0d1" />

## Development Environment
- [stack-chan_micro-ros_arduino: development-enviroment](https://github.com/YusukeKato/stack-chan_micro-ros_arduino#development-environment)

## Setup
- [stack-chan_micro-ros_arduino: setup](https://github.com/YusukeKato/stack-chan_micro-ros_arduino#setup)
- [Raspberry Pi Mouse: tutorials](https://rt-net.github.io/tutorials/raspimouse/products.html)

## Build
```sh
mkdir -p ~/stackchan_ws/src
cd ~/stackchan_ws/src
git clone https://github.com/YusukeKato/stackchan_on_raspimouse.git
cd ~/stackchan_ws
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build
source install/setup.bash
```

## Usage
Start the micro-ROS agent:
```sh
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888 -v6
```

Start Raspberry Pi Mouse:
[GitHub - rt-net/raspimouse2](https://github.com/rt-net/raspimouse2)

### Face Tracker
Start face tracking:
```sh
source install/setup.bash
ros2 run stackchan_on_raspimouse face_tracker_node
```

<img width="400" height="225" alt="face tracking" src="https://github.com/user-attachments/assets/25f4972c-a510-4adb-8b5f-a3fe789a76eb" />

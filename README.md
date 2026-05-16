# stackchan_on_raspimouse
StackChan on Raspberry Pi Mouse

## Build
```sh
mkdir -p ~/stackchan_ws/src
cd ~/stackchan_ws/src
git clone
cd ~/stackchan_ws
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build
source install/setup.bash
```

## Usage
Terminal 1:
```sh
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888 -v6
```

Terminal 2:
```sh
source install/setup.bash

```
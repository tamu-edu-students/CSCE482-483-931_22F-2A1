FROM ubuntu:20.04
WORKDIR /root
ENTRYPOINT ["/bin/bash","/root/startVNC.sh"]


# ROS Installation
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl gnupg2 lsb-release sudo && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    /bin/bash -c "echo 'deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -sc) main' | tee /etc/apt/sources.list.d/ros2.list > /dev/null" && \
    /bin/bash -c "echo 'deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main' | tee /etc/apt/sources.list.d/ros.list > /dev/null" && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install vim tmux git qt5-default ros-foxy-desktop ros-noetic-desktop-full tigervnc-standalone-server novnc openbox lxpanel && \
    apt-get clean && \
    echo "export DISPLAY=:1" >> .bashrc && \
    echo "source /opt/ros/foxy/setup.bash" > /root/foxy_setup.sh && \
    echo "source /opt/ros/noetic/setup.bash" > /root/noetic_setup.sh && \
    /bin/bash -c "echo -e 'password\npassword\nn' | vncpasswd" && \
    openssl req -x509 -nodes -newkey rsa:3072 -keyout novnc.pem -out novnc.pem -days 3650 -subj "/C=NA/ST=NA/L=NA/O=NA/OU=NA/CN=NA/emailAddress=NA" && \
    printf "rm -rf /tmp/.X1* \ntigervncserver :1 -xstartup /root/.xinit \n websockify --web=/usr/share/novnc/ -D --cert=novnc.pem 6081 127.0.0.1:5901 \n /bin/bash" > startVNC.sh && \
    printf "lxpanel &\n sleep 3 \n openbox-session" >.xinit && \
    chmod 777 /root/*.sh /root/.xinit

# HybridNets Setup
RUN apt-get update && \
    apt-get -y install \
    # Installing Python3 Pip
    python3-pip && \
    # echo "echo "Worked"" >> .bashrc
    # Installing dependancies for 
    pip install -qr https://raw.githubusercontent.com/datvuthanh/HybridNets/main/requirements.txt

# Cloning Repo and using latest rootfs folder
# RUN apt-get update && \
#     git clone --recursive https://github.com/tamu-edu-students/CSCE482-483-931_22F-2A1 && \
#     mv CSCE482-483-931_22F-2A1/rootfs rootfs && \
#     rm -rf CSCE482-483-931_22F-2A1

# ROS Setup
# To cd into a directory, do not use command "cd". Use WORKDIR as that is best practice
# ARG CACHE_BUST
# RUN echo "source /root/noetic_setup.sh" >> .bashrc 
# WORKDIR /root/rootfs/rootfs/catkin_ws/devel
# RUN echo "source setup.bash" >> .bashrc
# WORKDIR /root/rootfs/rootfs/catkin_ws
# RUN echo "catkin_make" >> .bashrc
# WORKDIR /root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/scripts
# CMD ["rm -rf HybridNets","git clone https://github.com/datvuthanh/HybridNets"]
# RUN rm -rf HybridNets && \
#     git clone https://github.com/datvuthanh/HybridNets
# COPY . .

# WORKDIR /root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/scripts/HybridNets
# RUN echo "ls" >> .bashrc
# WORKDIR /root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/scripts
# RUN echo "roscore & ros_basics_tutorials image_subscriber.py" >> .bashrc
# Example: 
# RUN echo "python3 image_subscriber.py" >> .bashrc

# CMD ["python3", "image_subscriber.py"]
# RUN echo "" >> .bashrc
# RUN echo "rosrun ros_basics_tutorials image_subscriber.py" >> .bashrc
# /root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/scripts
# WORKDIR /root
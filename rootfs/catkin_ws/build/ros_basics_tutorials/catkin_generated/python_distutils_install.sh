#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/root/rootfs/rootfs/catkin_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/root/rootfs/rootfs/catkin_ws/install/lib/python3/dist-packages:/root/rootfs/rootfs/catkin_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/root/rootfs/rootfs/catkin_ws/build" \
    "/usr/bin/python3" \
    "/root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/setup.py" \
    egg_info --egg-base /root/rootfs/rootfs/catkin_ws/build/ros_basics_tutorials \
    build --build-base "/root/rootfs/rootfs/catkin_ws/build/ros_basics_tutorials" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/root/rootfs/rootfs/catkin_ws/install" --install-scripts="/root/rootfs/rootfs/catkin_ws/install/bin"

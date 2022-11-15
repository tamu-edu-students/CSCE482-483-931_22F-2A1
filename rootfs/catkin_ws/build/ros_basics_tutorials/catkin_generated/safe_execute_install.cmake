execute_process(COMMAND "/root/rootfs/rootfs/catkin_ws/build/ros_basics_tutorials/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/root/rootfs/rootfs/catkin_ws/build/ros_basics_tutorials/catkin_generated/python_distutils_install.sh) returned error code ")
endif()

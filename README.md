# CSCE482-483-931_22F-2A1

<!-- ## Team: 2A1. Traffic Object/Lane Detection -->

<!-- <img src="logo.png" alt="Team Logo" width="25%" height="auto"> -->


<p align="center">
  <a>
    <img src="Reports/Assets/logo.png" alt="Team Logo" width="300" height="auto">
  </a>
  <h3 align="center">2A1. Traffic Object/Lane Detection</h3>
  <!-- <p align="center">
    Mini Description Here...
  </p> -->
</p>

## About the Project
todo

### Objectives: 
* Evaluate existing detection framework on our dataset
* Integrate existing detection framework with ROS/ROS2
* Input: image, Output: bounding boxes/classification results


## Prerequisites
* Operating System: Mac, Linux, or Windows
* Docker [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
* GitHub Account [https://github.com/join](https://github.com/join)


## Getting Started
Clone the repository:

```bash
git clone https://github.com/tamu-edu-students/CSCE482-483-931_22F-2A1
cd CSCE482-483-931_22F-2A1
```

Initialize the latest Docker container from image
```bash
make init
```



### Useful Commands  (For Development Purposes Only)
If a package already exists with the name 2a1-package, you can remove it using the following command:
```bash
make rm
```

If updating Dockerfile, use the following command to build your own image:
```bash
make build
```

To run docker container, use:
```bash
make run
```

You can also pull the latest Docker package using the following command:
```bash
docker pull ghcr.io/ojasonbernal/2a1-package:latest
```

### Disclaimer: 
Unable to associate GitHub Docker Package to repository due to restrictions from tamu-edu-students organization. \
Docker Package can be found here:
[https://github.com/users/ojasonbernal/packages/container/package/2a1-package](https://github.com/users/ojasonbernal/packages/container/package/2a1-package)

## Contributors:
Team Name: OLD482
* Pavan Poladi [https://github.com/pavanpoladi](https://github.com/pavanpoladi)
* Khai Nguyen [https://github.com/Khaihuyennguyen](https://github.com/Khaihuyennguyen)
* Viet Nguyen [https://github.com/vivelaviet](https://github.com/vivelaviet)
* Jason Bernal [https://github.com/ojasonbernal](https://github.com/ojasonbernal)


## License
todo

## Acknowledgements:
* [HybridNets](https://github.com/datvuthanh/HybridNets)
* [Darknet-ROS](https://github.com/leggedrobotics/darknet_ros)
* [ROS-Docker-Intro](https://github.com/tamu-edu-students/ROS-Docker-Intro)


### Resources Used:
* Learn Docker in 7 Easy Steps - Full Beginner's Tutorial [https://www.youtube.com/watch?v=gAkwW2tuIqE](https://www.youtube.com/watch?v=gAkwW2tuIqE)
* ROS Tutorial 5 (ROS1) - Write a ROS Node with Python [https://www.youtube.com/watch?v=jWtkzDbez9M](https://www.youtube.com/watch?v=jWtkzDbez9M)
* How to setup ROS with Python 3 [https://medium.com/@beta_b0t/how-to-setup-ros-with-python-3-44a69ca36674](https://medium.com/@beta_b0t/how-to-setup-ros-with-python-3-44a69ca36674)
* https://www.freecodecamp.org/news/docker-cache-tutorial/

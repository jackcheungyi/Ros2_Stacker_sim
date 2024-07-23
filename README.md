# Ros2_Stacker_sim
---
This is a simulation project integrating ros2_control, navigation2_Stack, and cartographer_ros for testing stacker-like robots.
---
## Stacker URDF 
A simple urdf is drawn for modeling
\
run
```ruby
ros2 launch stacker_description display_simple.launch.py
```
to preview the urdf model 
![rviz2_Demo](https://github.com/user-attachments/assets/788ea1c6-16c7-4dc0-9742-1b4e835b53a8)

---
## Drive the robot 
run 
```ruby
ros2 launch stacker_description stacker_drive.launch.py
```
and run teleop keyboard control in another terminal 
```ruby
 ros2 run teleop_twist_keyboard teleop_twist_keyboard cmd_vel:=/tricycle_controller/cmd_vel
```

https://github.com/user-attachments/assets/740cb77a-9e43-4efc-ba68-ee631ea03171

---
## Scan Map 
run 
```ruby
ros2 launch stacker_description stacker_drive.launch.py
```
and run cartographer node in another terminal 
```ruby
 ros2 launch stacker_cartographer cartographer.launch.py 
```

https://github.com/user-attachments/assets/2e38c80e-9a61-43d7-80ff-6297b9e027d0

---
## Navigation 
run 
```ruby
ros2 launch stacker_description stacker_drive.launch.py
```
and run navigation node in another terminal 
```ruby
 ros2 launch stacker_nav2 stacker_nav2.launch.py
```

https://github.com/user-attachments/assets/6ba8e08e-517e-4152-8891-00401c233ed5

---

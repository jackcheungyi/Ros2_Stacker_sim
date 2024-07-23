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

https://github.com/user-attachments/assets/2344ef1e-f3d9-495c-8266-478cd94b5cc6

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


https://github.com/user-attachments/assets/a9e2742f-c2d3-44c7-85ca-8ad487d30624


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

https://github.com/user-attachments/assets/6514163f-da6f-40c0-92f3-44c374566103

---

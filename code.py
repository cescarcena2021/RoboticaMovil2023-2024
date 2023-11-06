from GUI import GUI
from HAL import HAL
import math
import numpy as np
# Enter sequential code!


def absolute2relative (x_abs, y_abs, robotx, roboty, robott):

    # robotx, roboty are the absolute coordinates of the robot
    # robott is its absolute orientation
    # Convert to relatives
    dx = x_abs - robotx
    dy = y_abs - roboty

    # Rotate with current angle
    x_rel = dx * math.cos (-robott) - dy * math.sin (-robott)
    y_rel = dx * math.sin (-robott) + dy * math.cos (-robott)

    return x_rel, y_rel

def parse_laser(laser_data):
    laser = []
    i = 0
  
    for i, dist in enumerate(laser_data.values):
        angle = math.radians(i-90)
        laser += [(dist, angle)]
        i += 1
    return laser


def get_repulsive_force(parse_laser):

    laser_array = []
    for distance, angle in parse_laser:
      
        x = 1/distance * math.cos(angle) * -1
        y = 1/distance * math.sin(angle) * -1
        v = (x,y)

        laser_array += [v]
    laser_mean = np.mean(laser_array, axis=0)
    return laser_mean

while True:
    # Get the image 
    image = HAL.getImage()

    # Get the laser and parse it 
    laser_data = HAL.getLaserData()
    laser = parse_laser(laser_data)

    # Get the robot position
    robot_x = HAL.getPose3d().x
    robot_y = HAL.getPose3d().y
    robot_yaw = HAL.getPose3d().yaw
    
    # Get the target absolute position
    currentTarget = GUI.map.getNextTarget()
    absolute_x = currentTarget.getPose().x
    absolute_y = currentTarget.getPose().y
    
    # Transform the absolute target to the relative target
    relative_x, relative_y = absolute2relative(absolute_x,absolute_y,robot_x,robot_y,robot_yaw)
    relative_target = relative_x, relative_y
    
    # Car direction defined in a green vector
    atractive_vector = [max(min(relative_x, 3.5), -3.5), max(min(relative_y, 3.2), -3.2)]
    # Obstacle direction defined in a red vector
    repulsive_vector = [get_repulsive_force(laser)[0] * 3, get_repulsive_force(laser)[1] * 8]
    # Average direction defined in a black line
    total_vector = [(atractive_vector[0] + repulsive_vector[0]), (atractive_vector[1] + repulsive_vector[1]) * 0.3]


    if (relative_x < 2 and relative_y < 2):
        currentTarget.setReached(True)
  
    
    if(total_vector[0] < 0):
        #turnig state
        HAL.setW(5)
        HAL.setV(1)
        
    else:
        w_vel = math.tan(total_vector[1]/total_vector[0])
         
        HAL.setW(w_vel * 2)
        HAL.setV(total_vector[0])
        
    # Show everything
    GUI.showImage(image)
    GUI.showLocalTarget(relative_target)
    GUI.showForces(atractive_vector, repulsive_vector, total_vector)
    

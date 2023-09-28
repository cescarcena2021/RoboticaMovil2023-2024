from GUI import GUI
from HAL import HAL
import time
import random
import math


def parse_laser_data(laser_data):
    laser = []
    for i in range(180):
        dist = laser_data.values[i]
        angle = math.radians(i)
        laser += [(dist, angle)]
    return laser


def go_backwards():
    HAL.setV(-1)
    HAL.setW(0)
    return 0


def forwards():
    HAL.setV(2)
    HAL.setW(0)
    return 0


def spiral(radius):
    HAL.setV(1)
    HAL.setW(radius)


def turn():
    HAL.setV(0.5)
    HAL.setW(2.5)
    time.sleep(1)
    return 0


state = 0
# state 0 = spiral
# state 1 = go_backwards
# state 2 = forwards

state_start_time = time.time()
state_duration = random.uniform(0,4)
angle = 3
forward_speed = 0
time_max = random.uniform(2,5)

while True:
    laser_data = HAL.getLaserData()
    laser = parse_laser_data(laser_data)
    laser_dist = laser[90][0]
    # print(laser_dist)

    if laser_dist < 0.5:
        state = 1

    if state == 0:
        
        HAL.setV(forward_speed)
        HAL.setW(angle) 
        
        forward_speed += 0.01
        
        print(forward_speed)
        if (forward_speed > time_max) :
          state = 2
          forward_speed = 0
          time_max = random.uniform(2,5)

    if state == 1:
        go_backwards()
        if time.time() - state_start_time >= 1:
            state = 0
            state_start_time = time.time()  # Reinicia el temporizador

    if state == 2:
        forwards()
        
    #print(state)
import queue

import airsim

from delay import Delay
from image import Image
from input import Input

import random
import time

from onlyImage import OnlyImage


def delay():
    action = False
    delay_thread = Delay(args=(q_time, "hola"))
    delay_thread.start()
    if(q_time.get()):
        action = True


def resetSystem():
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

def up(position):
    position.z_val -= 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
    delay()

def down(position):

    position.z_val += 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
    delay()

def forward(position):

    position.x_val +=5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
    delay()

def back(position):

    position.x_val -=5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
    delay()

def left(position):

    position.y_val -= 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
    delay()

def right(position):

    position.y_val += 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
    delay()


while True:


    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    q_input = queue.Queue()
    q_image = queue.Queue()
    q_time  = queue.Queue()


    client.takeoffAsync().join()

    action = True

    #input_thread = Input(args=(client,q_input))
    #image_thread = Image(args=(client,q_image))

    #image_thread.start()
    #input_thread.start()

    image = OnlyImage(args=(client,q_image))

    while True:


        if client.simGetCollisionInfo().has_collided:
            print("CHOQUE")
            client.reset()
            break


        print(image.takePhoto())
        position = None


        if action:

            input = random.choice(['q','e','w','a','d'])

            try:

                position = client.simGetGroundTruthKinematics().position

                print(position)

                if input == 'q':
                    up(position)
                if input == 'e' and position.z_val < -4.5:
                    down(position)

                if input == 'w':
                    forward(position)

                if input == 'a':
                    left(position)

                if input == 'd':
                    right(position)

                if input == 's':
                    back(position)





            except RuntimeError:
               pass
               # print("IOLoop is already running")
            except BufferError:
                print("Existing exports of data: object cannot be re-sized")
                position = None






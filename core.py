import queue

import airsim

from image import Image
from input import Input



client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

q_input = queue.Queue()
q_image = queue.Queue()


client.takeoffAsync().join()

input_thread = Input(args=(client,q_input))
image_thread = Image(args=(client,q_image))

image_thread.start()
input_thread.start()



def up(position):
    position.z_val -= 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)

def down(position):
    position.z_val += 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
def forward(position):
    position.x_val +=5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
def back(position):
    position.x_val -=5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
def left(position):
    position.y_val -= 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)
def right(position):
    position.y_val += 5
    client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5, 5)


while True:

   if  not q_input.empty():

    input = q_input.get()
    position = None

    try:

        position = client.simGetGroundTruthKinematics().position

        print("al terminar ")
        print(position)

        if input == 'q':
            up(position)
        if input == 'e':
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
        print("IOLoop is already running")
    except BufferError:
        print("Existing exports of data: object cannot be re-sized")
        position = None







from soundscraper import Output
from os import path
from qhue import Bridge, QhueException, create_new_username
import random
from time import sleep

def initialize():
    print("Connecting to bridge...")
    bridge = None

    try:
        bridge = __create_bridge_conn("auth.txt", "192.168.0.10")
        sleep(1)

        for index in range(1, 4):
            bridge.lights[index].state(bri=1, transitiontime=0, on=True)
    except QhueException as exc:
        print(exc)
    return bridge

def __create_bridge_conn(authfile, bridgeIP):
    if path.exists(authfile):
        with open(authfile, "r") as cred_file:
            username = cred_file.read()
    else:
        print("Authfile does not exist! Creating new one...")
        try:
            username = create_new_username(bridgeIP)
        except QhueException as err:
            print(f"Error occurred while creating a new username: {format(err)}")
        # store the username in a credential file
        with open(authfile, "w") as cred_file:
            cred_file.write(username)

    return Bridge(bridgeIP, username)

class HueOutput(Output):
    def __init__(self, bridge, light_index):
        super().__init__()

        self.bridge = bridge
        self.light = self.bridge.lights[light_index]
        self.light_index = light_index
        self.state = True

        if self.bridge == None:
            raise Exception
    
    def __set_light(self, light, **kwargs):
        """
        kwargs:
        light:             Light resource to set (likely [0 - 2])
        bri:   [1 - 254]   Brightness of light
        hue:   [0 - 65535] The hue value is a wrapping value (Both 0 and 65535 are red, 25500 is green and 46920 is blue)
        sat:   [0 - 254]   Saturation. 254 is the most saturated (colored) and 0 is the least saturated (white).
        xy:    [x, y]      X and Y coordinates (floats in range [0, 1]) of a color in a CIE color space
        on:    bool        Light On/Off
        """

        light.state(**kwargs)

    def __flash_light(self, **kwargs):
        """kwargs same as set_light"""

        # self.__set_light(self.bridge.lights[self.light_index % 3 + 1], on = True)

        self.__set_light(self.bridge.lights[self.light_index % 3 + 1], bri=1)
        self.__set_light(self.bridge.lights[(self.light_index + 1) % 3 + 1], bri=1)
        self.__set_light(self.light, bri=255, **kwargs)

    def __bloop_light(self):
        self.__set_light(self.light, bri=255)
        self.__set_light(self.light, bri=0)

    def handler(self, label, pythostart_time, length):
        if self.light == None:
            print(label)
        else:
            #self.__flash_light(hue=random.randint(0, 65535))
            self.__bloop_light()

def get_number_lights():
    return 3

# def main():
#     from random import randint
#     from time import sleep

#     # check for a credential file / create conn
#     bridge = create_bridge_conn("auth.txt", "10.0.0.91")

#     # create a lights resource
#     lights = bridge.lights

#     # Turn on all lights, set brightness to max, min transition time
#     for index in range(1, 4):
#         set_light(lights[index], bri=254, transitiontime=0, on=True)
    
#     # Set random color on lights
#     for index in range(10):
#         set_light(lights[index % 3 + 1], hue=randint(0, 65535))
#         sleep(1)

#     # Flash random lights
#     for index in range(15):
#         flash_light(lights, index % 3 + 1, hue=randint(0, 65535))
#         sleep(1)

# if __name__ == "__main__":
#     main()
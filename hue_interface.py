from soundscraper import Output
from os import path
from qhue import Bridge, QhueException, create_new_username
import random

class HueOutput(Output):
    def __init__(self):
        super().__init__()
        self.auth_file_path = "auth.txt"
        self.address = "10.0.0.91"
        try:
            self.bridge = self.__create_bridge_conn(self.auth_file_path, self.address)
        except QhueException as exc:
            print(exc)
        else:
            self.lights = self.bridge.lights
        finally:
            self.bridge = self.lights = None
    
    def __create_bridge_conn(self, authfile, bridgeIP):
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

    def __flash_light(self, index, **kwargs):
        """kwargs same as set_light"""

        opp_lights = {0: 3, 1: 1, 2: 2}

        print("Unce")
        self.__set_light(self.lights[opp_lights[(index - 1) % 3]], on = False)
        self.__set_light(self.lights[opp_lights[(index - 2) % 3]], on = False)
        self.__set_light(self.lights[index], **kwargs, on = True)

    def handler(self, label, start_time, length):
        if self.lights == None:
            print(label)
        else:
            self.__flash_light(random.randint(0, len(self.lights)), 
                hue=random.randint(0, 65535),
                bri=254)

def get_number_lights():
    return 3 #TODO: @haydn implement this





# def main():
#     from random import randint
#     from time import sleep

#     # check for a credential file / create conn
#     bridge = create_bridge_conn("auth.txt", "10.0.0.91")"auth.txt"

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
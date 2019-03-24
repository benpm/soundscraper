from os import path
from qhue import Bridge, QhueException, create_new_username
from time import sleep

def createBridgeConn(authfile, bridgeIP):
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

def setLight(light, **kwargs):
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

def flashLight(lights, index, **kwargs):
    """kwargs same as setLight"""

    opp_lights = {0: 3, 1: 1, 2: 2}

    print("Unce")
    setLight(lights[opp_lights[(index - 1) % 3]], on = False)
    setLight(lights[opp_lights[(index - 2) % 3]], on = False)
    setLight(lights[index], **kwargs, on = True)
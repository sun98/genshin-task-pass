# %%
from ppadb.client import Client as AdbClient
from ppadb.client import Connection as AdbConnection
import PIL.Image as Image
import io
import cv2
import time
import numpy as np

# %%


def connect_device(host='127.0.0.1', port=5037):
    client = AdbClient(host, port)
    device = client.devices()[0]
    return device
# %%


@DeprecationWarning
def process_screencap(conn):
    image_bytes = conn.read_all().replace(b'\r\n', b'\n')
    print(len(image_bytes))
    with open('./image/test.png', 'wb') as f:
        f.write(image_bytes)
    image = cv2.imdecode(np.asarray(image_bytes, dtype='uint8'), cv2.IMREAD_COLOR)
    cv2.imshow("", image)
    cv2.waitKey(0)
    cv2.destroyWindow("")

# device.shell("screencap", handler=process_screencap)

# %%


def get_screencap(device):
    result = device.screencap()
    image = cv2.imdecode(np.asarray(result, np.uint8), cv2.IMREAD_COLOR)
    return image
# %%


def save_current_cap(device):
    image = get_screencap(device)
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    cv2.imwrite(f'./image/{current_time}.png', image)


# %%
if __name__ == '__main__':
    device = connect_device()
    current_image = get_screencap(device)
    print(current_image)

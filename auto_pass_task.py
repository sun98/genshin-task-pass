from ppadb.client import Client as AdbClient
import cv2
import time
import numpy as np


def connect_device(host='127.0.0.1', port=5037):
    client = AdbClient(host, port)
    device = client.devices()[0]
    return device


def get_screencap(device):
    result = device.screencap()
    image = cv2.imdecode(np.asarray(result, np.uint8), cv2.IMREAD_COLOR)
    return image


def save_current_cap(device):
    image = get_screencap(device)
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    cv2.imwrite(f'./image/{current_time}.png', image)


def match_icon(image, template, thr=0.9, log=True):
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > thr:
        top_left = max_loc
        w, h = template.shape[::-1]
        # bottom_right = (top_left[0] + w, top_left[1] + h)
        x, y = top_left[0]+w//2, top_left[1]+h//2
        if log:
            print(f'detected at {x} {y}, max_val={max_val}')
        return True, x, y
    else:
        if log:
            print(f'not detected, max_val={max_val}')
        return False, 0, 0


if __name__ == '__main__':
    device = connect_device()
    dialog_image = cv2.imread('./image/chat_icon.png', cv2.IMREAD_GRAYSCALE)
    playing_image = cv2.imread('./image/playing.png', cv2.IMREAD_GRAYSCALE)
    while True:
        current_image = get_screencap(device)
        current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        has_dialog, x, y = match_icon(current_image_gray, dialog_image)
        if has_dialog:
            device.shell(f'input tap {x} {y}')
        else:
            has_playing, _, _ = match_icon(current_image_gray, playing_image)
            if has_playing:
                device.shell('input tap 1170 1020')
        time.sleep(0.5)

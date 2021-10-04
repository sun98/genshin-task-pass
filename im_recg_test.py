# %%
import cv2
import numpy as np

# %%
test_image = cv2.imread('./image/2021-10-04-19-52-50.png')
# test_image = cv2.imread('./image/2021-10-04-19-33-18.png')
test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
template_image = cv2.imread('./image/playing.png', cv2.IMREAD_GRAYSCALE)
w, h = template_image.shape[::-1]

# %% multi matching
res = cv2.matchTemplate(test_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(test_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
cv2.imshow('result', test_image)
cv2.waitKey(0)
# %% single matching
res = cv2.matchTemplate(test_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
print(max_val, top_left, bottom_right)

cv2.rectangle(test_image, top_left, bottom_right, 255, 2)
cv2.imshow('result', test_image)
cv2.waitKey(0)

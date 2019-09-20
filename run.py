from PIL import Image
import json
import cv2
import numpy as np

case = '1'
#case = '2'

entry_name = 'entry' + case + '.jpeg'
texture_name = 'texture' + case + '.jpeg'
dot_file_name = 'dots' + case + '.json'
result_name = 'result' + case + '.png'

def transformation(matriz, x, y):
    new_x = matriz[0][0] * x + matriz[0][1] * y + matriz[0][2] * 1
    new_y = matriz[1][0] * x + matriz[1][1] * y + matriz[1][2] * 1
    new_z = matriz[2][0] * x + matriz[2][1] * y + matriz[2][2] * 1

    new_x = new_x/new_z
    new_y = new_y/new_z
    return [round(new_x, 0), round(new_y, 0)]

with open(dot_file_name) as json_file:
    data = json_file.read()

obj = json.loads(data)

texture = Image.open(texture_name)
texture_width = texture.size[0]
texture_height = texture.size[1]

entry_points = obj['entry']
texture_points = []

for ref_point in obj['texture']:
    texture_points += [[ref_point[0] * (texture_width - 1), ref_point[1] * (texture_height - 1)]]

src_pts = np.array(texture_points)
dst_pts = np.array(entry_points)

H, status = cv2.findHomography(src_pts, dst_pts)
H_inv = np.linalg.inv(H)

texture = texture.convert("RGBA")

entry = Image.open(entry_name)
entry = entry.convert("RGBA")

for x in range(entry.size[0]):
    for y in range(entry.size[1]):
        [x_trans, y_trans] = transformation(H_inv, x, y)

        if y_trans > 0 and y_trans < texture.size[1] and x_trans > 0 and x_trans < texture.size[0] :
            color = texture.getpixel((x_trans, y_trans))
            entry.putpixel((x,y), color)

entry.save(result_name)

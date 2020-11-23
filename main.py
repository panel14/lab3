# Алгоритм работы программы: сначала создаётся шапка файла: поля BITMAPFILEHEADER и BITMAPINFOHEADER.
# Далее функцией create_pointlist вычисляется список точек функции на координатной плоскости (graph_pointlist)
# Потом мы проходимся циклом по всем пикселям файла - если координата пикселя яляется точкой графика из списка
# graph_pointlist - красим ее в черный цвет (число 0 - 00 00 00 00 в hex формате), иначе - в белый
# (число 16777215 - ff ff ff 00 в hex формате)
import struct
import math

FILE_WIDTH = 100
FILE_HEIGHT = 100
FILE_SIZE = 0
FILE_OFFSET = 14 + 40
COLOR_DEEP = 4
COLOR_COUNT = 32
COMPRESS = 0
PX_PER_M = 0
PARAMETER_RANGE = 629
WHITE_COLOR_HEX = 16777215
GRAPH_UP_LIM = 50
GRAPH_LOW_LIM = -50


def create_hat_block():
    return struct.pack('<2ci2hi', b'B', b'M', FILE_SIZE * COLOR_DEEP, 0, 0, FILE_OFFSET)


def create_info_block():
    return struct.pack('<3i2h6i', 40, FILE_WIDTH, FILE_HEIGHT, 1, COLOR_COUNT, COMPRESS, FILE_SIZE * COLOR_DEEP,
                       PX_PER_M, PX_PER_M, 0, 0)


def create_pointlist():
    pointlist = []
    for t in range(0, PARAMETER_RANGE):
        x = round(20 * (math.cos(t / 100) + math.cos(5 * t / 100) / 5))
        y = round(20 * (math.sin(t / 100) - math.sin(5 * t / 100) / 5))
        if [x, y] not in pointlist:
            pointlist.append([x, y])
    return pointlist


with open("picture.bmp", "wb") as f:
    f.write(create_hat_block())
    f.write(create_info_block())
    graph_pointlist = create_pointlist()
    for y in range(GRAPH_LOW_LIM, GRAPH_UP_LIM):
        for x in range(GRAPH_LOW_LIM, GRAPH_UP_LIM):
            cur_coords = [x, y]
            if cur_coords in graph_pointlist:
                f.write(struct.pack('<i', 0))
            else:
                f.write(struct.pack('<i', WHITE_COLOR_HEX))

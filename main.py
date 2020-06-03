import config
import reg
import reg_itk
import exe


import os

from PIL import Image


# bmp 转换为 jpg
def bmpToJpg(file_path):
    for fileName in os.listdir(file_path):
        # print(fileName)
        newFileName = fileName[0:fileName.find(".")]+".jpg"
        print(newFileName)
        im = Image.open(file_path+"\\"+fileName)
        im.save(file_path+"\\"+newFileName)


# 删除原来的位图
def deleteImages(file_path, imageFormat):
    command = "del "+file_path+"\\*."+imageFormat
    os.system(command)


# def main():
#     file_path = config.OR_SEG_DIR
#     bmpToJpg(file_path)
#     deleteImages(file_path, "bmp")


def main(name):
    fixed_OR = config.OR_ANN_DIR + name + ".jpg"
    moving_OR_CT = config.OR_CT_DIR + name + ".jpg"
    moving_OR_MR = config.OR_MR_DIR + name + ".jpg"

    output_test = config.OUTPUT_DIR + name
    reg_itk.registration(fixed_OR, moving_OR_CT, output_test + "_ct_")
    reg_itk.registration(fixed_OR, moving_OR_MR, output_test + "_mr_")
    # tfm = config.TFM_DIR + name + ".tfm"
    # times = 50000
    # output = config.OUTPUT_DIR + name + "_" + str(times) + ".jpg"
    # reg.registration(fixed_OR, moving_OR, tfm, times, True)
    # exe.exe(fixed_OR, moving_OR, tfm, output)


if __name__ == '__main__':
    for i in range(0, 8506, 5):
        main("%04d" % i)

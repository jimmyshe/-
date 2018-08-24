from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
import json

# RESOLUTION = 600
# SINGLE_CARD_W_RATIO = 2089/11583
# SINGLE_CARD_H_RATIO = 1344/8024
# H_SPACER_RATIO = 35/8024
# W_SPACER_RATIO = 0
# START_L_RATIO =  338/11583
# START_T_RATIO =  624/8024
# PICTURE_ON_CARD_L = 65.0/1010.0
# PICTURE_ON_CARD_T = 58.0/638.0
# PICTURE_ON_CARD_W = 376.0/1010.0
# PICTURE_ON_CARD_H = 250.0/638.0
with open('setting.json', 'r') as f:
    data = json.load(f)
    RESOLUTION = int(data["DPI"])
    SINGLE_CARD_W_RATIO =  data['SINGLE_CARD_W_RATIO']
    SINGLE_CARD_H_RATIO = data['SINGLE_CARD_H_RATIO']
    H_SPACER_RATIO = data['H_SPACER_RATIO']
    W_SPACER_RATIO = data['W_SPACER_RATIO']
    START_L_RATIO = data['START_L_RATIO']
    START_T_RATIO = data['START_T_RATIO']
    PICTURE_ON_CARD_H = data['PICTURE_ON_CARD_H']
    PICTURE_ON_CARD_W = data['PICTURE_ON_CARD_W']
    PICTURE_ON_CARD_T = data['PICTURE_ON_CARD_T']
    PICTURE_ON_CARD_L = data['PICTURE_ON_CARD_L']


def convert_fg(filePath):
    with Image(filename=filePath,resolution=RESOLUTION) as img:
        img.format = 'png'
        img_picture = img.clone()
        w,h = img.size
        img_picture.crop(int(PICTURE_ON_CARD_L*w), int(PICTURE_ON_CARD_T*h), width=int(PICTURE_ON_CARD_W*w), height=int(PICTURE_ON_CARD_H*h))
        with Color('#FFFFFF') as white:
            img.transparent_color(white, alpha=0.0, fuzz=0)
        with Drawing() as draw:
            draw.composite(operator='replace', left=int(PICTURE_ON_CARD_L*w), top=int(PICTURE_ON_CARD_T*h),
                           width=img_picture.width, height=img_picture.height, image=img_picture)
            draw(img)
        return img.clone()

def convert(filePath):
    with Image(filename=filePath,resolution=RESOLUTION) as img:
        return img.clone()

def convert_pdf_add_white_background(filePath):
    with Image(filename=filePath,resolution=RESOLUTION) as img:
        with Image(width=img.width, height=img.height, background=Color("white")) as bg:
            bg.composite(img, 0, 0)
            return bg.clone()


def composite_fg_bg(bg, fg, position_left, position_top):
    if position_left > 4 or position_top > 4 or  position_left < 0 or position_top < 0:
        return
    w,h = bg.size
    position_left_pixel = int(START_L_RATIO*w + SINGLE_CARD_W_RATIO*w*position_left +W_SPACER_RATIO*w*position_left)
    position_top_pixel = int(START_T_RATIO*h + SINGLE_CARD_H_RATIO*h*position_top + H_SPACER_RATIO*h*position_top)
    with Drawing() as draw:
        draw.composite(operator='atop', left=position_left_pixel, top=position_top_pixel,
                       width=fg.width, height=fg.height, image=fg)
        draw(bg)
        return bg.clone()

if __name__ == '__main__':
    print("test")
    # bg =convert_pdf_add_white_background("bg.pdf")
    # bg.save(filename="bg.png")

    # img = convert_fg("1.pdf")
    # img.save(filename="temp.png")
    #
    # with Image(filename="bg.png", resolution=RESOLUTION) as bg:
    #     # w,h = bg.size
    #     # with Drawing() as draw:
    #     #     draw.composite(operator='atop', left=58/5297*w, top=75/3526*h,
    #     #                    width=img.width, height=img.height, image=img)
    #     #     draw(bg)
    #     # bg.save(filename="output.png")
    #     for x in range(5):
    #         for y in range(5):
    #             bg = composite_fg_bg(bg, img, x, y)
    #     bg.save(filename="output.png")


    # data = {'DPI': 600,
    #         'SINGLE_CARD_W_RATIO': 1,
    #         'SINGLE_CARD_H_RATIO': 1,
    #         'H_SPACER_RATIO' :1,
    #         'W_SPACER_RATIO' : 1,
    #         'START_L_RATIO' :1,
    #         'START_T_RATIO' : 1,
    #         'PICTURE_ON_CARD_L' : 1,
    #         'PICTURE_ON_CARD_T' : 1,
    #         'PICTURE_ON_CARD_W' : 1,
    #         'PICTURE_ON_CARD_H' : 1}
    #
    # data['DPI'] = RESOLUTION
    # data['SINGLE_CARD_W_RATIO'] = SINGLE_CARD_W_RATIO
    # data['SINGLE_CARD_H_RATIO'] = SINGLE_CARD_H_RATIO
    # data['H_SPACER_RATIO'] =H_SPACER_RATIO
    # data['W_SPACER_RATIO']=W_SPACER_RATIO
    # data['START_L_RATIO'] = START_L_RATIO
    # data['START_T_RATIO']= START_T_RATIO
    # data['PICTURE_ON_CARD_H'] = PICTURE_ON_CARD_H
    # data['PICTURE_ON_CARD_W'] = PICTURE_ON_CARD_W
    # data['PICTURE_ON_CARD_T'] = PICTURE_ON_CARD_T
    # data['PICTURE_ON_CARD_L'] = PICTURE_ON_CARD_L
    # with open('setting.json', 'w') as f:
    #     json.dump(data, f)
    #
    #

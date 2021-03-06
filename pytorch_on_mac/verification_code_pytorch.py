# 验证码识别

# coding=utf-8
import time
import random
import string
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import random

all_letters = string.digits + string.ascii_lowercase
letters_dict = {k: v for v, k in enumerate(all_letters)}

# 字体的位置，不同版本的系统会有不同
font_path = 'fonts/Roboto-Black.ttf'
# 生成几位数的验证码
number = 4
# 生成验证码图片的高度和宽度
size = (100, 30)
# 背景颜色，默认为白色
bgcolor = (0, 0, 0)
# 字体颜色，默认为蓝色
fontcolor = (0, 0, 255)
# 干扰线颜色。默认为红色
linecolor = (0, 0, 255)
# 是否要加入干扰线
draw_line = False
# 加入干扰线条数的上下限
line_number = (1, 5)


# 用来随机生成一个字符串
def gene_text():
    source = list(string.ascii_letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


# 用来绘制干扰线
def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


# 生成验证码
def gene_code():
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片
    font = ImageFont.truetype(font_path, 25)  # 验证码的字体
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = gene_text()  # 生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,
              font=font, fill=fontcolor)  # 填充字符串
    if draw_line:
        gene_line(draw, width, height)
    # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    image = image.transform((width, height), Image.AFFINE,
                            (random.uniform(0.8, 1.2), random.uniform(-0.5, 0.5), 0, random.uniform(-0.1, 0.1), 1, 0),
                            Image.BILINEAR)  # 创建扭曲(参数1：左右留白大小，2：左右扭曲度, 3:do't konw, 4:左右旋转度，5：
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    # image.save('idencode.png')  # 保存验证码图片
    s2 = ''
    # for循环是为了将大写字母变为小写
    for s in text:
        if 64 < ord(s) < 97:
            n = ord(s) + 32
            s = chr(n)
        s2 += s
    s_list = [-1]*36
    for n, a in enumerate(s2):
        s_list[n] = letters_dict[a]
    yield image, s_list


if __name__ == "__main__":
    t1 = time.time()
    plt.figure(figsize=(8,12))
    for i in range(1, 11):
        img, text = next(gene_code())
        plt.subplot(10, 1, i)
        plt.title(text[0:4])
        plt.imshow(img)
        plt.axis('off')
        plt.tight_layout()
    print(time.time()-t1)
    plt.show()

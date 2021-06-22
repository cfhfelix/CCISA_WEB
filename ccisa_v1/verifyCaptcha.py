import random
import string
# Image:一個畫布
# ImageDraw:一個畫筆
# ImageFont:畫筆的字體

# pip install pillow
from PIL import Image, ImageDraw, ImageFont


class Captcha(object):
    # 生成幾位數的驗證碼
    number = 4
    # 驗證碼圖片的高度和寬度
    size = (100, 30)
    # 驗證碼字體大小
    fontsize = 25
    #加入幹擾線條數
    line_number = 2

    #構建一個驗證碼源文本
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    #用來繪制幹擾線
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    # 用來繪制幹擾點
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance))) #大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    # 生成隨機的顏色
    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        random.seed()
        return (random.randint(start, end),random.randint(start, end), random.randint(start, end))

    # 隨機選擇一個字體
    @classmethod
    def __gene_random_font(cls):

        font = 'verdana.ttf'
        return 'static/font/' + font

    # 用來隨機生成一個字符串
    @classmethod
    def gene_text(cls, number):
        #num是生成驗證碼的位數
        return ''.join(random.sample(cls.SOURCE, number))

    # 生成驗證碼
    @classmethod
    def gene_graph_captcha(cls):
        #驗證碼圖片的高和寬
        width, height = cls.size
        #創建圖片
        image = Image.new('RGB', (width,height),cls.__gene_random_color(0, 100))
        #驗證碼的字體
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        #創建畫筆
        draw = ImageDraw.Draw(image)
        #生成字符串
        text = cls.gene_text(cls.number)
        #獲取字體尺寸
        font_width, font_height = font.getsize(text)
        #填充字符串
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font,
                  fill=cls.__gene_random_color(150, 255))
        #繪制幹擾線
        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
        #繪制噪點
        cls.__gene_points(draw, 10, width, height)
    
        return (text, image)
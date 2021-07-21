from datetime import datetime
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

from config import PHOTO_NAME
import urllib
import requests

class PhotoChanger:
    def __init__(self, width: int, height: int, font_size: int,
                 font_path: str, font_color: Tuple[int, int, int],
                 color: Tuple[int, int, int]):
        self.width = width
        self.font_size = font_size
        self.font_path = font_path
        self.font_color = font_color
        self.height = height
        self.color = color

    def image(self, delimiter: str) -> Image:
        image_time = Image.new('RGB', (self.width, self.height), self.color)
        font_progress = ImageFont.truetype(self.font_path, self.font_size)
        font_time = ImageFont.truetype(self.font_path, int(self.font_size*4.2))
        progress, time, percent = self.time(delimiter)
        draw = ImageDraw.Draw(image_time)
        progress_width, progress_height = draw.textsize(progress, font_progress)
        time_width, time_height = draw.textsize(time, font_time)
        self.draw_text(draw, time, progress_height,
                       time_width, time_height, font_time)
        self.draw_rectangle(draw, percent, font_progress)
        return image_time

    def draw_text(self, draw: ImageDraw, time: str,
                  progress_height: int, time_width: int,
                  time_height: int, font_time: ImageFont):
        draw.text(
            ((self.width-time_width)/2,
             (self.height-time_height-progress_height)/2),
            time, self.font_color, font=font_time, align='center'
        )

    def draw_rectangle(self, draw: ImageDraw, percent: float, font: ImageFont):
        left_x = self.width/6
        left_y = self.height*15/24
        right_x = self.width*4/6
        right_y = left_y+self.height*0.08
        draw.rectangle(((left_x, left_y), (right_x, right_y)),
                       outline=(255, 0, 0), width=5)
        draw.rectangle(((left_x, left_y), (right_x*percent/100, right_y)),
                       fill=(255, 0, 0))
        draw.text((right_x+self.width*0.03, left_y+self.height*0.02), f'{percent:2.2f}%',
                  (255, 0, 0), font=font)

    @staticmethod
    def time(delimiter: str):
        now = datetime.now()
        html_code = urllib.request.urlopen("http://www.unn.ru/time/").read()
        soup = BeautifulSoup(html_code, 'html.parser')
        hour = int(soup.get_text()[69] + soup.get_text()[70])
        minute = int(soup.get_text()[72] + soup.get_text()[73])
        second = int(soup.get_text()[75] + soup.get_text()[76])
        print(hour, minute, second)
        percent = (hour * 3600 + minute * 60 + second) / 864
        text = f'PROGRESS DAY'
        time = f'{hour}{delimiter}{minute}'
        return text, time, percent

    def save_profile_photo(self):
        image = self.image(':')
        image.save(PHOTO_NAME)


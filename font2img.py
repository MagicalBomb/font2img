#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: demo
@time: 2021/1/14
@email: 2
@desc: 
"""

from io import BytesIO
from math import ceil

from PIL import Image
from fontTools.pens.reportLabPen import ReportLabPen
from fontTools.ttLib import TTFont
from reportlab.graphics.shapes import Path
from reportlab.lib import colors
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing

# 图片相关参数
FONT_WIDTH = 180 # 单个字体转成图片的宽度
FONT_HEIGHT = 180 # 长度
BASE_BACKGOUND_WIDTH = FONT_WIDTH + 10
BASE_BACKGOUND_HEIGHT = FONT_HEIGHT + 10
WIDTH_PER_LINE = (BASE_BACKGOUND_WIDTH + FONT_WIDTH) // 2
HEIGHT_PER_LINE = (FONT_HEIGHT + BASE_BACKGOUND_HEIGHT) // 2
FONT_NUMS_PER_LINE = 14

__all__ = ["ParseTTFFont"]


class ParseTTFFont:


    def __init__(self, font, ignore_names=[], overwrite_ignore=False):
        self.font_file_name = font
        if isinstance(font, str):
            self.font = TTFont(font)
        elif isinstance(font, bytes):
            self.font = TTFont(BytesIO(font))
        else:
            raise ValueError('argument font must be str or bytes to indicate where the font file can be found')
        self.glyphnames = self.font.getGlyphOrder()
        self.ignore_names = ignore_names if overwrite_ignore else ignore_names + []

    def get_glyphnames(self):
        return self.glyphnames

    def one_to_image(self, glyph_name):
        glyphset = self.font.getGlyphSet()
        try:
            glyph = glyphset[glyph_name]
        except KeyError as e:
            raise KeyError("{} dont't in {}".format(glyph_name, self.font_file_name))
        
        pen = ReportLabPen(self.glyphnames, Path(fillColor=colors.black, strokeWidth=1))
        glyph.draw(pen)
        w, h = glyph.width if glyph.width > 1000 else 1000, glyph.width if glyph.width > 1000 else 1000
        d = Drawing(w, h)
        d.add(pen.path)
        im = renderPM.drawToPIL(d, dpi=72).resize((FONT_WIDTH, FONT_HEIGHT))
        return im



    def all_to_image(self):
        """
        将字体文件的字体整个绘制在Image对象上
        返回一个三元组,包括: 字体文件绘制完成的图片, 绘制出各字形的名称, 各字形单独的图片
        """
        glyphset = self.font.getGlyphSet()
        size = (BASE_BACKGOUND_WIDTH * FONT_NUMS_PER_LINE,
                ceil(len(self.glyphnames) / FONT_NUMS_PER_LINE) * BASE_BACKGOUND_HEIGHT)  # 背景图片尺寸
        image = Image.new("RGB", size=size, color=(255, 255, 255))  # 初始化背景图片
        name_list, image_dict = [], {}
        
        for index, glyphname in enumerate(self.glyphnames):
            if glyphname[0] in ['.', 'g'] or glyphname in self.ignore_names:  # 跳过'.notdef', '.null'
                continue
            g = glyphset[glyphname]
            pen = ReportLabPen(self.glyphnames, Path(fillColor=colors.black, strokeWidth=1))
            g.draw(pen)
            # w, h = g.width, g.width
            w, h = g.width if g.width > 1000 else 1000, g.width if g.width > 1000 else 1000
            g = Group(pen.path)
            g.translate(0, 200)
            d = Drawing(w, h)
            d.add(g)
            im = renderPM.drawToPIL(d, dpi=72).resize((FONT_WIDTH, FONT_HEIGHT))
            box = (
                (index % FONT_NUMS_PER_LINE) * BASE_BACKGOUND_WIDTH,
                (index // FONT_NUMS_PER_LINE) * BASE_BACKGOUND_HEIGHT)
            image.paste(im, box=box)
            name_list.append(glyphname)
            image_dict[glyphname] = im
        return image, name_list, image_dict

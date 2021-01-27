# 安装

```Python
pip install font2img
```

# 使用

```Python
from font2img import ParseTTFFont

p = ParseTTFont("font_file.woff") # 载入当前目录下的 font_file.woff 字体文件
glyphnames = p.get_glyphnames() # 获取字体文件中所有有效字形的代号

# im 类型为 PIL.Image
im = p.one_to_image(glphnames[10]) # 获取第 11 个字形的图像
im.show()

# 将所有字形整合成一张图像, 所有图像类型为 PIL.Image
# image: 包含所有字形的图形
# name_list: 包含所有字形的代号
# image_dict: 各字形图像同其代号的字典
image, name_list, image_dict = p.all_to_image() 
```

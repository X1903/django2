# _*_ coding:utf-8 _*_
__author__ = 'Xbc'

import matplotlib as mpl
mpl.use('TkAgg')


from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud




f = open('./jd_comment.txt','rb')
text = f.read()

cut_text = ''.join(jieba.lcut(text))
print(cut_text)
color_mask = imread("iphone.jpg")
cloud = WordCloud(
    font_path='ziti.TTF',  # 字体最好放在与脚本相同的目录下，而且必须设置
    background_color='white',
    mask=color_mask,
    max_words=500,
    max_font_size=3000
)
word_cloud = cloud.generate(cut_text)
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
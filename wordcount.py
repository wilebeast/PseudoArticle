import os
import re  # 正则表达式库
import collections  # 词频统计库
import numpy as np  # numpy数据处理库
import jieba  # 结巴分词
import wordcloud  # 词云展示库
from PIL import Image  # 图像处理库
import matplotlib.pyplot as plt  # 图像展示库

dir_list = []


def scan():
    # dir_list = os.listdir('./old_txt')
    for filepath, dirs, fs in os.walk('/Users/bytedance/go/src/code.byted.org/ad/engine'):
        for f in fs:
            # print(f)
            if os.path.splitext(f)[1] == '.go':
                dir_list.append(os.path.join(filepath, f))
    return dir_list


# 读取文件
scan()
print(dir_list)
string_data = ""
for path in dir_list:
    fn = open(path)  # 打开文件
    string_data += fn.read()  # 读出整个文件
    fn.close()  # 关闭文件

# 文本预处理
print(string_data)
pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

# 文本分词
seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
object_list = []
remove_words = [u',', u'，', u'_', u'=', u'}', u'{', u'/', u'[', u']', u'*', u'。', u' ', u'、', u'if', u'else', u'(',
                u')', u'func', u'struct', u'enum', u' ', u'return', u'&', u'nil', u'Value', u'true', u'err', u'int64',
                u'0', u'1', u'ad', u'map', u'&&', '>', 'string', 'v', 'id', 'float64', '%', 'range', 'var', 'common',
                'Name', 'cids', 'ok', 'aweme', '!', 'error', 'bool', 'mode', 'optional', 'type']  # 自定义去除词库

for word in seg_list_exact:  # 循环读出每个分词
    if word not in remove_words:  # 如果不在去除词库中
        object_list.append(word)  # 分词追加到列表

# 词频统计
word_counts = collections.Counter(object_list)  # 对分词做词频统计
word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
print(word_counts_top10)  # 输出检查

# 词频展示
# mask = np.array(Image.open('wordcloud.jpg'))  # 定义词频背景
wc = wordcloud.WordCloud(
    # font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
    # mask=mask,  # 设置背景图
    max_words=200,  # 最多显示词数
    max_font_size=100  # 字体最大值
)

wc.generate_from_frequencies(word_counts)  # 从字典生成词云
# image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
# wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
plt.imshow(wc)  # 显示词云
plt.axis('off')  # 关闭坐标轴
plt.show()  # 显示图像

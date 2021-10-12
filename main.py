# coding=utf-8
import os, re
import synonyms
from jieba import posseg as pseg


def Scan():
    dir_list = os.listdir('./old_txt')
    return dir_list


def Read(path):
    with open('./old_txt/' + path, 'r', encoding='utf-8') as f:
        content = f.read()
    title_list = re.findall('<title=(.*?)>', content)
    title = title_list[0] if len(title_list) != 0 else None
    article_list = re.findall('<neirong=([\s\S]*)>', (content.replace('\n', '')).replace('<p>', ''))
    article = article_list[0] if len(article_list) != 0 else None
    words_list = []
    string_list = article.split('</p>')
    for string in string_list:
        if string != '':
            words_list.append(string)
    if title is not None and len(words_list) > 0:
        return title, words_list
    else:
        return None, None


def write(path,content):
    with open('./new_txt/' + path, 'a+', encoding='utf-8') as f:
        f.write(content)


def words_change(words):  # 传入句子，变形返回
    words_tuple = pseg.lcut(words)
    print(words_tuple)
    word_list = []
    for word, flag in words_tuple:
        if flag == 'a' or flag == 'ad' or flag == 'v':  # 词性判断
            seg_list = (synonyms.nearby(word))[0]
            if len(seg_list) <= 1:
                word = word
            else:
                word = seg_list[1]
        word_list.append(word)
    return "".join(word_list)


def run():
    dir_list = Scan()
    for path in dir_list:
        title, words_list = Read(path)
        if title is not None and words_list is not None:
            title = words_change(title)
            write(path,'<title={}>'.format(title) + '\n')
            write(path,'<neirong=')
            for words in words_list:
                word = words_change(words)
                write(path,'\n<p>' + word + '</p>' + '')
            write(path,'>')


if __name__ == '__main__':
    run()

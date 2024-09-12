import unittest

import jieba
import gensim
import re

jieba.setLogLevel(jieba.logging.INFO)

# 获取指定的原文
def get_file(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str

#将读取到的文件内容先进行jieba分词，然后再把标点符号、转义符号等特殊符号过滤掉
def filter(str):
    str = jieba.lcut(str)
    result = []
    for tags in str:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags)):
            result.append(tags)
        else:
            pass
    return result


#传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
def calc_similarity(text1, text2) -> object:
    texts=[text1,text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim

def main_test():
    path1 = input("请输入文件1的绝对路径：")
    path2 = input("请输入文件2的绝对路径：")
    str1 = get_file(path1)
    str2 = get_file(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)
    result=round(similarity.item(),2)
    return result

if __name__ == '__main__':
    main_test()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main_test(),0.99)


if __name__ == '__main__':
    unittest.main()


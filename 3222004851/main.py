import jieba
import gensim
import re
import os


jieba.setLogLevel(jieba.logging.INFO)


# 获取指定的原文
def get_file(path):
    # global str2
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str


# 将获取到的文本先进行预处理：将文本分词，再将标点符号、换行等等特殊符号过滤
def filter(str1):
    str1 = jieba.lcut(str1)
    result = []
    for tags in str1:
        if re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags):
            result.append(tags)
    else:
        pass
    return result


# 将文本的语法等等去除，把文本只看成一个个词汇的集合
def convert_corpus(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus


# 将经过预处理的数据，利用gensim.similarities.Similarity计算余弦相似度
def file_similarity(text1, text2) -> object:
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim


if __name__ == '__main__':
    path1 = input("请输入论文原文的文件的绝对路径：")
    path2 = input("请输入抄袭版论文的文件的绝对路径：")
    if not os.path.exists(path1):
        print("论文原文文件不存在")
        exit()
    if not os.path.exists(path2):
        print("抄袭版论文文件不存在")
        exit()
    save_path = "D:/学习资料/软工作业/AAA-Lin/3222004851/ans.txt"  # 输出结果绝对路径
    str1 = get_file(path1)
    str2 = get_file(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = file_similarity(text1, text2)
    print("文章相似度： %.4f" % similarity)
    # 将结果输出写入指定文件
    f = open(save_path, 'w', encoding="utf-8")
    f.write( "文章相似度： %.4f" % similarity)
    f.close()


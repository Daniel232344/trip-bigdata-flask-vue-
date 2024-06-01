import jieba
import jieba.posseg as pseg

from utils.dbutils import *
from question_answer.获取天气情况 import *
import re
from utils.user_base import *

jieba.enable_paddle()


def get_loc_list(text):
    per_list = []  # 列表
    word_list = jieba.lcut(text)
    print(word_list)
    """
    for word in word_list:
        if len(word) == 1:  # 不加判断会爆
            continue
        words = pseg.cut(word, use_paddle=True)  # paddle模式
        print('list(words)')
        print(list(words))
        for word1, flag in list(words):  # 直接遍历生成器中的元素
            print('word1')
            print(word1)
            per_list.append(word1)
    per_list = list(set(per_list))
    print(per_list)
    return per_list
    """
    return word_list


def question_classifier(text,uid='1'):
    # 如果flag一直为0的话就表示看不懂
    ans = '呜呜呜，我没看懂，换个问题试试'

    # 地区有什么景点
    if len(re.findall('.*?-景点',text))>0:
        print('地区有什么景点')
        all_data = []
        nodes = []
        links = []
        ner = text.split("-")[0]
        sql = 'select * from scenery where location="%s" limit 10'%ner
        all_data = select_data(sql)
        ans = '、'.join([i['title'] for i in all_data])

        # 添加景点node
        index = 0
        for i in all_data:
            nodes.append({'id':index,'category':0,'name':i['title'],'symbol' : 'circle','symbolSize' : 40})
            index+=1
        # 添加地区node
        nodes.append({'id': index, 'category': 1, 'name': ner, 'symbol': 'circle', 'symbolSize': 40})
        index += 1

        # 添加关系
        for i in nodes:
            if i['category']==0:
                links.append({'source': i['id'], 'target': index-1, 'value': '位于', 'name': '位于'})

        return ans,nodes,links

    # 景点在哪个地区
    if len(re.findall('.*?-位置',text))>0:
        print('景点在哪个地区')
        all_data = []
        nodes = []
        links = []
        ner = text.split("-")[0]
        sql = 'select location from scenery where title="%s"'%ner
        print('对应的sql语句')
        print(sql)
        all_data = select_data(sql)[0]
        ans = all_data['location']
        # 两个node
        nodes.append({'id': 1, 'category': 0, 'name': ner, 'symbol': 'circle', 'symbolSize': 40})
        nodes.append({'id': 2, 'category': 1, 'name': ans, 'symbol': 'circle', 'symbolSize': 40})
        links.append({'source': 1, 'target': 2, 'value': '位于', 'name': '位于'})
        print(ans, nodes, links)
        return ans, nodes, links
        # print('景点在哪个地区')

    # 附近景点
    if len(re.findall('.*?-附近景点',text))>0:
        print('附近景点')
        all_data = []
        nodes = []
        links = []
        ner = text.split("-")[0]
        sql = 'select * from relationship where A="%s" and relationship="%s" limit 10'%(ner,'附近')
        all_data = select_data(sql)
        ans = '、'.join([i['B'] for i in all_data])

        index = 0
        for i in all_data:
            nodes.append({'id': index, 'category': 0, 'name': i['B'], 'symbol': 'circle', 'symbolSize': 40})
            index+=1
        nodes.append({'id': index, 'category': 0, 'name': all_data[0]['A'], 'symbol': 'circle', 'symbolSize': 40})
        index+=1
        # 联系
        for i in nodes:
            if i['name']!= all_data[0]['A']:
                links.append({'source': i['id'], 'target': index-1, 'value': '附近', 'name': '附近'})
        return ans,nodes,links
        # print('附近景点')

    # 相似景点
    if len(re.findall('.*?-类似景点',text))>0:
        print('类似景点')
        all_data = []
        nodes = []
        links = []
        ner = text.split("-")[0]
        sql = 'select * from relationship where A="%s" and relationship="%s" limit 10'%(ner,'相似')
        all_data = select_data(sql)
        ans = '、'.join([i['B'] for i in all_data])

        index = 0
        for i in all_data:
            nodes.append({'id': index, 'category': 0, 'name': i['B'], 'symbol': 'circle', 'symbolSize': 40})
            index+=1
        nodes.append({'id': index, 'category': 0, 'name': all_data[0]['A'], 'symbol': 'circle', 'symbolSize': 40})
        index+=1
        # 联系
        for i in nodes:
            if i['name']!= all_data[0]['A']:
                links.append({'source': i['id'], 'target': index-1, 'value': '相似', 'name': '相似'})

        return ans,nodes,links

        # print('相似景点')

    # # 景点相关的vlog
    # if len(re.findall('.*?相关的视频.*?|.*?黄鹤楼相关的vlog.*?',text))>0:
    #     ans = '景点相关的vlog'
    #     # print('景点相关的vlog')

    # 景点相关的游记
    if len(re.findall('.*?-游记',text))>0:
        print('景点相关的游记')
        all_data = []
        nodes = []
        links = []
        ner = text.split("-")[0]
        sql = 'select * from relationship where A="%s" and relationship="%s" limit 5' % (ner, '相关游记')
        # print(sql)
        all_data = select_data(sql)
        # print(data)
        ans = '、\n'.join([i['B'] for i in all_data])

        index = 0
        for i in all_data:
            nodes.append({'id': index, 'category': 2, 'name': i['B'], 'symbol': 'circle', 'symbolSize': 40})
            index+=1
        nodes.append({'id': index, 'category': 0, 'name': all_data[0]['A'], 'symbol': 'circle', 'symbolSize': 40})
        index+=1
        # 联系
        for i in nodes:
            if i['name']!= all_data[0]['A']:
                links.append({'source': i['id'], 'target': index-1, 'value': '相关游记', 'name': '相关游记'})
        return ans,nodes,links

    # 推荐景点
    if len(re.findall('推荐景点',text))>0:
        print('推荐景点')
        all_data = []
        nodes = []
        links = []
        user_cf = User_CF('scenery_action')
        id_list = user_cf.get_one_recommend(uid)
        for i in id_list:
            sql = 'select * from scenery where `index`=%s'%i
            one_data = select_data(sql)[0]
            all_data.append(one_data)
        ans = '、'.join([i['title'] for i in all_data])

        index = 0
        for i in all_data:
            nodes.append({'id': index, 'category': 0, 'name': i['title'], 'symbol': 'circle', 'symbolSize': 40})
            index+=1
        return ans,nodes,links


    # 推荐游记
    if len(re.findall('推荐游记',text))>0:
        print('推荐游记')
        all_data = []
        nodes = []
        links = []
        user_cf = User_CF('artical_action')
        id_list = user_cf.get_one_recommend(uid)[:3]
        for i in id_list:
            sql = 'select * from artical where `index`=%s'%i
            one_data = select_data(sql)[0]
            all_data.append(one_data)
        ans = '、\n'.join([i['title'] for i in all_data])

        index = 0
        for i in all_data:
            nodes.append({'id': index, 'category': 2, 'name': i['title'], 'symbol': 'circle', 'symbolSize': 40})
            index+=1
        return ans,nodes,links

    # # 推荐vlog
    # if len(re.findall('.*?推荐一些视频|推荐视频|.*?推荐一些vlog|推荐vlog',text))>0:
    #     ans = '推荐vlog'
    #     # print('推荐vlog')
    return ans,[],[]


if __name__ == '__main__':
    while 1:
        text = input('问:')
        ans = question_classifier(text)
        print('分类结果:', ans)
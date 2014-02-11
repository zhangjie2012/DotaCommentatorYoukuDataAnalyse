#! /usr/bin/python
# -*- coding: UTF-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from GlobalParam import *

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Microsoft YaHei']})

from pylab import *
rcParams['figure.figsize'] = 12, 8

colors = [ '#bd2309', '#bbb12d', '#1480fa', '#14fa2f', '#000000', '#faf214', '#2edfea', '#ea2ec4', '#ea2e40', '#cdcdcd',
    '#577a4d', '#2e46c0', '#f59422', '#219774', '#8086d9', '#2e24ea']

def translate_to_chinese(name):
    if name == "2009":
        return u"酒神"
    elif name == "HaiTao":
        return u"海涛"
    elif name == "ManLouShuiPing":
        return u"满楼"
    elif name == "XiaoMan":
        return u"小满"
    elif name == "NiuWa":
        return u"蛙导"
    elif name == "LaoShu_SJQ":
        return u"老鼠"
    elif name == "KuangShi":
        return u"狂湿"
    elif name == "Ks_ChenBin":
        return u"Kssss"
    elif name == "TuFu_AChuan":
        return u"阿川"
    elif name == "Pc_LengLeng":
        return u"冷冷"
    elif name == "Pis":
        return u"P神"
    elif name == "MeiXi_Huang":
        return u"梅西"
    elif name == "Kevin":
        return u"凯文"
    elif name == "XiaoGuai":
        return u"乖神"
    elif name == "QingShu":
        return u"情书"
    else:
        return name
        
def draw_all_com_followers_topology(rel_graph):
    rel_graph.to_chinese()
    
    G = nx.Graph()
    
    # add edge
    e_very_strong = []
    e_strong = []
    e_normal = []
    
    for rel in rel_graph.very_strong:
        G.add_edge(rel.first_name, rel.second_name, weight=rel.weight)
        e_very_strong.append((rel.first_name, rel.second_name))
        
    for rel in rel_graph.strong:
        G.add_edge(rel.first_name, rel.second_name, weight=rel.weight)
        e_strong.append((rel.first_name, rel.second_name))
        
    for rel in rel_graph.normal:
        G.add_edge(rel.first_name, rel.second_name, weight=rel.weight)
        e_normal.append((rel.first_name, rel.second_name))
        
    # positions for all nodes
    pos = nx.spring_layout(G)
    
    nx.draw_networkx_nodes(G, pos, alpha=0.5, node_color="#000000", node_size=2500)
    nx.draw_networkx_edges(G, pos, edgelist=e_very_strong, edge_color='#EE30A7', width=3)
    nx.draw_networkx_edges(G, pos, edgelist=e_strong, edge_color='#1E90FF', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=e_normal, edge_color='#C1CDC1', width=1)
    
    nx.draw_networkx_labels(G, pos, font_size=14, font_color='#ADFF2F', font_family='Microsoft YaHei')
    
    plt.title(u"优酷Dota众解说粉丝重合率结构图")
    plt.axis('off')
    plt.savefig("%s/YoukuDotaComFollowersTopology.png"%temp_img_store_dir, dpi=120)
    #plt.show() # display

def draw_one_com_compare_pie(com):
    sizes = []
    labels = []
    for rl in com.relevancy_list:
        sizes.append(rl.same_followers_count)
        labels.append(u"%s %1.1f%%" % (translate_to_chinese(commentator_id_to_name[rl.other_id]), rl.percent*100))
        
    plt.pie(sizes, colors=colors, startangle=45)
    plt.title(u"%s与其他解说粉丝重合占比"%translate_to_chinese(commentator_id_to_name[com.id]));
    plt.legend(labels)
    plt.axis('off')
    plt.savefig("%s/%s_WithOthersCompare.png"%(temp_img_store_dir, commentator_id_to_name[com.id]), dpi=120)
    #plt.show()
    plt.clf()
    
def draw_all_coms_compare_pie(commentators):
    for com in commentators:
        draw_one_com_compare_pie(com)
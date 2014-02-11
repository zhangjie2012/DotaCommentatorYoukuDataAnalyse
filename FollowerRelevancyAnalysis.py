#! /usr/bin/python
# -*- coding: UTF-8 -*-

from GlobalParam import *
from GetMinFollowersCount import *
from DrawImg import *

class RelevancyAtom:
    def __init__(self, id, count):
        self.other_id = id
        self.same_followers_count = count
        self.percent = 0.0
        
class Commentator:
    def __init__(self, id, name, analyse_followers_count):
        self.id = id
        
        # init followers id from file
        self.followers_id = set()
        file_path = self.__get_follower_data_file_path(id, name)
        self.__get_follower_from_file(file_path, analyse_followers_count)
        
        self.relevancy_list = []
        
    def insert_relevancy(self, id, count):
        self.relevancy_list.append(RelevancyAtom(id, count))
        
    def cal_other_id_followers_percent(self):
        total_same_followers = 0
        
        for rel_atom in self.relevancy_list:
            total_same_followers += rel_atom.same_followers_count
        for rel_atom in self.relevancy_list:
            rel_atom.percent = rel_atom.same_followers_count/float(total_same_followers)
    
    def sort_relevancy_by_percent(self):
        self.relevancy_list.sort(key=lambda rel_atom : rel_atom.percent, reverse = True)
        
    def get_index(self, id):
        index = 1
        for rl in self.relevancy_list:
            if rl.other_id == id:
                break
            index += 1
        return index
        
    def debug_output(self):
        print "\nName: %s TotalAnalyseFollowers: %d" % (commentator_id_to_name[self.id], len(self.followers_id))
        for rel_atom in self.relevancy_list:
            print "\t-> %15s %10s %10.2f%%" % (commentator_id_to_name[rel_atom.other_id], rel_atom.same_followers_count, rel_atom.percent*100)
        
    def __get_follower_from_file(self, file_path, analyse_followers_count):
        file_handle = open(file_path, "r")
        
        while True:
            if analyse_followers_count == 0:
                break
                
            line = file_handle.readline()
            if not line:
                break
            
            line = line.strip()
            if len(line) != 0:
                self.followers_id.add(line)
            
            analyse_followers_count -= 1
            
        file_handle.close()
        
    def __get_follower_data_file_path(self, id, name):
        return  "%s/%s_%s" % (temp_data_store_dir, name, id)

class RelevancyNode():
    def __init__(self, first_name, second_name, weight):
        self.first_name = first_name
        self.second_name = second_name
        self.weight = weight
        
class RelevancyGraph():
    def __init__(self):
        self.very_strong = []
        self.strong = []
        self.normal = []
        self.weak = []
        
    # first_loc: second_name in first_name's relevancy_list's index
    # second_loc: first_name in second_name's relevancy_list's index 
    # predicate relevancy:
    #   weight in 
    #       [2 ~ 4) -> very strong
    #       [4 ~ 7) -> strong
    #       [7 ~ 11) -> normal
    #       [11 ~ ) -> weak [do not show]
    def insert_node(self, first_name, second_name, first_loc, second_loc):
        weight = first_loc + second_loc
        
        if weight < 4:
            self.very_strong.append(RelevancyNode(first_name, second_name, weight))
        elif weight < 7:
            self.strong.append(RelevancyNode(first_name, second_name, weight))
        elif weight < 11:
            self.normal.append(RelevancyNode(first_name, second_name, weight))
        else:
            self.weak.append(RelevancyNode(first_name, second_name, weight))
    
    def to_chinese(self):
        for rel in self.very_strong:
            rel.first_name = translate_to_chinese(rel.first_name)
            rel.second_name = translate_to_chinese(rel.second_name)
        for rel in self.strong:
            rel.first_name = translate_to_chinese(rel.first_name)
            rel.second_name = translate_to_chinese(rel.second_name)
        for rel in self.normal:
            rel.first_name = translate_to_chinese(rel.first_name)
            rel.second_name = translate_to_chinese(rel.second_name)
        for rel in self.weak:
            rel.first_name = translate_to_chinese(rel.first_name)
            rel.second_name = translate_to_chinese(rel.second_name)
        
    def debug_output(self):
        print "very_strong:"
        for rel in self.very_strong:
            print "\t", rel.first_name, rel.second_name, rel.weight
            
        print "strong:"
        for rel in self.strong:
            print "\t", rel.first_name, rel.second_name, rel.weight
            
        print "normal:"
        for rel in self.normal:
            print "\t", rel.first_name, rel.second_name, rel.weight
        
        print "weak:"
        for rel in self.weak:
            print "\t", rel.first_name, rel.second_name, rel.weight
            
def cal_follower_relevancy(commentators):
    for i in range(0, len(commentators)):
        for j in range(0, len(commentators)):
            if i == j:
                continue
            commentators[i].insert_relevancy(commentators[j].id,
                                             len(commentators[i].followers_id.intersection(commentators[j].followers_id)))
        
        commentators[i].cal_other_id_followers_percent()
        commentators[i].sort_relevancy_by_percent()

def gen_commentators_from_file():
    analyse_followers_count = get_min_follower_count()
    
    commentators = []
    for (id, name)  in commentator_id_to_name.items():
        commentators.append(Commentator(id, name, analyse_followers_count))
    
    cal_follower_relevancy(commentators)
    
    return commentators
     
def init_rel_graph_data(commentators):    
    rel_graph = RelevancyGraph()
    
    for i in range(0, len(commentators)):
        for j in range(i+1, len(commentators)):
            rel_graph.insert_node(commentator_id_to_name[commentators[i].id], commentator_id_to_name[commentators[j].id],
                commentators[i].get_index(commentators[j].id), commentators[j].get_index(commentators[i].id))
    #rel_graph.debug_output()
    return rel_graph
    
    
def main():
    commentators = gen_commentators_from_file()
    draw_all_coms_compare_pie(commentators)
    
    # for com in commentators:
        # com.debug_output()
        
    rel_graph = init_rel_graph_data(commentators)
    draw_all_com_followers_topology(rel_graph)
    
if __name__ == "__main__":
   main()
    
#! /usr/bin/python
# -*- coding: UTF-8 -*-

from GlobalParam import *

class RelevancyAtom:
    def __init__(self, id, count):
        self.other_id = id
        self.same_followers_count = count
        self.percent = 0.0
        
class Commentator:
    def __init__(self, id, name):
        self.id = id
        
        # init followers id from file
        self.followers_id = set()
        file_path = self.__get_follower_data_file_path(id, name)
        self.__get_follower_from_file(file_path)
        
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
        
    def debug_output(self):
        print "\n%s followers: %d" % (commentator_id_to_name[self.id], len(self.followers_id))
        for rel_atom in self.relevancy_list:
            print "\t-> %15s %10s %.2f%%" % (commentator_id_to_name[rel_atom.other_id], rel_atom.same_followers_count, rel_atom.percent*100)
        
    def __get_follower_from_file(self, file_path):
        file_handle = open(file_path, "r")
        
        while True:
            line = file_handle.readline()
            if not line:
                break
            
            line = line.strip()
            if len(line) != 0:
                self.followers_id.add(line)
            
        file_handle.close()
        
    def __get_follower_data_file_path(self, id, name):
        return  "%s/%s_%s" % (temp_data_store_dir, name, id)

def cal_follower_relevancy(commentators):
    for i in range(0, len(commentators)):
        for j in range(0, len(commentators)):
            if i ==j:
                continue
            commentators[i].insert_relevancy(commentators[j].id,
                                             len(commentators[i].followers_id.intersection(commentators[j].followers_id)))
        
        commentators[i].cal_other_id_followers_percent()
        commentators[i].sort_relevancy_by_percent()
        
if __name__ == "__main__":
    commentators = []
    for (id, name)  in commentator_id_to_name.items():
        commentators.append(Commentator(id, name))
    
    cal_follower_relevancy(commentators)
    for com in commentators:
        com.debug_output()
    
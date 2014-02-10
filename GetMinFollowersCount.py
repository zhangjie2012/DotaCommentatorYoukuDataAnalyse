#! /usr/bin/python
# -*- coding: UTF-8 -*-

from GlobalParam import *

def get_follower_data_file_path(id, name):
    return  "%s/%s_%s" % (temp_data_store_dir, name, id)
    
def get_follower_counts(file_path):
    file_handle = open(file_path, "r")
    
    follower_count = 0
    while True:
        line = file_handle.readline()
        if not line:
            break
        follower_count += 1
    
    file_handle.close()
    
    return follower_count

def get_min_follower_count():
    min_follower_count = MAXINT
    for (id, name)  in commentator_id_to_name.items():
        follower_count = get_follower_counts(get_follower_data_file_path(id, name))
        if follower_count < min_follower_count:
            min_follower_count = follower_count
    
    return min_follower_count
    
if __name__ == "__main__":
    print get_min_follower_count()
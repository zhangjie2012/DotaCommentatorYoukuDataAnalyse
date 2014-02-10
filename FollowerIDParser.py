#! /usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import time
import os

from GlobalParam import *

def generate_personal_home_url(id):
    return youku_base_url + id

def generate_follower_first_page(id):
    return youku_base_url + id + "/followers/page_1"
    
def generate_follower_next_page(prev_page_url):
    pos = prev_page_url.rfind("_")
    if pos == -1:
        return ""
    return "%s%d" % (prev_page_url[0 : pos+1], + int(prev_page_url[pos+1:]) + 1)

def create_temp_data_dir():
    if os.path.isdir(temp_data_store_dir) is False:
        os.mkdir(temp_data_store_dir)
    
# return value:
#   first: the list of followers list
#   second: if have a except(request timeout)
def get_one_page_follwers_id(page_url):
    try:
        content = urllib2.urlopen(page_url, data=None, timeout = 3).read()
    except:
        print "timeout!"
        return (None, True)
    
    if content == None:
        print "read empty."
        return (None, True)
    
    lines = content.split('\n')
    
    follwers = set()
    for line in lines:
        line = line.lstrip().rstrip();
        m1 = re.search(r"(onclick=\"hz.postHz.+http://i.youku.com/u/)(.+?)(=*?\")", line)
        if m1 != None:
            follwers.add(m1.group(2))
            continue
            
        m2 = re.search("(onclick=\"hz.postHz.+http://u.youku.com/user_show/id_)(.+?)(=*?\.html)", line)
        if m2 != None:
            follwers.add(m2.group(2))
            continue
    return (follwers, False)

# max_page for debug
def get_all_followers_id(id, name, max_page=MAXINT):
    file_handle = open("%s/%s_%s" % (temp_data_store_dir, name, id), "w")
    
    page_count = 0
    next_page = generate_follower_first_page(id)
    print next_page
    
    last_page_followers_count = 0
    while True:
        if page_count > max_page:
            break
        
        print commentator_id_to_name[id], next_page, time.clock(), last_page_followers_count
        
        follwers, have_except = get_one_page_follwers_id(next_page)
        next_page = generate_follower_next_page(next_page)
        
        # if timeout, we need to continue read next pages
        if have_except == True:
            continue
        elif len(follwers) == 0:
            break
            
        for follwer in follwers:
            file_handle.write("%s\n"%follwer)
        
        last_page_followers_count = len(follwers)
        
        page_count += 1
        file_handle.flush()
        
    file_handle.close()
    
def get_commentator_followers():
    max_page = MAXINT
    create_temp_data_dir()
    for (id, name) in commentator_id_to_name.items():
        get_all_followers_id(id, name, max_page)
    
if __name__ == "__main__":
    get_commentator_followers()
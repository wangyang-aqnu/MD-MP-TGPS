# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:01:38 2021

@author: Administrator
"""
import pandas as pd
import numpy as np
import math
def twp(filename,eta):
  str1='./ml/'
  prefs_item_user={}#产生原始项目被评分字典：{项目：{用户：[标签，时间戳]}}
  prefs_item_tag={}
  prefs_user_item={}
  prefs_user_tag={}
  prefs_tag_user={}
  prefs_tag_item={}
  
  rnames=['userid','movieid','tagid','timestamp']
  taggings=pd.read_table(str1+filename,sep='\t',header=None,names=rnames,engine='python')


  tmax=taggings['timestamp'].max()
  tmin=taggings['timestamp'].min()
  #print(tmax,tmin)
  
  
  
  with open(str1+filename,'r') as f:
    lines=f.readlines()
    for line in lines:
      (userid,itemid,tagid,ts)=line.split('\t')
#########################item:{user:score}
      if itemid not in prefs_item_user:
          prefs_item_user.setdefault(itemid,{})
          if userid not in prefs_item_user[itemid]:
              prefs_item_user[itemid][userid]=1.0
          else:
              prefs_item_user[itemid][userid]+=1.0
      else:
           if userid not in prefs_item_user[itemid]:
              prefs_item_user[itemid][userid]=1.0
           else:
              prefs_item_user[itemid][userid]+=1.0
#########################################
#########################item:{tag:score}
      if itemid not in prefs_item_tag:
          prefs_item_tag.setdefault(itemid,{})
          if tagid not in prefs_item_tag[itemid]:
              prefs_item_tag[itemid][tagid]=1.0
          else:
              prefs_item_tag[itemid][tagid]+=1.0
      else:
           if tagid not in prefs_item_tag[itemid]:
              prefs_item_tag[itemid][tagid]=1.0
           else:
              prefs_item_tag[itemid][tagid]+=1.0
#########################################
######################### user:{item:score}
      if userid not in prefs_user_item:
          prefs_user_item.setdefault(userid,{})
          if itemid not in prefs_user_item[userid]:
              prefs_user_item[userid][itemid]=1.0
          else:
              prefs_user_item[userid][itemid]+=1.0
      else:
           if itemid not in prefs_user_item[userid]:
              prefs_user_item[userid][itemid]=1.0
           else:
              prefs_user_item[userid][itemid]+=1.0
#########################user:{tag:score} 
      if userid not in prefs_user_tag:
          prefs_user_tag.setdefault(userid,{})
          if tagid not in prefs_user_tag[userid]:
              prefs_user_tag[userid][tagid]=1.0
          else:
              prefs_user_tag[userid][tagid]+=1.0
      else:
           if tagid not in prefs_user_tag[userid]:
              prefs_user_tag[userid][tagid]=1.0
           else:
               prefs_user_tag[userid][tagid]+=1.0
#########################################
#########################user:{item:score}  tag:{item:score}
      if tagid not in prefs_tag_item:
          prefs_tag_item.setdefault(tagid,{})
          if itemid not in prefs_tag_item[tagid]:
              prefs_tag_item[tagid][itemid]=1.0
          else:
              prefs_tag_item[tagid][itemid]+=1.0
      else:
           if itemid not in prefs_tag_item[tagid]:
              prefs_tag_item[tagid][itemid]=1.0
           else:
              prefs_tag_item[tagid][itemid]+=1.0
#########################################
#########################tag:{item:score} tag:{user:score}
      if tagid not in prefs_tag_user:
          prefs_tag_user.setdefault(tagid,{})
          if userid not in prefs_tag_user[tagid]:
              prefs_tag_user[tagid][userid]=1.0
          else:
              prefs_tag_user[tagid][userid]+=1.0
      else:
           if userid not in prefs_tag_user[tagid]:
              prefs_tag_user[tagid][userid]=1.0
           else:
              prefs_tag_user[tagid][userid]+=1.0
#########################################
              
              
###############################              
#list_all_items_tag(prefs_item_tag):
  list_allitems_tag=[]
  for itemid in prefs_item_tag:
    if itemid not in list_allitems_tag:
      list_allitems_tag.append(itemid)#填加所有项目
################################

################################
#list_all_items_user(prefs_item_user):
  list_allitems_user=[]
  for itemid in prefs_item_user:
    if itemid not in list_allitems_user:
      list_allitems_user.append(itemid)#填加所有项目
#################################

###################################
#list_all_tags_item(prefs_tag_item):
  list_alltags_item=[]
  for tagid in prefs_tag_item:
    if tagid not in list_alltags_item:
      list_alltags_item.append(tagid)#填加所有标签
###################################

###################################
#list_all_tags_user(prefs_tag_user):
  list_alltags_user=[]
  for tagid in prefs_tag_user:
    if tagid not in list_alltags_user:
      list_alltags_user.append(tagid)#填加所有标签
##################################

##################################
#list_all_users_item(prefs_user_item):
  list_allusers_item=[]
  for userid in prefs_user_item:
    if userid not in list_allusers_item:
      list_allusers_item.append(userid)#填加所有用户
###################################
  
###################################
#list_all_users_tag(prefs_user_tag):
  list_allusers_tag=[]
  for userid in prefs_user_tag:
    if userid not in list_allusers_tag:
      list_allusers_tag.append(userid)#所有用户
######################################

  return prefs_item_user,prefs_item_tag,prefs_user_item,prefs_user_tag,prefs_tag_user,prefs_tag_item,\
list_allitems_user,list_allitems_tag,list_allusers_item,list_allusers_tag,list_alltags_user,list_alltags_item
      
      
'''
prefs_item_user,prefs_item_tag,prefs_user_item,prefs_user_tag,prefs_tag_user,prefs_tag_item,\
list_allitems_user,list_allitems_tag,list_allusers_item,list_allusers_tag,list_alltags_user,list_alltags_item=\
twp('test5.dat',60)

print(prefs_item_user)
print("\n")
print(prefs_item_tag)
print("\n")
print(prefs_user_item)
print("\n")
print(prefs_user_tag)
print("\n")
print(prefs_tag_user)
print("\n")
print(prefs_tag_item)
print("\n")
print(list_allitems_user)
print("\n")
print(list_allitems_tag)
'''


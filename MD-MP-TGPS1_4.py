# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 07:28:11 2018

@author: Administrator
"""
import numpy as np
import math

import timeprocess as tp
import loadtestdatauser as ldtuser
import K_items as ki
dic_pre_double,dic_pre_triple,dic_pre_hwL,dic_pre_hwA,dic_cumsum_items,dic_sum2_degree=ki.deg_K_items(r'./ml/35T/sam4/')


###################user_item二分网络
######user_item的权重和user的度
#用户选择项目的评分权重字典R
def prefs_user_item_t(prefs_user_item):
    R_user_to_item={}
    for user in prefs_user_item:
        R_user_to_item.setdefault(user,{})
        for item in prefs_user_item[user]:
            R_user_to_item[user][item]=prefs_user_item[user][item]
    return R_user_to_item


#用户总度数字典
def SD_user_item_t(R_user_to_item):
  SD_user_to_item={}#用户的总度数
  for user in R_user_to_item:
    SD_user_to_item.setdefault(user,0)
    for item in R_user_to_item[user]:
      SD_user_to_item[user]+=R_user_to_item[user][item]
  return SD_user_to_item
##############


######item_user的权重和item的度  
#项目到用户的字典R_item_to_user
def prefs_item_user_t(prefs_item_user):
    R_item_to_user={}#带时间的项目对用户的评分权重
    for item in prefs_item_user:
        R_item_to_user.setdefault(item,{})
        for user in prefs_item_user[item]:
            R_item_to_user[item][user]=prefs_item_user[item][user]
    return R_item_to_user

#项目总度数
def SD_item_user_t(R_item_to_user):
    SD_item_to_user={}#项目的总度数
    for item in R_item_to_user:
        SD_item_to_user.setdefault(item,0)
        for user in R_item_to_user[item]:
            SD_item_to_user[item]+=R_item_to_user[item][user]
    return SD_item_to_user
########################



###################user_tag二分网络
######user_tag的权重和user的度
#用户打标签的字典R
def prefs_user_tag_t(prefs_user_tag):
    R_user_to_tag={}
    for user in prefs_user_tag:
        R_user_to_tag.setdefault(user,{})
        for item in prefs_user_tag[user]:
            R_user_to_tag[user][item]=prefs_user_tag[user][item]
    return R_user_to_tag


#用户总度数字典
def SD_user_tag_t(R_user_to_tag):
  SD_user_to_tag={}#用户的总度数
  for user in R_user_to_tag:
    SD_user_to_tag.setdefault(user,0)
    for item in R_user_to_tag[user]:
      SD_user_to_tag[user]+=R_user_to_tag[user][item]
  return SD_user_to_tag
##############


######tag_user的权重和tag的度  
#标签到项目的字典R_item_to_user
def prefs_tag_user_t(prefs_tag_user):
    R_tag_to_user={}#带时间的项目对用户的评分权重
    for tag in prefs_tag_user:
        R_tag_to_user.setdefault(tag,{})
        for user in prefs_tag_user[tag]:
            R_tag_to_user[tag][user]=prefs_tag_user[tag][user]
    return R_tag_to_user

#标签总度数
def SD_tag_user_t(R_tag_to_user):
    SD_tag_to_user={}#项目的总度数
    for tag in R_tag_to_user:
        SD_tag_to_user.setdefault(tag,0)
        for user in R_tag_to_user[tag]:
            SD_tag_to_user[tag]+=R_tag_to_user[tag][user]
    return SD_tag_to_user
########################



###################item_tag二分网络
######item_tag的权重和item的度
#项目到标签的字典R_item_to_tag
def prefs_item_tag_t(prefs_item_tag):
    R_item_to_tag={}#带时间的项目对用户的评分权重
    for item in prefs_item_tag:
        R_item_to_tag.setdefault(item,{})
        for tag in prefs_item_tag[item]:
            R_item_to_tag[item][tag]=prefs_item_tag[item][tag]
    return R_item_to_tag

#项目总度数(item-tag)
def SD_item_tag_t(R_item_to_tag):
    SD_item_to_tag={}#项目的总度数
    for item in R_item_to_tag:
        SD_item_to_tag.setdefault(item,0)
        for tag in R_item_to_tag[item]:
            SD_item_to_tag[item]+=R_item_to_tag[item][tag]
    return SD_item_to_tag




######tag_item的权重和tag的度
#标签到项目的字典R_item_to_tag
def prefs_tag_item_t(prefs_tag_item):
    R_tag_to_item={}
    for tag in prefs_tag_item:
        R_tag_to_item.setdefault(tag,{})
        for item in prefs_tag_item[tag]:
            R_tag_to_item[tag][item]=prefs_tag_item[tag][item]
    return R_tag_to_item


#标签总度数字典
def SD_tag_item_t(R_tag_to_item):
  SD_tag_to_item={}#用户的总度数
  for tag in R_tag_to_item:
    SD_tag_to_item.setdefault(tag,0)
    for item in R_tag_to_item[tag]:
      SD_tag_to_item[tag]+=R_tag_to_item[tag][item]
  return SD_tag_to_item
############################################## 


##############################################
         
#选择了用户的初始项目资源配置O，引入了随时间衰减因子alpha
def first_resources(prefs_user_item,prefs_user_tag,user):
  O1={}
  O2={}
  for item in prefs_user_item[user]:
    O1.setdefault(item)
    O1[item]=prefs_user_item[user][item]
  for tag in prefs_user_tag[user]:
    O2.setdefault(tag)
    O2[tag]=prefs_user_tag[user][tag]
  return O1,O2


#######################ui:user-item partite network
#first setp:由指定用户的初始项目配置资源传递到用户上
def RC_item_to_user(R_item_user,SD_item_user,O1):
  ST1_R_user={}#第一步后各用户的资源量
  for item in O1:
    if item in R_item_user:
      for user in R_item_user[item]:
        if user not in ST1_R_user:
          ST1_R_user.setdefault(user,0)
          ST1_R_user[user]=O1[item]*R_item_user[item][user]/SD_item_user[item]
        else:
          ST1_R_user[user]+=O1[item]*R_item_user[item][user]/SD_item_user[item]
  return ST1_R_user





#Second setp:由用户传回项目,ST1_R_user为第一步由项目－用户传递后的用户资源量
def RC_user_to_item(R_user_item,SD_user_item,ST1_R_user):
  ST2_R_item={}#第二步后各项目的资源量
  for user in ST1_R_user:
    if user in R_user_item:
      for item in R_user_item[user]:
        if item not in ST2_R_item:
          ST2_R_item.setdefault(item,0)
          ST2_R_item[item]=ST1_R_user[user]*R_user_item[user][item]/SD_user_item[user]
        else:
          ST2_R_item[item]+=ST1_R_user[user]*R_user_item[user][item]/SD_user_item[user]
  return ST2_R_item
#################################

def iteration1(n,R_item_user,SD_item_user,R_user_item,SD_user_item,O1):
    iter_n=0
    ST1_R_user=RC_item_to_user(R_item_user,SD_item_user,O1)
    ST2_R_item=RC_user_to_item(R_user_item,SD_user_item,ST1_R_user)
    while (iter_n <n):
        ST1_R_user=RC_item_to_user(R_item_user,SD_item_user,ST2_R_item)
        ST2_R_item=RC_user_to_item(R_user_item,SD_user_item,ST1_R_user)
        iter_n+=1
    return ST2_R_item

#######################user-item partite network
#first setp:由指定用户的初始项目配置资源传递到用户上
def RC_item_to_tag(R_item_tag,SD_item_tag,O1):
  ST1_R_tag={}#第一步后各用户的资源量
  for item in O1:
    if item in R_item_tag:
      for tag in R_item_tag[item]:
        if tag not in ST1_R_tag:
          ST1_R_tag.setdefault(tag,0)
          ST1_R_tag[tag]=O1[item]*R_item_tag[item][tag]/SD_item_tag[item]
        else:
          ST1_R_tag[tag]+=O1[item]*R_item_tag[item][tag]/SD_item_tag[item]
  return ST1_R_tag


#Second setp:由用户传回项目,ST1_R_user为第一步由项目－用户传递后的用户资源量
def RC_tag_to_item(R_tag_item,SD_tag_item,ST1_R_tag):
  ST2_R_item_tag={}#第二步后各项目的资源量
  for tag in ST1_R_tag:
    if tag in R_tag_item:
      for item in R_tag_item[tag]:
        if item not in ST2_R_item_tag:
          ST2_R_item_tag.setdefault(item,0)
          ST2_R_item_tag[item]=ST1_R_tag[tag]*R_tag_item[tag][item]/SD_tag_item[tag]
        else:
          ST2_R_item_tag[item]+=ST1_R_tag[tag]*R_tag_item[tag][item]/SD_tag_item[tag]
  return ST2_R_item_tag
#################################

def iteration2(n,R_item_tag,SD_item_tag,R_tag_item,SD_tag_item,O1):
    iter_n=0
    ST1_R_tag=RC_item_to_tag(R_item_tag,SD_item_tag,O1)
    ST2_R_item_tag=RC_tag_to_item(R_tag_item,SD_tag_item,ST1_R_tag)
    while (iter_n <n):
        ST1_R_tag=RC_item_to_tag(R_item_tag,SD_item_tag,ST2_R_item_tag)
        ST2_R_item_tag=RC_tag_to_item(R_tag_item,SD_tag_item,ST1_R_tag)
        iter_n+=1
    return ST2_R_item_tag

#######################user-item partite network
#first setp:由指定用户的初始项目配置资源传递到标签上
def RC_item_to_tag_2(R_item_to_tag,SD_item_to_tag,O1):
  ST1_R_tag={}#第一步后各用户的资源量
  for item in O1:
    if item in R_item_to_tag:
      for tag in R_item_to_tag[item]:
        if tag not in ST1_R_tag:
          ST1_R_tag.setdefault(tag,0)
          ST1_R_tag[tag]=O1[item]*R_item_to_tag[item][tag]/SD_item_to_tag[item]
        else:
          ST1_R_tag[tag]+=O1[item]*R_item_to_tag[item][tag]/SD_item_to_tag[item]
  return ST1_R_tag




#Second setp:由标签传到用户,ST1_R_user为第一步由项目－标签传递后的标签资源量
def RC_tag_to_user(R_tag_to_user,SD_tag_to_user,ST1_R_tag):
  ST2_R_user={}#第二步后各用户的资源量
  for tag in ST1_R_tag:
    if tag in R_tag_to_user:
      for user in R_tag_to_user[tag]:
        if user not in ST2_R_user:
          ST2_R_user.setdefault(user,0)
          ST2_R_user[user]=ST1_R_tag[tag]*R_tag_to_user[tag][user]/SD_tag_to_user[tag]
        else:
          ST2_R_user[user]+=ST1_R_tag[tag]*R_tag_to_user[tag][user]/SD_tag_to_user[tag]
  return ST2_R_user


#third setp:由用户传回项目,ST2_R_user为第二步由标签－用户传递后的用户资源量
def RC_user_to_item_2(R_user_to_item,SD_user_to_item,ST2_R_user):
  ST3_R_item={}#第三步后各项目的资源量
  for user in ST2_R_user:
    if user in R_user_to_item:
      for item in R_user_to_item[user]:
        if item not in ST3_R_item:
          ST3_R_item.setdefault(item,0)
          ST3_R_item[item]=ST2_R_user[user]*R_user_to_item[user][item]/SD_user_to_item[user]
        else:
          ST3_R_item[item]+=ST2_R_user[user]*R_user_to_item[user][item]/SD_user_to_item[user]
  return ST3_R_item

#################################

#################################

def iteration3(n,R_item_to_tag,SD_item_to_tag,R_tag_to_user,SD_tag_to_user,R_user_to_item,SD_user_to_item,O1):
    iter_n=0
    ST1_R_tag=RC_item_to_tag_2(R_item_to_tag,SD_item_to_tag,O1)
    ST2_R_user=RC_tag_to_user(R_tag_to_user,SD_tag_to_user,ST1_R_tag)
    ST3_R_item=RC_user_to_item_2(R_user_to_item,SD_user_to_item,ST2_R_user)
    while (iter_n <n):
        ST1_R_tag=RC_item_to_tag(R_item_to_tag,SD_item_to_tag,ST3_R_item)
        ST2_R_user=RC_tag_to_user(R_tag_to_user,SD_tag_to_user,ST1_R_tag)
        ST3_R_item=RC_user_to_item_2(R_user_to_item,SD_user_to_item,  ST2_R_user)
        iter_n+=1
    return ST3_R_item
    

#######################user-item partite network
#first setp:由指定用户的初始项目配置资源传递到用户上
def RC_item_to_user_2(R_item_to_user,SD_item_to_user,O1):
  ST1_R_user={}#第一步后各用户的资源量
  for item in O1:
    if item in R_item_to_user:
      for user in R_item_to_user[item]:
        if user not in ST1_R_user:
          ST1_R_user.setdefault(user,0)
          ST1_R_user[user]=O1[item]*R_item_to_user[item][user]/SD_item_to_user[item]
        else:
          ST1_R_user[user]+=O1[item]*R_item_to_user[item][user]/SD_item_to_user[item]
  return ST1_R_user




#Second setp:由用户传到标签,ST1_R_user为第一步由项目－用户传递后的用户资源量
def RC_user_to_tag(R_user_to_tag,SD_user_to_tag,ST1_R_user):
  ST2_R_tag={}#第二步后各项目的资源量
  for user in ST1_R_user:
    if user in R_user_to_tag:
      for tag in R_user_to_tag[user]:
        if tag not in ST2_R_tag:
          ST2_R_tag.setdefault(tag,0)
          ST2_R_tag[tag]=ST1_R_user[user]*R_user_to_tag[user][tag]/SD_user_to_tag[user]
        else:
          ST2_R_tag[tag]+=ST1_R_user[user]*R_user_to_tag[user][tag]/SD_user_to_tag[user]
  return ST2_R_tag


#third setp:由标签传回项目,ST2_R_tag为第二步由用户－标签传递后的标签资源量
def RC_tag_to_item_2(R_tag_to_item,SD_tag_to_item,ST2_R_tag):
  ST3_R_item={}#第二步后各项目的资源量
  for tag in ST2_R_tag:
    if tag in R_tag_to_item:
      for item in R_tag_to_item[tag]:
        if item not in ST3_R_item:
          ST3_R_item.setdefault(item,0)
          ST3_R_item[item]=ST2_R_tag[tag]*R_tag_to_item[tag][item]/SD_tag_to_item[tag]
        else:
          ST3_R_item[item]+=ST2_R_tag[tag]*R_tag_to_item[tag][item]/SD_tag_to_item[tag]
  return ST3_R_item
#################################

def iteration4(n,R_item_to_user,SD_item_to_user,R_user_to_tag,SD_user_to_tag,R_tag_to_item,SD_tag_to_item,O1):
    iter_n=0
    ST1_R_user=RC_item_to_user_2(R_item_to_user,SD_item_to_user,O1)
    ST2_R_tag=RC_user_to_tag(R_user_to_tag,SD_user_to_tag,ST1_R_user)
    ST3_R_item=RC_tag_to_item_2(R_tag_to_item,SD_tag_to_item,ST2_R_tag)
    while (iter_n <n):
        ST1_R_user=RC_item_to_user_2(R_item_to_user,SD_item_to_user,ST3_R_item)
        ST2_R_tag=RC_user_to_tag(R_user_to_tag,SD_user_to_tag,ST1_R_user)
        ST3_R_item=RC_tag_to_item_2(R_tag_to_item,SD_tag_to_item,ST2_R_tag)
        iter_n+=1
    return ST3_R_item


#######################5-it:tag-item partite network

#first setp:由标签传回项目,ST1_R_user为标签资源量
def RC_tag_to_item_3(R_tag_item,SD_tag_item,O2):
  ST3_R_item_tag={}#标签传播后各项目的资源量
  for tag in O2:
    if tag in R_tag_item:
      for item in R_tag_item[tag]:
        if item not in ST3_R_item_tag:
          ST3_R_item_tag.setdefault(item,0)
          ST3_R_item_tag[item]=O2[tag]*R_tag_item[tag][item]/SD_tag_item[tag]
        else:
          ST3_R_item_tag[item]+=O2[tag]*R_tag_item[tag][item]/SD_tag_item[tag]
  return ST3_R_item_tag
#################################


def iteration5(n,R_tag_to_item,SD_tag_to_item,R_item_to_tag,SD_item_to_tag,O2):
    iter_n=0
    ST3_R_item_tag=RC_tag_to_item_3(R_tag_to_item,SD_tag_to_item,O2)
    ST4_R_tag_item=RC_item_to_tag_2(R_item_to_tag,SD_item_to_tag,ST3_R_item_tag)
    while (iter_n <n):
        ST3_R_item_tag=RC_tag_to_item_3(R_tag_to_item,SD_tag_to_item,ST4_R_tag_item)
        ST4_R_tag_item=RC_item_to_tag_2(R_item_to_tag,SD_item_to_tag,ST3_R_item_tag)
        iter_n+=1
    return ST3_R_item_tag

###############################6-tui
#first setp:由标签传到用户,
def RC_tag_to_user_2(R_tag_to_user,SD_tag_to_user,O2):
  ST2_R_user={}#第二步后各用户的资源量
  for tag in O2:
    if tag in R_tag_to_user:
      for user in R_tag_to_user[tag]:
        if user not in ST2_R_user:
          ST2_R_user.setdefault(user,0)
          ST2_R_user[user]=O2[tag]*R_tag_to_user[tag][user]/SD_tag_to_user[tag]
        else:
          ST2_R_user[user]+=O2[tag]*R_tag_to_user[tag][user]/SD_tag_to_user[tag]
  return ST2_R_user


#third setp:由用户传回项目,ST2_R_user为第二步由标签－用户传递后的用户资源量
def RC_user_to_item_3(R_user_to_item,SD_user_to_item,ST2_R_user):
  ST3_R_item={}#第三步后各项目的资源量
  for user in ST2_R_user:
    if user in R_user_to_item:
      for item in R_user_to_item[user]:
        if item not in ST3_R_item:
          ST3_R_item.setdefault(item,0)
          ST3_R_item[item]=ST2_R_user[user]*R_user_to_item[user][item]/SD_user_to_item[user]
        else:
          ST3_R_item[item]+=ST2_R_user[user]*R_user_to_item[user][item]/SD_user_to_item[user]
  return ST3_R_item

#################################

#################################

def iteration6(n,R_tag_to_user,SD_tag_to_user,R_user_to_item,SD_user_to_item,R_item_to_tag,SD_item_to_tag,O2):
    iter_n=0
    ST2_R_user_tag=RC_tag_to_user_2(R_tag_to_user,SD_tag_to_user,O2)
    ST3_R_item_user=RC_user_to_item_3(R_user_to_item,SD_user_to_item,ST2_R_user_tag)
    ST4_R_tag_item=RC_item_to_tag_2(R_item_to_tag,SD_item_to_tag, ST3_R_item_user)
    while (iter_n <n):
        ST2_R_user_tag=RC_tag_to_user(R_tag_to_user,SD_tag_to_user,ST4_R_tag_item)
        ST3_R_item_user=RC_user_to_item_3(R_user_to_item,SD_user_to_item,ST2_R_user_tag)
        ST4_R_tag_item=RC_item_to_tag_2(R_item_to_tag,SD_item_to_tag, ST3_R_item_user)
        iter_n+=1
    return ST3_R_item_user

#######################################################

#fusion of iui,iti,iuti,itui和it，各条路径产生top-n推荐列表，有重叠的取最大值，
#没有就取该路径物品的资源值，再按资源数降序排列,产生最终的top-推荐列表
#ST2_R_item,ST2_R_item_tag,itui_ST3_R_item,iuti_ST3_R_item实际为list_recom1,list_recom2,list_recom3,list_recom4
def Fus_item(ST2_R_item,ST2_R_item_tag,itui_ST3_R_item,iuti_ST3_R_item,ST3_R_item_tag,tui_ST3_R_item,w1,w2,w3,w4,w5,w6):
  Fus_ST3_R_item={}
  
  for item in ST2_R_item:
    Fus_ST3_R_item.setdefault(item,[0,0])
    Fus_ST3_R_item[item][1]+=w1*ST2_R_item[item]
    Fus_ST3_R_item[item][0]+=1
    
  for item in ST2_R_item_tag:
    if item in Fus_ST3_R_item:
        Fus_ST3_R_item[item][1]+=w2*ST2_R_item_tag[item]
        Fus_ST3_R_item[item][0]+=1
    else:
        Fus_ST3_R_item.setdefault(item,[0,0])
        Fus_ST3_R_item[item][1]+=w2*ST2_R_item_tag[item]
        Fus_ST3_R_item[item][0]+=1
        
  for item in itui_ST3_R_item:
    if item in Fus_ST3_R_item:
        Fus_ST3_R_item[item][1]+=w3*itui_ST3_R_item[item]
        Fus_ST3_R_item[item][0]+=1
    else:
        Fus_ST3_R_item.setdefault(item,[0,0])
        Fus_ST3_R_item[item][1]+=w3*itui_ST3_R_item[item]
        Fus_ST3_R_item[item][0]+=1
    
  for item in iuti_ST3_R_item:
    if item in Fus_ST3_R_item:
        Fus_ST3_R_item[item][1]+=w4*iuti_ST3_R_item[item]
        Fus_ST3_R_item[item][0]+=1
    else:
        Fus_ST3_R_item.setdefault(item,[0,0])
        Fus_ST3_R_item[item][1]+=w4*iuti_ST3_R_item[item]
        Fus_ST3_R_item[item][0]+=1
    
  for item in ST3_R_item_tag:
    if item in Fus_ST3_R_item:
        Fus_ST3_R_item[item][1]+=w5*ST3_R_item_tag[item]
        Fus_ST3_R_item[item][0]+=1
    else:
        Fus_ST3_R_item.setdefault(item,[0,0])
        Fus_ST3_R_item[item][1]+=w5*ST3_R_item_tag[item]
        Fus_ST3_R_item[item][0]+=1
           
  for item in tui_ST3_R_item:
    if item in Fus_ST3_R_item:
        Fus_ST3_R_item[item][1]+=w6*tui_ST3_R_item[item]
        Fus_ST3_R_item[item][0]+=1
    else:
        Fus_ST3_R_item.setdefault(item,[0,0])
        Fus_ST3_R_item[item][1]+=w6*tui_ST3_R_item[item]
        Fus_ST3_R_item[item][0]+=1
     
  return Fus_ST3_R_item

####################################
#对指定用户按两步配置后项目资源量排序，产生排序项目列表
def sorted_R_item_1(list_recom):
    sorted_R_item_list=sorted(list_recom.items(),key=lambda item:item[1],reverse=True)
    #dict(sorted_R_item_list)
    return sorted_R_item_list

####################################
#对指定用户按两步配置后项目资源量排序，产生排序项目列表
def sorted_R_item_2(Fus_ST3_R_item):
    sorted_R_item_list=sorted(Fus_ST3_R_item.items(),key=lambda item:item[1],reverse=True)
    #dict(sorted_R_item_list)
    return sorted_R_item_list
############################

#产生用户未评分项目列表
def unrating_items(user,prefs_user_item,list_allitems_user):#后面需要指定用户
    list_unrating_items=[]
    for item in list_allitems_user:
      if item not in prefs_user_item[user]:
        list_unrating_items.append(item)
        #unratingcou=len(list_unrating_items)
    return list_unrating_items
    
######################################
#对指定用户产生TOP L推荐--给定用户
def list_recs_1(list_unrating_items,sorted_R_item_list,L):
  ncount=0
  list_recom_1={}
  for item in sorted_R_item_list:
    if item in list_unrating_items:
      list_recom_1[item]=sorted_R_item_list[item]
      ncount+=1
    if (ncount==L):break
  return list_recom_1


###########################################
def list_recs(list_unrating_items,sorted_R_item_list,L):
  ncount=0
  list_recom=[]
  for item1,R_item1 in sorted_R_item_list:
    if item1 in list_unrating_items:
      list_recom.append((item1,R_item1))
      ncount+=1
    if (ncount==L):break
  return list_recom
#########################################



#计算推荐列表的项目度
def com_populary(user,list_recom,prefs_user_test,L):
  rec_PO=0.0#推荐列表项目度
  for item,rating in list_recom:
      if item in dic_cumsum_items:
          rec_PO+=dic_cumsum_items[item]['22']      #######注意此处要随sam修改 
  #print(user,HR,"\\n")
  return rec_PO


#计算命中率
def com_HR(user,list_recom,prefs_user_test,L):
  HR=0.0#命中条目数
  for item,rating in list_recom:
      if item in prefs_user_test[user]:
        HR+=1        
  #print(user,HR,"\\n")
  return HR

#计算测试集中评分个数
def count_prefs_user_test(prefs_user_test):
    count_test=0
    for user in prefs_user_test:
        count_test+=len(prefs_user_test[user])
    return count_test
 
#count_test=count_prefs_user_test(prefs_user_test)
#print (count_test)
          
#计算平均位置得分
def com_PS(user,list_recom,prefs_user_test,list_unrating_items):
  
  PR=0.0
  position=0
  p=0#指定用户推荐列表命中测试集次数
  for item,rating in list_recom:
      if item in prefs_user_test[user]:
          p+=1
          position=list_recom.index((item,rating))+1
          #print("用户%s选择%s项目合中%d位置:" %(user,item,position),"\n")
          PR+=position/(len(list_unrating_items))
          #print("用户%s未评分项目数%d.\n" %(user,len(list_unrating_items)))
  #print("用户共命中%d次,该用户命中率合计为%f.\n" %(p,PR))
  return PR,p
#######################################add
#转化prefs_item_user
def tr_prefs_item_alluser(prefs_item_user):
  #prefs_item_user={'1':{'1':3}, '2':{'1':5,'2':3,'3':3}, '3':{'2':5,'3':5},'4':{'1':4,'3':2}}    
  list_item_alluser={}
  for item in prefs_item_user:
    if item not in list_item_alluser:
      list_item_alluser.setdefault(item,[])
      for user in prefs_item_user[item]:
        list_item_alluser[item].append(user)
        #list_item_alluser={'1': ['1'], '2': ['1', '2', '3'], '3': ['2', '3'], '4': ['1', '3']}
  return list_item_alluser
##################################
#转化推荐列表，只需项目  
def tr_list_recom(list_recom):
  #list_recom=[('1',4),('3',3)]
  list_recom_items=[]
  for item,score in list_recom:
    list_recom_items.append(item)
    #list_recom_items=['1', '3']
  return list_recom_items
#############################################
#推荐物品列表完整的list_item_alluser
def recom_list_items_user(list_recom_items,list_item_alluser):
  #list_recom_items=['1','3']
  list_recom_items_user={}
  for item in list_recom_items:
    list_recom_items_user[item]=list_item_alluser[item]
    #list_recom_items_user={'1': ['1'], '3': ['2', '3']}
  return list_recom_items_user  
#########################################
#计算Intra-list diverisity
def ILD(list_item_alluser):
  #list_item_alluser即为list_recom_items_user 
  #list_item_alluser={'1': ['1'], '2': ['1', '2', '3'], '3': ['2', '3'], '4': ['1', '3']}
  ILD_dist=0.0
  H_n=0
  for item_i in list_item_alluser:
    for item_j in list_item_alluser:
        if item_i!=item_j:
            Q_i=0.0
            Q_u=0.0
            H_n+=1
            Q_i=len(set(list_item_alluser[item_i]).intersection(list_item_alluser[item_j]))
            Q_u=len(set(list_item_alluser[item_i]).union(list_item_alluser[item_j])) 
            ILD_dist+=1-Q_i/Q_u
  if H_n==0:
      ILD_dist=-1 #
  else:
    ILD_dist=ILD_dist/H_n
  #ILD_dist=0.5833333333333334
  return ILD_dist
#######################################
###############################
#主程序  
def pers_recom(trainsetname,testsetname,L,tw,delta,w1,w2,w3,w4,w5,w6):
  prefs_item_user,prefs_item_tag,prefs_user_item,prefs_user_tag,prefs_tag_user,prefs_tag_item,\
list_allitems_user,list_allitems_tag,list_allusers_item,list_allusers_tag,list_alltags_user,list_alltags_item\
=tp.twp(trainsetname,tw)
  ##############################################################
  #调用tr_prefs_item_alluser
  list_item_alluser=tr_prefs_item_alluser(prefs_item_user)
  #list_item_alluser={'1': ['1'], '2': ['1', '2', '3'], '3': ['2', '3'], '4': ['1', '3']}
  ############################################################
  prefs_user_test=ldtuser.load_data_prefs_user_test(testsetname)

  avg_HR=0.0#平均命中率
  avg_PR=0.0#平均位置评分
  sum_p=0#总命中条目数
  avg_PO=0.0#平均推荐流行度
  sum_PO=0#推荐总流行度
  ###############################
  avg_ILD=0.0#平均列表内部多样性
  #########################
  #'''调用用户选择项目评分权重函数
  R_user_to_item=prefs_user_item_t(prefs_user_item)
  SD_user_to_item=SD_user_item_t(R_user_to_item)
  

  
  R_item_to_user=prefs_item_user_t(prefs_item_user)
  SD_item_to_user=SD_item_user_t(R_item_to_user) 
  
  ##########################
  
  R_tag_to_item=prefs_tag_item_t(prefs_tag_item)
  SD_tag_to_item=SD_tag_item_t(R_tag_to_item)
  

  R_item_to_tag=prefs_item_tag_t(prefs_item_tag)
  SD_item_to_tag=SD_item_tag_t(R_item_to_tag) 
  
  ##########################
  
  R_tag_to_user=prefs_tag_user_t(prefs_tag_user)
  SD_tag_to_user=SD_tag_user_t(R_tag_to_user)
  
 
  R_user_to_tag=prefs_user_tag_t(prefs_user_tag)
  SD_user_to_tag=SD_user_tag_t(R_user_to_tag) 

  ##########################
  
  
  #测试集评分个数
  count_test=count_prefs_user_test(prefs_user_test)
  
  list_all_recom={}#所有用户推荐列表，为了计算汉明矩离Hij
  
  n_count_user_test=0#测试集中用户数
  #####################################
  n2_count_user_test=0
  #####################################
  for user in prefs_user_test:
    #'''调用用户初始资源配置函数
    p=0#循环返回的条目数
    
    n_count_user_test+=1#用户每循环一次，测试集中用户数加1
    ###################################
    #计算ILD时用户数
    n2_count_user_test+=1
    ##################################
    list_all_recom.setdefault(user,[])#把用户逐条加入所有用户推荐列表
    
    
    O1,O2=first_resources(prefs_user_item,prefs_user_tag,user)
    #print ("指定用户，项目初始资源加权量\n",O,"\n\n")

####################################
    #列出用户user所有未评分列表
    list_unrating_items=unrating_items(user,prefs_user_item,list_allitems_user)
###################################
#iui路径   
    ST2_R_item=iteration1(0,R_item_to_user,SD_item_to_user,R_user_to_item,SD_user_to_item,O1)
    sorted_R_item_list_1=sorted_R_item_1(ST2_R_item)       
    #对user用户利用iui路径产生TOP-L推荐
    list_recom1=list_recs_1(list_unrating_items,dict(sorted_R_item_list_1),L)
###################################
#iti路径
    ST2_R_item_tag=iteration2(0,R_item_to_tag,SD_item_to_tag,R_tag_to_item,SD_tag_to_item,O1)
    sorted_R_item_list_2=sorted_R_item_1(ST2_R_item_tag)       
    #对user用户利用iti路径产生TOP-L推荐
    list_recom2=list_recs_1(list_unrating_items,dict(sorted_R_item_list_2),L)
###################################
#itui路径    
    itui_ST3_R_item=iteration3(0,R_item_to_tag,SD_item_to_tag,R_tag_to_user,SD_tag_to_user,R_user_to_item,SD_user_to_item,O1)
    sorted_R_item_list_3=sorted_R_item_1(itui_ST3_R_item)       
    #对user用户利用itui路径产生TOP-L推荐
    list_recom3=list_recs_1(list_unrating_items,dict(sorted_R_item_list_3),L)
###################################
    #ST2_R_item_tag=RC_tag_to_item(R_tag_item,SD_tag_item,O2)
###################################
#iuti路径
    iuti_ST3_R_item=iteration4(0,R_item_to_user,SD_item_to_user,R_user_to_tag,SD_user_to_tag,R_tag_to_item,SD_tag_to_item,O1)
    sorted_R_item_list_4=sorted_R_item_1(iuti_ST3_R_item)       
    #对user用户利用iuti路径产生TOP-L推荐
    list_recom4=list_recs_1(list_unrating_items,dict(sorted_R_item_list_4),L)
    

#################################  
#ti路径
    ST3_R_item_tag=iteration5(0,R_tag_to_item,SD_tag_to_item,R_item_to_tag,SD_item_to_tag,O2)
    sorted_R_item_list_5=sorted_R_item_1(ST3_R_item_tag)       
    #对user用户利用ti路径产生TOP-L推荐
    list_recom5=list_recs_1(list_unrating_items,dict(sorted_R_item_list_5),L)
#################################     
#tui路径
    tui_ST3_R_item=iteration6(0,R_tag_to_user,SD_tag_to_user,R_user_to_item,SD_user_to_item,R_item_to_tag,SD_item_to_tag,O2)
    sorted_R_item_list_6=sorted_R_item_1(tui_ST3_R_item)       
    #对user用户利用ti路径产生TOP-L推荐
    list_recom6=list_recs_1(list_unrating_items,dict(sorted_R_item_list_6),L)
#################################          

    Fus_ST3_R_item=Fus_item(list_recom1,list_recom2,list_recom3,list_recom4,list_recom5,list_recom6,w1,w2,w3,w4,w5,w6)
    sorted_R_item_list=sorted_R_item_2(Fus_ST3_R_item)
    
    #print("推荐列表:\n",sorted_R_item_list)
    
    
    #对user用户产生TOP-L推荐
    list_recom=list_recs(list_unrating_items,sorted_R_item_list,L)
    #print("TOP-L推荐列表:\n",list_recom)
####################################################
    ############################################
    #调用tr_list_recom
    list_recom_items=tr_list_recom(list_recom)
    #print(list_recom_items)
    #############################################
    #调用recom_list_items_user
    list_recom_items_user=recom_list_items_user(list_recom_items,list_item_alluser)
    #print(list_recom_items_user)
    ############################################
    for list_recom1 in list_recom:
        list_all_recom[user].append(list_recom1[0]) #把user用户推荐列表加入所有用户推荐列表中
    #####################################
    #user-lever的ILD计算
    ILD_dist=ILD(list_recom_items_user)
    if ILD_dist==-1:
      n2_count_user_test-=1
    else:
      avg_ILD+=ILD_dist
    #####################################
    #推荐项目流行度计算
    rec_PO=com_populary(user,list_recom,prefs_user_test,L)
    sum_PO+=rec_PO
    
    
    #命中率计算
    HR=com_HR(user,list_recom,prefs_user_test,L)
    #print('命中%d个项目:'%(n))
    #print('命中率为:%.4f%%'%(HR*100))
    avg_HR+=HR
    
    #位置得分计算
    PR,p=com_PS(user,list_recom,prefs_user_test,list_unrating_items)
    #print('平均位置得分为%.8f'%(PR))
    sum_p+=p
    #print("sum_p",sum_p)
    avg_PR+=PR
  
    
  #计算汉明矩离
  Ham_dist=0.0
  H_n=0
  for user_i in list_all_recom:
      for user_j in list_all_recom:
          if user_i!=user_j:
              Q=0.0
              H_n+=1
              Q=len(set(list_all_recom[user_i]).intersection(list_all_recom[user_j]))
              
              Ham_dist+=1-Q/L
  
  Ham_dist=Ham_dist/H_n
              
  #计算精确率，即命中次数/L
  Apris=sum_p/(n_count_user_test*L)
  
  #计算推荐平均流行度
  avg_PO=sum_PO/(n_count_user_test*L)
  
  #print ("总命中",avg_HR)
  #print ("\npopulation：",count_test)
  avg_HR=avg_HR/count_test #平均命中率
 
  #avg_PR=avg_PR/sum_p #平均位置得分
  ######################################
  #计算推荐的平均ILD
  avg_ILD=avg_ILD/n2_count_user_test
  ######################################
  return avg_HR,avg_ILD,Ham_dist,avg_PO,Apris


f=open('MD-MP-TGPS1_4.txt','a')
f.write("u4:\n")
for i in range(10,110,10):
#for de in np.arange(0,1.01,0.01):
  avg_HR,avg_ILD,Ham_dist,avg_PO,Apris=pers_recom("train4.dat","test4.dat",i,15,1,1,1,1,1,1,1)
  f.write(str(Apris)+'\t'+str(avg_HR)+'\t'+str(Ham_dist)+'\t'+str(avg_PO)+'\t'+str(avg_ILD))
  f.write("\n")
  f.flush()
f.close()
        
    
    
               
            















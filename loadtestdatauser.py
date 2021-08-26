# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:29:13 2018

@author: Administrator
"""

#产生测试数据用户评分数据
def load_data_prefs_user_test(filename):
    str1='./ml/'
    prefs_user_test={}
    with open(str1+filename,'r') as f:
      lines=f.readlines()
      for line in lines:
        (userid,itemid,tagid,ts)=line.split('\t')
        if userid not in prefs_user_test:
          prefs_user_test.setdefault(userid,{})
          if itemid not in prefs_user_test[userid]:
            prefs_user_test[userid][itemid]=1.0
          else:
            prefs_user_test[userid][itemid]+=1.0
        else:
           if itemid not in  prefs_user_test[userid]:
               prefs_user_test[userid][itemid]=1.0
           else:
               prefs_user_test[userid][itemid]+=1.0  
    return prefs_user_test


'''
prefs_user_test=load_data_prefs_user_test("test5.dat")
print(prefs_user_test)



if __name__=="__main__":
    prefs_user_test=load_data_prefs_user_test("test1.dat")
    print("读取成功")
    print("用户已选项目个数：",len(prefs_user_test),"个，字典如下：")
    print(prefs_user_test)
'''

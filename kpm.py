
import time
from functools import wraps
  
def fn_timer(function):
  @wraps(function)
  def function_timer(*args, **kwargs):
    t0 = time.time()
    result = function(*args, **kwargs)
    t1 = time.time()
    print ("Total time running %s: %s seconds" %
        (function.func_name, str(t1-t0))
        )
    return result
  return function_timer 

  
def same_long(a, b):
    long = 0
    for i in a:
        for j in b:
            if i == j and len(i) > long:
                long = len(i)
    return long

def get_match_value(f):
    value = []
    for i in range(len(f)):
        pre = f[:i]
        suf = f[1:i+1]
        pre_list = []
        for i in range(len(pre)):
            #print 'pre', pre[:i+1] ,
            pre_list.append(pre[:i+1])
       # print 
        suf_list = []
        for i in range(len(suf)):
            #print 'suf', suf[-i:] ,
            suf_list.append(suf[-i:])
        #print 
        #print pre_list, suf_list
        value.append(same_long(pre_list, suf_list))
        
    return value

#@fn_timer
def kmp(o,f):
    value = get_match_value(f)    
    i = 0
    while i < len(o):
    
        #print i
        flag = True
        
        had_match_digt = 0
        for ii in range(len(f)):
            
            if f[ii] != o[ii+i]:
                flag = False
                step = had_match_digt - value[ii]
                step = step > 1 and step or 1
                i += step #had_match_digt - value[ii]
                break
            else:
                had_match_digt += 1
        
        if flag:
            #print o[i: i+len(o)]
            return i
            
    
        
    return False
    
#@fn_timer 
def x_find(a,b):
    return a.find(b)

    
a="1232132ABCDAB132ABCDABsdfDAA1321312321ABCDAsdfBDAA32ABdsfABCDABsdfDAACDAB1sdf321312sdf3122ABCDABABCDABDAA324324324AABCDABDAAABCDABDABCDAB3242342342ABCDABDA34324324324324324324324324ABCDABsABABCDABDAAA"
b='ABCDABDAAA'


from timeit import Timer

tkmp=Timer("kmp(a,b)","from __main__ import kmp, a, b")
tfind=Timer("x_find(a,b)","from __main__ import x_find, a, b")

print tkmp.timeit(100)
print tfind.timeit(100)

#print kmp(a,b) 
#print x_find(a,b)











 
 
 
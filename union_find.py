#并查集(Union-Find)算法介绍
#url http://blog.csdn.net/dm_vincent/article/details/7655764


class UN(object):
    def __init__(self, x):
        """
        #初始化数组对象，
        @group  分配分组，所有联通对象在同一个组
        @size  计算累计分组大小
        """
        self.x = x
        self.group = {}
        self.size = {}
        self.count = len(x)
        for i in x:
            self.group[i] = i
            self.size[i] =1
        
    def find(self, a):
        """
        查询数字所在的分组树的顶点
        """
        return self.group[a]
        while self.group[a] != a:
            a = self.group[a]
        return p
            
    def connected(self, a, b):
        '''
        判断是否联接，其分组的树顶点相同
        '''
        return self.find(a) == self.find(b)
        
    def union(self, a, b):
        '''
        查询所在组的树顶点，
        如果是非链接的，把小树，链接到大树下，树的高度决定 find 效率，尽量控制树的高度
        '''
        g_a = self.find(a)
        g_b = self.find(b)
        
        if g_a == g_b:
            print "had union"
            return 
        
        if self.size[g_a] < self.size[g_b]:        
            self.group[g_a] = g_b
            self.size[g_b] += self.size[g_a]
            
        else:
            self.group[g_b] = g_a
            self.size[g_a] += self.size[g_b]
            
            
        self.count -= 1 
    
    def count(self):
        return self.count
           
                
x=[1,2,3,4,5,6,7,8,9,10]
u = UN(x)



print u.union(1,2)
print u.group
print u.size
print u.union(3,4)
print u.group
print u.size
print u.union(2,4)
print u.group
print u.size




        
        
    
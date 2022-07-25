#!/usr/bin/env python
# coding: utf-8

# In[251]:


#import_Libraries
import numpy as np
from matplotlib import pyplot as plt
import math
from datetime import datetime


# In[464]:


class Node:
    #این کلاس به ایجاد درایه های ماتریس میپردازد هر نود دارای یک مقدار کلید هست که در آن آدرس(مختصات درایه
    # و مقدار آن درایه نگه داری می شود
    def __init__(self,row_number,col_number,value):
        self.key = (row_number,col_number)
        self.row_number = row_number
        self.col_number = col_number
        self.value = value
        
    def find_Nodes(array):
        # به این تابع یک آرایه پاس داده میشود و از آن آرایه مقادیر غیر صفر را بر میگرداند
        #Finding zeros Nodes and return them from an array
        output=[]
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j]!=0:
                    New_Node=Node(i,j,array[i][j])
                    output.append(New_Node)
        return [output,array]
                    
        
class mat:
    
    def __init__(self,col,row,count_full=0,mat_type = None):
        self.col = col
        self.row = row
        self.keys = []
        self.dict = {}
        self.coo = [self.dict]
        #self.coo saves matirx using COO method.
        self.count_full = len(self.keys)
        #it count nomber of full Nodes in matrix it's equal to Len of keys
        self.mat_type = None
        self.sparsity = 1-(len(self.keys)/(self.row*self.col)) 
        self.ord=[]

        
    def make_coo(self):
        self.coo.append([self.col,self.row])
        
    def convert_to_matrix(array):
        #getting an array and convrt it to a matrix
        new_mat = mat(len(array),len(array[0]))
        new_mat.ord = Node.find_Nodes(array)[1]
        for i in Node.find_Nodes(array)[0]:
            new_mat.insert(i)
        new_mat.find_type()
        return new_mat
        
    def insert(self,New_Node):   
        #insert a New Node to the matrix
        if New_Node.key not in self. keys:
            if New_Node.value!=0:
                self.keys.append(New_Node.key)
                self.dict[New_Node.key] = New_Node.value
                self.ord[New_Node.key[0]][New_Node.key[1]]=New_Node.value
            #else:
                    #self.ord[New_Node.key[0]][New_Node.key[1]]= 0 
        else:
            self.keys.remove(New_Node.key)
            mat.insert(self,New_Node)
        
        if New_Node.key[0]>self.row:
            self.row += 1
        if New_Node.key[1]>self.col:
            self.col += 1
        
        self.find_type()

        
    
    def find_type(self):
        #finding the Type of matrix, if the density was grater than 60% the matrix is not sparse
        self.sparsity = 1-(len(self.keys)/(self.col*self.row))
        
        if (len(self.keys)/(self.col*self.row)) > 0.6:
            self.mat_type = "ordinary"
        else:
            self.mat_type = "sparse"
        
        return self.mat_type
    
    def remove_Node(self,Node_adrees):
        self.ord[Node_adrees[0]][Node_adrees[1]]= 0
        self.keys.remove(Node_adrees)
        self.dict.pop(Node_adrees)
        self.find_type()

    def plus_function(mat1,mat2):
        #using plus function for COO matrix, this function uses to add two sparse matrix
        sum_mat = mat(mat1.row,mat1.col)
        sum_mat.ord = mat1.ord[:][:]
        for i in mat1.keys:
                sum_mat.insert(Node(i[0],i[1],(mat1.coo[0].get(i))))
            
        for i in mat2.keys:
            if i not in sum_mat.keys:
                sum_mat.insert(Node(i[0],i[1],(mat2.coo[0].get(i))))
            else: 
                sum_mat.insert(Node(i[0],i[1],(mat1.coo[0].get(i)+mat2.coo[0].get(i))))
        
        return sum_mat
    
    def return_value(self,key):
        #returning the value of a matrix by getting the key
        if key in self.keys:
            return self.coo[0].get(key)
        else:
            return "The key's value is null"
    
    def regular_plus_function(array1,array2,n):
        #using plus function for regular matrix, this function uses to add two regular matrix
        sum_mat=array1[:][:]
        for i in range(n):
            for j in range(n):
                sum_mat[i][j]=array1[i][j]+array2[i][j]
        return sum_mat
    
    def auto_plus(mat1,mat2):
        # این تابع با توجه به شلوغی ماتریس تصمیم میگیرد که از چه نوع جمعی استفاده کند
        if mat1.find_type == "sparse" or mat1.find_type == "sparse":
            mat.plus_function(mat1,mat2)
            
        if mat1.find_type == "ordinary" and mat1.find_type == "ordinary":
            mat.regular_plus_function(mat1.ord,mat2.ord)
    
    def ordinary_multiply(array1,array2):
        #از این تابع برای ضرب ماتریس های شلوغ به شکل معمولی استفاده میشود.
        result=[[0 for i in range(len(array2[0]))] for j in range(len(array1))]
        for i in range(len(array1)):
            for j in range(len(array2[0])):
                for k in range(len(array1[0])):
                    result[i][j]+= array1[i][k]*array2[k][j]
        return result

        
    def sparse_multiply(mat1,mat2):
        #این تابع دو ماتریس خلوت را به سبک ماتریس بهینه شده در هم ضرب میکند
        result=[[0 for i in range(mat2.col)] for j in range(mat1.row)]
        for c in mat1.dict:
            i=c[0]
            k=c[1]
            for d in mat2.dict:
                if k==d[0]:
                    j=d[1]
                    result[i][j]+=mat1.dict[(i,k)]*mat2.dict[(k,j)]
        
        return(mat.convert_to_matrix(result))
    
    def auto_multiply(mat1,mat2):
                # این تابع با توجه به شلوغی ماتریس تصمیم میگیرد که از چه نوع ضربی استفاده کند
        if mat1.mat_type == "sparse" or mat1.mat_type == "sparse":
            mat.spare_multiply(mat1,mat2)
            
        if mat1.mat_type == "ordinary" and mat1.mat_type == "ordinary":
            mat.ordinary_multiply(mat1,mat2)
            
    def printmat(mat):
        #ماتریس را برمیگرداند
        if mat.mat_type == "sparse":
            print(mat.coo)
            
        else:
            
            print(mat.ord)
           
        
     


# In[378]:


#making test cases
def make_random_mat(row,col,non_zeros):
    #این تابع ماتریس های تصادفی به شکل ماتریس بهینه شده خلوت ایجاد میکند ورودی اول و دوم به
    #ترتیب تعداد سطر و ستون ها و ورودی سوم تعداد عناصر غیر صفر است
    #making COO random matrix
    randmat = [([0]*row) for i in range(col)]
    count = 0
    while count<non_zeros:
        i = np.random.randint(0,row)
        j = np.random.randint(0,col)
        if randmat[i][j]==0:
            randmat[i][j]=np.random.randint(1000)
            count+=1
    outputmat = mat.convert_to_matrix(randmat)
    outputmat.ord = 
    return outputmat


def make_random_ordinary_mat(row,col,non_zeros):
    #این تابع به سبک تابع بالا است منتهی ماتریس عادی میسازد
    #making ordinary random matrix for test cases
    randmat = np.zeros((row,col),dtype = int)
    count = 0
    while count<non_zeros:
        i = np.random.randint(0,row)
        j = np.random.randint(0,col)
        if randmat[i][j]==0:
            randmat[i][j]=np.random.randint(10000)
            count+=1
    return randmat


# In[386]:


my_mat = make_random_mat(4,4,5)
my_mat.printmat()


# In[388]:


my_mat.insert(Node(0,3,121))
my_mat.printmat()


# In[391]:


my_mat.return_value((0,2))


# In[389]:


my_mat.mat_type


# In[460]:


my_mat2=make_random_mat(3,3,7)
my_mat2.mat_type


# In[461]:


rndmat1 = make_random_mat(5,5,10)
rndmat2 = make_random_mat(5,5,7)
rndmat1.printmat()
rndmat2.printmat()
sum_mat = mat.plus_function(rndmat1,rndmat2)
sum_mat.printmat()


# In[459]:


new_node=Node(1,1,620)
rndmat2.ord[new_node.key[0]][new_node.key[1]]


# In[463]:


rndmat1 = make_random_mat(5,5,10)
rndmat2 = make_random_mat(5,5,7)
rndmat1.printmat()
rndmat2.printmat()
sum_mat = mat.sparse_multiply(rndmat1,rndmat2)
sum_mat.printmat()


# In[467]:


Node.find_Nodes([[1,0,2],[0,1,0]])[0]


# In[ ]:





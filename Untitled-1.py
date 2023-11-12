""" 素数（prime number）又称质数，有无限个。除了1和它本身以外不再被其他的除数整除。

以下实例可以输出指定范围内的素数： """
""" def num(n) :
    for i in range(2,n) :
        if n%i==0:
            break
        if i==n-1 :
                print(n)
        
def pr(q,h):
    for i in range(q,h+1) :
        num(i)
pr(1,100) """
# 整数的阶乘（英语：factorial）是所有小于及等于该数的正整数的积，0的阶乘为1。即：n!=1×2×3×...×n。
""" def jiecheng(n) :
    sum=1
    for i in range(1,n+1) :
        
        sum=sum*i
    print(sum)

jiecheng(4) """

""" # 以下实例演示了如何实现九九乘法表：
def jiujiu(n) :
    for i in range(1,n+1) :
        
        for m in range(1,i+1) :
            print("{.5}x{}={}".format(i,m,i*m),end=" ")
        print()
        
    
    

#  """
# import time  # 引入time模块

# ticks = time.time()
# print ("当前时间戳为:", ticks)

# import time

# localtime = time.localtime(time.time())
# print ("本地时间为 :", localtime)
#  """
# #  30 个人在一条船上，超载，需要 15 人下船。

# # 于是人们排成一队，排队的位置即为他们的编号。

# # 报数，从 1 开始，数到 9 的人下船。

# # 如此循环，直到船上仅剩 15 人为止，问都有哪些编号的人下船了呢？

# # 计算公式 13 + 23 + 33 + 43 + …….+ n3

# # 实现要求：

# # 输入 : n = 5

# # 输出 : 225

# # 公式 : 13 + 23 + 33 + 43 + 53 = 225


# # 输入 : n = 7

# # 输入 : 784

# # 公式 : 13 + 23 + 33 + 43 + 53 + 63 + 73 = 784
""" n=int(input())
sum=0
for i in range(1,n+1):
    sum=i**3+sum
print(sum) """
# 定义一个整型数组，并计算元素之和。

# 实现要求：

# 输入 : arr[] = {1, 2, 3}

# 输出 : 6

# 计算: 1 + 2 + 3 = 6
""" a=(input())
l=[int(x) for x in a.split(",")]
print(l) """
# 定义一个整型数组，并将指定个数的元素翻转到数组的尾部。

# 例如：(ar[], d, n) 将长度为 n 的 数组 arr 的前面 d 个元素翻转到数组尾部。

# 以下演示了将数组的前面两个元素放到数组后面。
""" def reverse(arr,d,n):
    if d>n:
        print("sb")
    for i in range(n):
        tem=arr.pop(0)
        arr.append(tem)
    print(arr)
    
    
reverse([1,2,3,4],2,3) """
#使用拼接也好使
""" def reverse(arr,d,n):
    print(arr[d:])
    print(arr[:d])
    print(arr[1:3])
    if d>n:
        print("sb")
    arr=arr[d:]+arr[:d]
    print(arr)
    
reverse([1,2,3,4],2,9) """
# 定义一个列表，并将列表中的头尾两个元素对调。
""" def re(arr):
    n=len(arr)
    arr[0],arr[n-1]=arr[n-1],arr[0]
    print(arr)
re([1,2,3,4]) """
# 定义一个列表，并判断元素是否在列表中。
""" def j(arr,n):
    if n in arr:
        print ("you")
    else:
        print("meiyou")
j([1,2,3],2) """
""" def find(arr,m):
    try:
        arr.index("m")
    except: """

""" def clone(list):
    return [x for x in list]


print(clone([1,2,3])) """
# 定义一个列表，并计算某个元素在列表中出现的次数。
# def fre(list,n):
#     i=0
#     for x in list:
#         if x==n:
#             i+=1
#     print(i)
list=[1,2,3,1,1,1]
# print(list.count(1))
# print(sum(list))
# 计算元素之积
""" sum=1
for i in list:
    sum*=i
print (sum) """

""" # 给定一个字符串，然后移除指定位置的字符：
test_str = "Runoob"
 
# 输出原始字符串
print ("原始字符串为 : " + test_str)
 
# 移除第三个字符 n
new_str = ""
 
for i in range(0, len(test_str)):
    if i != 2:
        new_str = new_str + test_str[i]
        print(new_str + test_str[i])

print ("字符串移除后为 : " +new_str)
 """
#  给定一个字符串，然后判断指定的子字符串是否存在于该字符串中。
""" def str(str, n):
    for i in range(0,len(str)):
        if n==str[i]:
            print("zai") """
# a="boost"
# print(a.find("t"))
class force:
    def __init__(self) -> None:
        pass
    def __eq__(self, __value: object) -> bool:
        pass
a=force()
b=force()
print(a=b)
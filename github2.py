#Reverse of the elements in a list

l = [10,22,43,67,32]
print("List =",l)
n = []
for i in range(len(l) -1,-1,-1):
    n.append(l[i])
print("Reverse list=",n)

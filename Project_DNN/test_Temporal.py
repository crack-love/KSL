from numpy import array

length = int(10)
seq = array([i/float(length) for i in range(length)])
x = seq.reshape(2, 5, (1, 2))
y = seq.reshape(1, length)

print(seq)
print(x)
print(y)
import matplotlib.pyplot as plt

x=1
p=1
while True:
    p = p * (365 - x +1)/365
    if 1-p >0.5:
        break
    x+=1

print(x)
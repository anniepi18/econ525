"""Jan 17, 2025"""
# int, float, complex
# j = i in python as in i the imaginary number 

roark = 2
roark = complex(roark)
test1 = bool(1)
test2 = False
display = "Hello Econ 493"
attendance = 31
newvar = roark + attendance
display2 = f"{display} , did you get your coffee? Todays attendance is: {attendance} students."
print(display2)
x = [0,1,2,3,4,5, 'end of my list']
y= x[2]
z = [5,4,3,2,1]
z.append(0) #adds 0 to the end of z
z.extend(x) #adds x to the end of z
print(z)
print(z.count(1)) #instances of 1 in z
print(y)
print(len(x))

#del z[:5]
#print(z)

w = set(z)
v = set(x)
u = w.difference(v)
u = w.intersection(v)
print(u)



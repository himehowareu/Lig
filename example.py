from dataclasses import dataclass
print(str("this is a test"),end='')
test = "test"
def sayHello(prompt):
  name= ""
  name= input(prompt)
  print(str("Hello "),end='')
  print(str(name),end="\n")
sayHello("john")
@dataclass
class person():
  age:int
  name:str
def greet(customer):
  print(str("hello "),end='')
  print(str(customer.name),end='')
john = person(25,"john")
greet(john)
a = 0
def dec(x):
  v = 0
  v=x-1
  return v
while a > 10:
  print(str(a),end='')
john.age=john.age+1
print(str(john.age),end="\n")
def canDrink(customer):
  if customer.age >= 21:
    return True
  else:
    return False

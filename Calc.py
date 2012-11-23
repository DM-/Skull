# This file is the calculator of the bot, the Calc() function is a wrapper for everything in here and should be the only thing called
# It will calculate the input, in the form of a string or a list, and return a number as a result.

#Imports
from random import randrange
import operator
import re
#regexes
number = re.compile('\d+')
cutter = re.compile('([+\-*d^/])')
nowhite= re.compile("\s")
#operator precedence
OpPrec={'+':2,'-':2,'*':3,"/":3,"d":8,"^":4}
#operator association, l for left, r for right
OpAsso={'+':'l','-':'l','*':'l',"/":'l',"d":'l',"^":'r'}

def do_op(op, lhs, rhs):
  return {'+': operator.add,'-': operator.sub,'*': operator.mul,'/':operator.div,'^':operator.pow,'d':dice}[op](lhs, rhs)
def dice(num, sides):
    return sum(randrange(sides)+1 for die in range(num))
#reverse polish notation calculator, easier to convert to postfix then calculate.
def rpn(lst, stack):
  if lst == []:
    return stack
  if lst[0] in '-+*/d':
    return rpn(lst[1:], [do_op(lst[0], stack[1], stack[0])] + stack[2:])
  return rpn(lst[1:], [int(lst[0])] + stack)
#preper to set everything up for SYA
def SYAW(Input):
  # lemme walk this through, strip the input of whitespace both at the ends and inside
  # then split it along operators and then flip it so we can use .pop() (faster).
  return SYA(cutter.split(nowhite.sub("",Input))[::-1],[],[])
def SYA(Input,side, stack):
  if (not Input) and (not side):
    return stack
  elif not Input:
    while side:
      stack.append(side.pop())
    return SYA(Input,side,stack)
  #since we aren't done, time to start working. Pop off the next token and start.
  a=Input.pop()

  if number.match(a):
    stack.append(a)
    return SYA(Input,side,stack)
  if OpAsso[a] == 'l':
    while side and (OpPrec[a]<=OpPrec[side[-1]]):
      stack.append(side.pop())
    side.append(a)
    return SYA(Input,side,stack)
  if OpAsso[a] == 'r':
    while side and OpPrec[a]<OpPrec[side[-1]]:
      stack.append(side.pop())
    side.append(a)
    return SYA(Input,sie,stack)

def Calc(Input):
  #other files will only call Calc from here, this should basically turn the file into a black box.
  #if str, go through the normal route prep it and all
  if type(Input)==str:
    return rpn(SYAW(Input),[])[0]
  #if list, assume preformated. Just flip and pass to core functions.
  elif type(Input)==list:
    return rpn(SYA(input[::-1],[],[]),[])



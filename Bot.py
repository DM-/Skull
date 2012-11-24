#lesse now, how does one make an irc bot again?
#test
import sys
import re
import math
from Calc import Calc
from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.application import internet, service
from random import randrange
#Constants
def dice(num, sides):
    return sum(randrange(sides)+1 for die in range(num))
diceroll=re.compile("\d+d\d+.*")
nickname_pattern = re.compile('^[a-zA-Z][a-zA-Z ]*$')
CHAT, ACTION, SYSTEM_ACTION = xrange(3)
def color(string, color):
    return '\003%s %s \017 ' % (color,string)
#Colors
WHITE = 0
BLACK = 1
BLUE = 2
GREEN = 3
RED = 4
BROWN = 5
PURPLE = 6
ORANGE = 7
YELLOW = 8
LIGHTGREEN = 9
CYAN = 10
LIGHTCYAN = 11
LIGHTBLUE = 12
PINK = 13
GREY = 14
LIGHTGREY = 15 

BOLD = 002,
INVERSE = 026,
UNDERLINE = 037

DEFAULT_COLOR = 017,
#Vars
nickToUse="MyBot"
specialSymbol=","
HOST, PORT = 'irc.freenode.net', 6667
# sideways implementations of a regex dict
def InRegDict(dic,test):
	for i in dic:
		if i.match(test):
			return True
	return False
def GetRegDict(dic,test):
	for i in dic:
		if i.match(test):
			return dic[i]
	False
#remember to add a function for locaion
def ModDoSF(test,adj,DoSF):
	#what we're gonna return
	val=''
	for i in adj:
		# DHAdj must be a regdict, DHAdj stands for DH adjective. adj stands for adjective. Because of problems in dict, need to use has_key and get
		if InRegDict(DHAdj,i):
			val.append(GetRegDict(DHAdj,i)(i,test,DoSF))
	return (val,DoSf)
DHAdj1=[re.compile(x, re.I) for x in ["dark(ness)?","Diff[a-z]*Terrain","Wors[et]?Terrain","Shoot[a-b]*Melee","ExtremeRange","Fatigue[d]*","Fog","(2|(two))to(1|(one))","(3|(three))to(1|(one))","Helpless","High(er)?ground","LongRange","PointBlank","ShortRange","Stun(n)?(ed)?Target","UnawareTarget","Weather1","Weather2" ]]
DHAdj2=[re.compile(x, re.I) for x in []]
DHAdj=dict(zip(DHAdj1,DHAdj2))
def ModDif(test,adj,Diff):
	d=Diff
	for i in adj:
		if InRegDict(DHDiff,i):
			d+=GetRegDict(DHDiff,i)(i,test,Diff)
	return d
DHDiff1=[""]
DHDiff2=
DHDiff
class BotProtocol(irc.IRCClient):
	nickname = nickToUse
	def signedOn(self):
		#join channels listed on signon
		for channel in self.factory.channels:
			self.join(channel)

	def privmsg(self, user, channel, message):
		nick, loool, host = user.partition('!')
		message = message.strip()
		def FuncOut(functiontouse,*args):
			# Add callbacks to deal with whatever the command results are.
			# maybeDeferred will always return a Deferred.
			d= defer.maybeDeferred(functiontouse,*args)
			if ispriv:
				d.addCallback(self._send_message,nick)
			else:
				d.addCallback(self._send_message,channel,nick)
		#use V to set command symbol
		if not message.startswith(specialSymbol):
			return #we don't care for this
		command, sep, rest = message.lstrip(specialSymbol).partition(' ')
		#check beforehand if msg is channel or not When channel == self.nickname, the message was sent to the bot
		ispriv = 0
		if channel == self.nickname:
			ispriv = 1
		# Get the function corresponding to the command given.
		func = getattr(self, 'do_' + command, None)
		# Or, if there was no function, try and catch innate functions.
		if func is None:
			if diceroll.match(command):
				func=getattr(self,'do_roll',None)
				FuncOut(func,command)
				return
			else:
				return
		FuncOut(func,rest)
		

	def _send_message(self, msgval, target, nick=None):
		msg=0
		if nick:
			msg = '%s, %s' % (nick, msgval[0])
		else:
			msg=msgval[0]
		if msgval[1]==0:
			self.msg_other(target,msg)
		elif msgval[1]==1:
			self.msg_info(target,msg)
		elif msgval[1]==2:
			self.msg_err(target,msg)
		elif msgval[1]==3:
			self.describe(target,msgval[0])
		else:
			self.msg_other(target,msg,msgval[1])
	def msg_err(self, target,msg):
		self.msg(target,color('*** %s ***' % msg, RED))
	def msg_info(self,target, msg):
		self.msg(target,color('%s' % msg, YELLOW))
	def msg_other(self,target, msg, color_t=None):
		if color_t is not None:
			self.msg(target,color(msg, color_t))
		else:
			self.msg(target,msg)
	def do_dance(self,whatevers):
		return ("dances",3)
	def do_ping(self, rest):
		return ('Pong.',0)
	def do_roll(self, rest):
		try:
			return(Calc(rest))
		except:
			return ("That ain't a polite dice roll",2)
	# sanity check, currently useless. returning 0 means sane. ie. not insane
	def insane(self,version,rest):
		return 0
	def do_dhroll(self,rest):
		try:
			z=rest.split(" ")
			#why are we using z.pop below? to standardize the output of course!
			#if the second number is a number, it's probably input like ,dhroll (dice) (tn)
			if re.match("\d+",z[1]):
				# this is the target number , for stuff like 1d100 80 and such.
				TN=int(z.pop(1))
				# and the one before it is the dice roll
				total=Calc(z.pop(0))
			# if it ain't, then maybe it was assumed dice=1d100 and given as ,dhroll (tn)
			elif re.match("\d+",z[0]):
				#cause of format, tn will be first argument
				TN=int(z.pop(0))
				#default diceroll
				total=Calc("1d100")
			else :
				#fuck you , no dice and no tn what am I supposed to do.
				raise StandardError
			#if there's only one thing more, it's either the skill or additives. Functions that take additives as args
			# are supposed to ignore anything they don't recognize, not break on it so we're safe.
			if z[-1]=z[0]:
				additives=z[:]
			#otherwise we've got both
			elif z[-1]=z[2]:
				test=z[0]
				additives=z[1:]
			# sanity check the fucker, currently does nothing but does stop the code from running
			if insane("dh",test,additives):
				return "That's insane"+insane("dh",test,additives)
			#difference between rolled and TN
			Diff = ModDif(test,additives,TN- total)
			#degrees of sucess and failure
			DoSF = ModDoSF(test,additives,math.floor(Diff/10))
			#extra is where you add anything you want to add
			Extra=ModExtra(test,additives,DoSF)


				#change this, maybe add a formatter function and remember to have it somehow show what was actually rolled so you can make sure it didn't fuck up
				if Diff >= 0:
					return ("Test passed by "+str(DoSF)+" DoS"+extra,1)
				else:
					return ("Test failed by "+str(DoSF)+" DoF"+extra,1)
				
			else:
				return (total,1)
		except IndexError :
			return ("something's mising...,",2)
		except :
			return ("That dhroll was invalid",2)

	def do_saylater(self, rest):
		when, sep, msg = rest.partition(' ')
		when = int(when)
		d = defer.Deferred()
		# A small example of how to defer the reply from a command. callLater
		# will callback the Deferred with the reply after so many seconds.
		reactor.callLater(when, d.callback, msg)
		# Returning the Deferred here means that it'll be returned from
		# maybeDeferred in privmsg.
		return d

class MyFirstIRCFactory(protocol.ReconnectingClientFactory):
	protocol = BotProtocol
	channels = ['##MyFirstIrcBot,#darkf']

if __name__ == '__main__':
	# This runs the program in the foreground. We tell the reactor to connect
	# over TCP using a given factory, and once the reactor is started, it will
	# open that connection.
	reactor.connectTCP(HOST, PORT, MyFirstIRCFactory())
	# Since we're running in the foreground anyway, show what's happening by
	# logging to stdout.
	log.startLogging(sys.stdout)
	# And this starts the reactor running. This call blocks until everything is
	# done, because this runs the whole twisted mainloop.
	reactor.run()

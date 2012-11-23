#lesse now, how does one make an irc bot again?
#test
import sys
import operator
import re
import math
from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.application import internet, service
from random import randrange
#Constants
def dice(num, sides):
    return sum(randrange(sides)+1 for die in range(num))
optables={'+':operator.add,'-':operator.sub,'*':operator.mul,"/":operator.div,"":None}
opregex=re.compile('[+|-|*|/]')
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
		# Or, if there was no function, ignore the message.
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
	def _show_error(self, failure):
		return failure.getErrorMessage()
	def do_dance(self,whatevers):
		return ("dances",3)
	def do_ping(self, rest):
		return ('Pong.',0)
	def do_roll(self, rest):
		try:
			q=rest.partition("d")
			if opregex.search(q[2]):
				dicefaces, extraop, val=q[2].partition(opregex.search(q[2]).group())
				z=optables.get(extraop)(dice(int(q[0]),int(dicefaces)),int(val))
				return (z,1)
			else:
				return (dice(int(q[0]),int(q[2])),1)
		except:
			return ("That ain't a polite dice roll",2)
	def do_dhroll(self,rest):
		try:
			z=rest.split(" ")
			q=z[0].partition("d")
			# V catches a trailing +,-,*,/ and handles it.
			if opregex.search(q[2]):
				dicefaces, extraop, val=q[2].partition(opregex.search(q[2]).group())
				total=optables.get(extraop)(dice(int(q[0]),int(dicefaces)),int(val))
			else:
				total=dice(int(q[0]),int(q[2]))
			if re.match("\d+",z[1]):
				# this is where all the stuff you wanted to implement will go
				TN=int(z[1])
				Diff = TN- total
				DoSF = math.floor(Diff/10)
				try:
					if z[2]:
						pass

					
				except IndexError:
					if Diff >= 0:
						return ("Test passed by "+str(DoSF)+" DoS",1)
					else:
						return ("Test failed by "+str(DoSF)+" DoF",1)
				
			else:
				return (total,1)
		except:
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

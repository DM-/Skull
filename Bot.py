#lesse now, how does one make an irc bot again?
#test
import sys
import operator
import re
from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.application import internet, service
from random import randrange

def dice(num, sides):
    return sum(randrange(sides)+1 for die in range(num))
optables={'+':operator.add,'-':operator.sub,'*':operator.mul,"/":operator.div,"":None}
opregex=re.compile('[+|-|*|/]')
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
		#use V to set command symbol
		if not message.startswith(specialSymbol):
			return #we don't care for this
		command, sep, rest = message.lstrip(specialSymbol).partition(' ')
		#check beforehand if msg is channel or not
		ispriv=0
		if channel == self.nickname:
			ispriv = 1
		# Get the function corresponding to the command given.
		func = getattr(self, 'do_' + command, None)
		# Or, if there was no function, ignore the message.
		if func is None:
			try:
				func=getattr(self,'do_roll',None)
				d = defer.maybeDeferred(func, command)
				if ispriv:
					d.addCallback(self._send_message, nick)
				else:
					d.addCallback(self._send_message, channel, nick)
				return
			except:
				return
		# maybeDeferred will always return a Deferred. It calls func(rest), and
		# if that returned a Deferred, return that. Otherwise, return the return
		# value of the function wrapped in twisted.internet.defer.succeed. If
		# an exception was raised, wrap the traceback in
		# twisted.internet.defer.fail and return that.
		d = defer.maybeDeferred(func, rest)
		# Add callbacks to deal with whatever the command results are.
		# If the command gives error, the _show_error callback will turn the 
		# error into a terse message first:
		d.addErrback(self._show_error)
		# Whatever is returned is sent back as a reply:
		if ispriv:
			# When channel == self.nickname, the message was sent to the bot
			# directly and not to a channel. So we will answer directly too:
			d.addCallback(self._send_message, nick)
		else:
			# Otherwise, send the answer to the channel, and use the nick
			# as addressing in the message itself:
			d.addCallback(self._send_message, channel, nick)
	def _send_message(self, msg, target, nick=None):
		if nick:
					 msg = '%s, %s' % (nick, msg)
		self.msg(target, msg)

	def _show_error(self, failure):
		return failure.getErrorMessage()

	def do_ping(self, rest):
		return 'Pong.'
	def do_roll(self, rest):
		try:
			q=rest.partition("d")
			if opregex.search(q[2]):
				dicefaces, extraop, val=q[2].partition(opregex.search(q[2]).group())
				z=optables.get(extraop)(dice(int(q[0]),int(dicefaces)),int(val))
				return z
			return dice(int(q[0]),int(q[2]))
		except:
			return "That ain't a polite dice roll"
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

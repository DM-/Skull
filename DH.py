import re
WS = re.compile("WS|Weapon(s)?skill")
BS = re.compile("BS|Bal(l)?istic(s)?skill")
WSBS = re.compile("BS|Bal(l)?istic(s)?skill|WS|Weapon(s)?skill")
def dark(self,test,Diff):
	if WS.match(test):
		return -20
	elif BS.match(test):
		return -30
	else:
		return 0
def terrain10(self,test,Diff):
	if WSBS.match(test):
		return -10
	else:
		return 0
def terrain30(self,test,Diff):
	if WSBS.match(test):
		return -30
	else:
		return 0
def shootmelee(self,test,Diff):
	if BS.match(test):
		return -20
	else:
		return 0

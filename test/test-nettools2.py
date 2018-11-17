import sys, pickle

sys.path.append('../')

from nettools import MailBox


"""
Tesh sending random classes and strings over the mailboxes.
"""
class SentClass(object):
  def __init__(self):
    self.moo = "moo"
    self.cat = 1
    self.an = ['asdasd']
    self.next = None
    self.asda = {'assssssssssssssssssssss'}

m1 = MailBox()

m2 = MailBox()

m1_ad =  m1.getAddress()
m2_ad = m2.getAddress()

msg = ''

for i in range(1,100):
  msg = '.'*i
  m1.send(msg, m2_ad)
  data, addr = m2.receive()
  assert(data == msg)
print "Test passed"

#print msg
'''
Created on Feb 26, 2016

@author: shaibujnr
'''
import shelve
hs = shelve.open("highscore.txt")
print hs.has_key("highscore")
hs.close()
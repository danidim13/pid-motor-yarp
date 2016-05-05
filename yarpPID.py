#!/usr/bin/python

import yarp as y
import numpy as np
import time
from PID2 import PID

y.Network.init()

input_port0 = y.BufferedPortBottle()
input_port1 = y.BufferedPortBottle()
output_port = y.BufferedPortBottle()
input_port0.open("/pid/inr")
input_port1.open("/pid/inx")
output_port.open("/pid/out")

maxe = np.pi/4 
C = PID(0.01, 1.9, 0,maxe,-maxe)
setpoint = 2*np.pi*20
C.setInput(setpoint)
C.setRef(setpoint)
C.begin(setpoint)

epsilon_t = np.float_(0)
h_t = np.float_(0.001)

while True:
  t1 = time.clock()

  inputbottle = input_port0.read(False)  #false indica que no se queda esperando datos si no hay datos nuevos
  if inputbottle:
    C.setRef(inputbottle.get(0).asDouble())

  inputbottle = input_port1.read(False)
  if inputbottle:
    C.setInput(inputbottle.get(0).asDouble())
  
  	# A partir de aqui se hacen cosas con los inputs
    #outputnumber = inputbottle.get(0).asDouble() + inputbottle.get(1).asDouble()
    
  #else:
  epsilon_t = epsilon_t + time.clock() - t1
  if epsilon_t >= h_t :
    
    # Cosas para escribir en el output
    outputbottle = output_port.prepare()
    outputbottle.clear()
    outputbottle.addDouble(C.timestep(h_t))
    output_port.write()
    epsilon_t = epsilon_t - epsilon_t


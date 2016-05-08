#!/usr/bin/python

#Importacion de paquetes y clases

import yarp as y
from PMSM import PMSM
import numpy as np
import time
y.Network.init()

##### Declaracion de Puertos ####

## Puertos de Entrada

mtentrada = y.BufferedPortBottle()
mtsalida_theta = y.BufferedPortBottle()
mtsalida_omega = y.BufferedPortBottle()
mtsalida_alfa = y.BufferedPortBottle()
## Nombre de los puertos
mtentrada.open("/mt/in")
mtsalida_theta.open("/mt/out/theta")
mtsalida_omega.open("/mt/out/omega")
mtsalida_alfa.open("/mt/out/alfa")

#### Declarion motor ####
# (B,C,K,X_s,I_r,I_c)
motor = PMSM(2.0,3.392,0.001,1.02,0.624,0.2016)
omega_inicial = 2*np.pi*20
motor.begin(omega_inicial)
motor.setInput(0.0)

epsilon_t = np.float_(0)
h_t = np.float_(0.001)

while True:
  t1 = time.clock()

  inputbottle = mtentrada.read(False)  #false indica que no se queda esperando datos si no hay datos nuevos
  if inputbottle:
    motor.setInput(inputbottle.get(0).asDouble())
  
    # Se define la entrada del motor y el objeto de motor de iman permanente
  epsilon_t = epsilon_t + time.clock() - t1
    
  if epsilon_t >= h_t :
    alfa, omega, theta = motor.timestep(h_t)
    
   #### Aqui se escribe el output
    
    outputbottle_theta = mtsalida_theta.prepare()
    outputbottle_theta.clear()
    outputbottle_theta.addDouble(theta)
    mtsalida_theta.write()

    outputbottle_omega = mtsalida_omega.prepare()
    outputbottle_omega.clear()
    outputbottle_omega.addDouble(omega)
    mtsalida_omega.write()

    outputbottle_alfa = mtsalida_alfa.prepare()
    outputbottle_alfa.clear()
    outputbottle_alfa.addDouble(alfa)
    mtsalida_alfa.write()
    epsilon_t = epsilon_t - epsilon_t

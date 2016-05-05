#Clase motor sincrono de iman permanente (PMSM por sus siglas en ingles)

import numpy as np
import math
import time

class PMSM:
    def __init__(self,B,C,K,X_s,I_r,I_c):
        
        self.B = np.float(B) #constante proporcional entre V-Delta
        self.C = np.float(C) #constante proporcional entre E_a-omega
        self.K = np.float(K) #constante proporcional entre T_f-omega
        self.X_s = np.float(X_s) # Reactancia Sincrona
        self.I_r = np.float(I_r) # Momento de Inercia del Rotor
        self.I_c = np.float(I_c) # Momento de Inercia de la Carga
        self.theta = np.float_(0) # Posicion angular del rotor
	self.past_theta_p = np.float_(0) # valor anterior de la derivada de theta
        self.omega = np.float_(0) # Velocidad angular del rotor
	self.past_omega_p = np.float_(0) # valor anterior de la derivada de omega
        #self.alfa = np.float_(0) # Aceleracion angular del rotor
        self.delta = np.float_(0) # Angulo entre la corriente y tension
        self.epsilon = np.float_(0.01) #Tension inducida  minima
        self.tau_ind = np.float_(0) # Torque inducido en el rotor
        self.tau_friccion = np.float_(0) #Torque producido por la friccion
        self.tau_total = np.float_(0) # Torque total
        self.E_a = np.float_(12)#self.epsilon # Tension inducida
        
        #
        self.N_vueltas = np.int_(0)

    def begin(self,omega_inicial): #Se define el tiempo pasado
        self.omega = omega_inicial
        
    def setInput(self, delta):
    	self.delta = delta

    def timestep(self, delta_t):
        
       #d_omega = self.alfa*entrada
       
       #Calculo de tension inducida y torques
       
       #self.E_a  = 12 #self. epsilon + self.B*self.delta #Se calcula la tension inducida
       self.tau_ind = 3*self.E_a*self.C*self.omega*math.sin(self.delta)/(self.X_s*self.omega) #Se 
       self.tau_friccion = self.K*self.omega
       self.tau_total = self.tau_ind - self.tau_friccion

       # Calcular alfa(t), omega(t) y theta(t)
       self.omega_p = self.tau_total/(self.I_r + self.I_c)
       self.theta_p = self.omega
       
       self.omega = (self.past_omega_p + self.omega_p)*delta_t/2 + self.omega
       self.theta = (self.past_theta_p + self.theta_p)*delta_t/2 + self.theta
       
       if(self.theta > np.pi*2):
			extras = np.int_(self.theta/(np.pi*2))
			self.N_vueltas = self.N_vueltas + extras
			self.theta = np.fmod(self.theta, np.pi*2)
			print self.N_vueltas

       # Se actualizan los valores anteriores
       self.past_omega_p = self.omega_p
       self.past_theta_p = self.theta_p

        
       return self.omega_p, self.omega, self.theta

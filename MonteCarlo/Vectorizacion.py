#!/usr/bin/env python
# coding: utf-8

# # Práctica 1 Vectorización

# ## Calculo de integrales mediante el metodo de Monte Carlo
# Importamos las librerias que nos harán falta:
# + matplotlib para hacer gráficas <br>
# + numpy para generar números aleatorios y operaciones con arrays <br>
# + time para calcular el tiempo de cómputo <br>
# + scipy para comprobar el area de una función <br>
# 
# Para calcular el area de una funcion compleja de integrar usaremos este metodo que se basa en la probabilidad para aproximar el calculo de una integral <br>
# Se usan dos metodos diferentes para calcular el numero de puntos que caen debajo de la funcion
# + Bucle, calculando 1 a 1 todos los puntos que estan debajo
# + Vectores, calculando la longitud del vecto de los elementos por debajo de la funcion <br>

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import integrate


# In[2]:


#return -(x)**2+100 #puede ser cualquier funcion ej:ln(x)+3x+x^2

f = lambda x : x**2

def plot_func(fun,a,b):
    """plots the function fun from point a to b"""
    plt.figure()
    x = np.linspace(a,b,50)
    y = fun(x)
    plt.plot(x,y)


# ## Funciones usadas para el calculo de puntos debajo de la funcion
# La funcion loop itera sobre los n puntos y comprueba si estan por debajo de la funcion <br>
# La funcion vector simplemente devuelve la longitud de el array el cual contiene los puntos que estan por debajo <br>
# Para 1 millon de puntos el tiempo de calculo es de unas <b>10 veces mayor</b> en la funcion del bucle
#     
# + Vector
# 
#     Media de tiempo con 1 millon de puntos es de 93ms
#     
# + Loop
# 
#     Media de tiempo con 1 millon de puntos es de 953ms

# In[3]:


def vector(fun,a,b,num_puntos,x_rand,y_rand): #vector method
    return np.count_nonzero(y_rand < fun(x_rand)) 
    
def loop(fun,a,b,num_puntos,x_rand,y_rand): #loop method
    y_fun = fun(x_rand)
    debajo = 0
    for i in range(num_puntos):
        if y_rand[i] < y_fun[i]:
            debajo += 1
    return debajo


# In[4]:


def integra_mc(fun, a, b, num_puntos=10000, print_out=True, method=vector):
    VAL = 10000
    x = np.linspace(a,b,VAL)
    y = np.array(fun(x))
    tic = time.process_time()
    x_rand = np.random.uniform(a,b,num_puntos)
    y_rand = np.random.uniform(min(y),max(y),num_puntos)
    debajo = method(fun,a,b,num_puntos,x_rand,y_rand)
    toc = time.process_time()
    if print_out:
        print("Tiempo: {}".format(1000*(toc-tic)))
        print("Nº Debajo: {}".format(debajo))
        print("Nº Total: {}".format(num_puntos))
        print("(b-a)M = {}".format((b-a)*max(y)))
        print("Area Vector: {}".format((debajo/num_puntos)*(b-a)*max(y)))
        plt.scatter(x_rand,y_rand,c='red',marker='x', alpha=0.5)
    return (debajo/num_puntos)*(b-a)*max(y)


# ## Prueba del metodo montecarlo 
# Imprimiendo todos los valores obtenidos <br>
# Grafica de puntos aleatorios y de la funcion

# In[5]:


func = f
a = 0
b = 10
puntos = 500

plot_func(func,a,b)
mc_area = integra_mc(func,a,b,num_puntos=puntos)
plt.show()
print("\nArea de scipy: {}".format(integrate.quad(func,a,b)[0]))
print("Error: {}".format(abs(mc_area - integrate.quad(func,a,b)[0])))


# In[6]:


def integra_mc_time(fun, a, b, num_puntos=100000, method=vector):
    """Devuelve una tupla de (area,tiempo)"""
    VAL = 1000
    x = np.linspace(a,b,VAL)
    y = np.array(fun(x))
    tic = time.process_time()
    x_rand = np.random.uniform(a,b,num_puntos)
    y_rand = np.random.uniform(min(y),max(y),num_puntos)
    debajo = method(fun,a,b,num_puntos,x_rand,y_rand)
    toc = time.process_time()
    return (((debajo/num_puntos)*(b-a)*max(y)),1000*(toc-tic))

def compara_tiempos(fun,a,b,puntos_min=100,puntos_max=1000000):
    sizes = np.linspace(puntos_min,puntos_max,20) #100000000
    vector_time = []
    vector_area = []
    loop_time = []
    for size in sizes:
        #Devuelven una tupla de (area,tiempo)
        v = integra_mc_time(fun,a,b,int(size),method=vector)
        vector_time.append(v[1])
        vector_area.append(v[0])
        loop_time.append(integra_mc_time(fun,a,b,int(size),method=loop)[1])
    actual_area = integrate.quad(fun,a,b)[0]
    return (sizes, loop_time, vector_time, vector_area, actual_area)

#result -> sizes, loop_time, vector_time, vector_area, actual_area
#result -> 0,     1,         2,           3,           4

def plot_dif_time(result):
    plt.figure()
    plt.scatter(result[0],result[1], c='red')
    plt.plot(result[0],result[1], c='red', label='bucle')
    plt.scatter(result[0], result[2], c='blue')
    plt.plot(result[0], result[2], c='blue', label='vector')
    plt.legend()
    plt.show()
def plot_vector_time(result):
    plt.figure()
    plt.scatter(result[0], result[2], c='blue', label='vector')
    plt.plot(result[0], result[2], c='blue', label='vector')
    plt.show()    

def plot_areas(result):
    plt.figure()
    #quitamos el primero para que no desvie demasiado el eje del error
    plt.scatter(result[0][1:],result[3][1:], c='blue', label='results vector') 
    plt.plot([min(result[0]),max(result[0])],[result[4],result[4]], c='green', label='actual')
    plt.legend()
    plt.show()


# ## Grafica de tiempos

# In[7]:


result = compara_tiempos(f,a,b,puntos_min=100,puntos_max=10000000)


# Se puede observar que ambas graficas crecen de forma lineal, pero sin embargo la del vector (azul) lo hace con menor pendiente

# In[8]:


plot_dif_time(result)


# En esta grafica vemos mas detalladamente como el tiempo del vector aumenta cuantos mas puntos añadamos <br>
# Pero vemos que tienen una diferencia menor entre min y max comparada con la del bucle

# In[9]:


plot_vector_time(result)


# Como podemos ver aqui, el error, al aumentar el numero de puntos disminuye

# In[10]:


plot_areas(result)

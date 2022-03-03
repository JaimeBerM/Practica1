from multiprocessing import Process, BoundedSemaphore
from random import randint
from multiprocessing import Manager

K = 9 #longitud de las sucesiones 
N = 3  #numero de sucesiones

def sucesion_creciente(): #crea una sucesion de numeros crecientes
    suc = [0 for i in range(K)]
    suc[0] = randint(0,7)
    suc[K-1] = -1
    for i in range(K-2):
        suc[i+1] = suc[i] + randint(1,5)
    return suc

def procesar_minimo(suc): #devuelve el minimo de una lista y su posicion (obviando el -1 final)
    m = max(suc)
    pos = suc.index(m)
    if m > -1:
        for i in range(N):
            if suc[i] >= 0 and suc[i] < m:
                m = suc[i]
                pos = i
    return (m,pos)
    
def producer(semaforo_e,semaforo_n,buffer,sucesion,ide): #dos semaforos
    for i in range(K):
        semaforo_e.acquire()
        buffer[ide] = sucesion[i]
        semaforo_n.release()

def consumer(semaforos_e,semaforos_ne,buffer,result):  #dos listas de semaforos
    acabado = False
    while  not acabado:
        for j in range(N):
            semaforos_ne[j].acquire()
        (a,pos) = procesar_minimo(buffer)
        if a == -1: # hemos acabado
            acabado=True
        else: #se acaba 
            result.append(a)
        for i in range(N):
            if i == pos:
                semaforos_e[i].release()
            else:
                semaforos_ne[i].release()
        
def main():
    manager = Manager()
    buffer = manager.list() #buffer, variable compartida por todos los procesos
    lp = []                 #lista de procesos
    semaforos_e = [BoundedSemaphore(1) for i in range(N)]
    semaforos_ne = [BoundedSemaphore(1) for i in range(N)]
    result = manager.list()
    lp.append(Process(target=consumer,args=(semaforos_e,semaforos_ne,buffer,result)))  #agregamos el consumidor
    for i in range(N):              #agregamos los productores
        buffer.append(-3)
        semaforos_ne[i].acquire()
       	sucesion = sucesion_creciente()
        lp.append(Process(target=producer,args=(semaforos_e[i],semaforos_ne[i],buffer,sucesion,i)))
        print('Sucesion ' ,i+1,":",sucesion)
    for p in lp:    #iniciamos los procesos
        p.start()
    for p in lp:
        p.join()
    print('Sucesion ordenada: ',result)

if __name__ == '__main__':
    main()

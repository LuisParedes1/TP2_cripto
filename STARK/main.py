# El objetivo consiste en probar la validez de un programa que calcula 2^{8^20} módulo
# p, utilizando diferentes estrategias y viendo el perfil de costos (tanto en términos de
# longitud de la prueba como de tiempo de generación). 

# 1. Considerar a_0 = 2 y a_{n+1}=a_n^8.
# 2. Considerar a_0 = 2 y a_{n+1}=a_n^2
# 3. Considerar a_0 = 2 y a_{2n+1}=a_{2n}^2 y a_{2n}=a_{2n-1}^4.
# 4. Usando 2 columnas.

# Tener en cuenta que, dado el grado de las restricciones, se requiere usar un factor de
# expansión (blowup) por lo menos tan grande como el grado de las restricciones.

import channel, field, list_utils, merkle, polynomial

import time
from field import FieldElement # Cuerpo Finito
from polynomial import X # Polinomios
from polynomial import interpolate_poly # Interpolacion de Lagrange
from merkle import MerkleTree # Merkle Tree
from channel import Channel # Implements Fiat-Shamir Heuristic

#####
from CP import CP_eval, get_CP # Returns a list of images from the CP
from FRI import FriCommit # Next domain for the FRI operator
from decommitment import decommit_fri # proof algorithm

# 1. Considerar a_0 = 2 y a_{n+1}=a_n^8.
def modelo():
    
    # Pasos

    # 1) Genero mi execution trace
    a = [FieldElement(1), FieldElement(3141592)]
    while len(a) < 1023:
        a.append(a[-2] * a[-2] + a[-1] * a[-1]) # Cambiar con el modelo actual
    
    pass


def fibSq():

    # Quiero probar que a[1022] = 2338775057, siendo 
    # * a_0 = 1
    # * a_1 = X (cualquiera)
    # * a[n+2] = a[n+1]^2 + a[n]^2


    # Trabajamos en el espacio finito F_3221225473  (archivo field.py)

    # 1. Generate the trace

    start = time.time()
    start_all = start
    print("Generating the trace")

    # FibonacciSq Trace
    a = [FieldElement(1), FieldElement(3141592)]

    # a[n+2] = a[n+1]^2 + a[n]^2
    while len(a) < 1023:
        a.append(a[-2] * a[-2] + a[-1] * a[-1])   


    # 2. Busco un espacio finitamente generado   

    # Busco elemento generador g tal que el subgrupo sea de orden |Fx| = n
    # G = {g,g^1, g^2, ... , g^n}, G[i] = g^i

    # Hint: When 𝑘 divides |𝔽×|, 𝑔𝑘 generates a group of size |𝔽×| / 𝑘, 
    # and the n-th power of some FieldElement 𝑥 can be computed by calling x ** n.

    ## En este caso, |𝔽×| = 3221225473, k = 3*2**20 = 3145728
    ## Por ende, |𝔽×| / 𝑘 = 1024.
    ## Nuestro grupo es de orden 1024
    g = FieldElement.generator() ** (3 * 2 ** 20)  ## g^k
    G = [g ** i for i in range(1024)]


    # Siendo n el orden  n*k = |𝔽×| , busco k tal que |𝔽×| = 3221225473


    # 3. Busco un polinomio asociado a la traza y hago interpolacion
    # y extiendo la traza
    
    # Ahora con el polinomio asociado, cada elemento de la traza 
    # lo veo como una evaluacion hecha del polinomio f sobre
    # elementos g (del espacio generador)

    # Esto se llama Reed-Solomon error correction code

    ## Evaluamos en un dominio mucho mas grande que G. Tomamos
    ## un dominio H que es 8 veces mas grande

    ## n = 8*1024
    ## |𝔽×| = 3221225473
    ## k = 393216

    print("We blow up the trace (Extend the trace) 8 times bigger")
    
    w = FieldElement.generator()
    h = w ** ((2 ** 30 * 3) // 8192)  # (este es mi generador g^k)
    H = [h ** i for i in range(8192)]
    eval_domain = [w * x for x in H]


    ## 4 Busco un polinomio asociado y hago interpolacion

    f = interpolate_poly(G[:-1], a)  ## Este polinomio pasa por todos los 
                                    ## puntos que nos interes

    # Busco un polinomio asociado a la traza 
    # f = interpolate_poly(G[:-1], a)

    # x[i] = G[i] (espacio finitamente generado)
    # y[i] = a[i] (FibonacciSq)
                                     
    f_eval = [f(d) for d in eval_domain] ## Busco la imagen en todos los 
                                        ## elementos del dominio extendido


    # f_eval va a tener los elementos originales de la traza y los adicionales

    # 5. Commitment 
    # 
    # Con la traza extendida, ahora creo las hojas del merkle tree
    # a partir de estos 

    f_merkle = MerkleTree(f_eval)  


    # 6. Channels
    #
    # Theoretically, a STARK proof system is a protocol for interaction
    # between two parties - a prover and a verifier.
    #
    # In practice, we convert this interactive protocol into a 
    # non-interactive proof using the Fiat-Shamir Heuristic

    channel = Channel()     # El channel nos dara datos que deberia darnos el verifier
    channel.send(f_merkle.root)


    # Notebook 2
    print(f'{time.time() - start}s')
    start = time.time()
    print("Generating the composition polynomial and the FRI layers...")

    # Constraints
    # Convierto todas las restricciones originales a rational functions

    ## a0 = 1
    numer0 = f - 1
    denom0 = X - 1
    p0 = numer0 / denom0

    ## a_1022 = 2338775057
    numer1 = f - 2338775057
    denom1 = X - g**1022
    p1 = numer1 / denom1
    
    ## a[n+2] = a[n+1]^2 + a[n]^2
    numer2 = f(g**2 * X) - f(g * X)**2 - f**2
    denom2 = (X**1024 - 1) / ((X - g**1021) * (X - g**1022) * (X - g**1023))
    p2 = numer2 / denom2

    # Composition Polynomial
    cp = get_CP(channel,p0,p1,p2)
    cp_eval = CP_eval(cp,eval_domain)
    cp_merkle = MerkleTree(cp_eval)
    channel.send(cp_merkle.root)
    
    # Notebook 3
    
    # FRI Folding Operator
    fri_polys, fri_domains, fri_layers, fri_merkles = FriCommit(cp, eval_domain, cp_eval, cp_merkle, channel)

    # Notebook 4
    print(f'{time.time() - start}s')
    start = time.time()
    print("Generating queries and decommitments...")
    
    decommit_fri(channel, fri_layers, fri_merkles, f_eval, f_merkle)

    print(channel.proof)
    print(f'Overall time: {time.time() - start_all}s')
    print(f'Uncompressed proof length in characters: {len(str(channel.proof))}')
    

## |G°| = 20 y G = {g^0,g^1, g^2,...g^20} con g = 5, g=5
## p = 3221225472
#  G = {g^i | 0 <= i < |G°|}
if __name__ == "__main__":

    ### Ejemplo FibonacciSQ
    fibSq()

    # print("Para el siguiente modelo se tomara el espacio de cuerpo finito de grado 20 y primo 3221225472")
    # print("Tomaremos como generador g = 5")

    # modelo1()
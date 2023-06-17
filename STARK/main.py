# El objetivo consiste en probar la validez de un programa que calcula 2^{8^20} módulo
# p, utilizando diferentes estrategias y viendo el perfil de costos (tanto en términos de
# longitud de la prueba como de tiempo de generación). 

# 1. Considerar a_0 = 2 y a_{n+1}=a_n^8.
# 2. Considerar a_0 = 2 y a_{n+1}=a_n^2
# 3. Considerar a_0 = 2 y a_{2n+1}=a_{2n}^2 y a_{2n}=a_{2n-1}^4.
# 4. Usando 2 columnas.

# Tener en cuenta que, dado el grado de las restricciones, se requiere usar un factor de
# expansión (blowup) por lo menos tan grande como el grado de las restricciones.

from field import FieldElement

import channel, field, list_utils, merkle, polynomial

# 1. Considerar a_0 = 2 y a_{n+1}=a_n^8.
def modelo1():
    
    # Pasos

    # 1) Genero mi execution trace
    a = [FieldElement(1), FieldElement(3141592)]
    while len(a) < 1023:
        a.append(a[-2] * a[-2] + a[-1] * a[-1]) # Cambiar con el modelo actual
    
    pass


def modelo2():
    pass


    


## |G°| = 20 y G = {g^0,g^1, g^2,...g^20} con g = 5, g=5
## p = 3221225472
#  G = {g^i | 0 <= i < |G°|}
if __name__ == "__main__":

    print("Para el siguiente modelo se tomara el espacio de cuerpo finito de grado 20 y primo 3221225472")
    print("Tomaremos como generador g = 5")

    modelo1()
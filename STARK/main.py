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

def main():
    print("Hello World!")

    



if __name__ == "__main__":
    main()
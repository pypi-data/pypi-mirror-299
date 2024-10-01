def funcion():
    """
    def f(x):
        return (x**3) - (60*(x**2)) + (900*x) + 100
    """
    return None

def simulated():
    """
    def simulated_anneling(estado, nums, temperatura_inicial, factor_friccion):
        current_state = list(map(int, estado))
        score = f(int(estado, 2))

        #guardamos el mejor numero
        mejor_num = current_state
        mejor_score = score
        temperatura = temperatura_inicial

        scores = []

        #Bucle que valida que tengamos una "alta temperatura"
        while temperatura > 1:
            nuevo_estado = current_state.copy()
            i = random.randint(0, len(estado) - 1)
            nuevo_estado[i] = str(1 - int(nuevo_estado[i]))
            nuevo_estado = ''.join(map(str, nuevo_estado))

            nuevo_num = int(nuevo_estado, 2)
            nuevo_score = f(nuevo_num)
            nuevo_estado = list(map(int, nuevo_estado))

            #calculamos la diferencia
            diferencia = mejor_score - nuevo_score

            if diferencia < 0 or random.random() < math.exp(-diferencia / temperatura): #aqui se evalua primero si la diferencia es menor que 0 y se le aplica la formula de la temp
            current_state = nuevo_estado

            if nuevo_score > mejor_score:
                mejor_num = nuevo_estado
                mejor_score = nuevo_score

            temperatura*=factor_friccion
            scores.append(mejor_score)

            #mostrar os resultados relevantes
            print (f"resultado de la iteracion: ")
            print ("----------------------------")
            print(f"ruta actual: {current_state}")

            print(f"mejor ruta: {mejor_num}")
            print(f"mejor distancia: {mejor_score}")

            print(f"Variacion de Distancia: {diferencia}")
            print(f"temperatura: {temperatura}")


        return mejor_num, mejor_score, scores

    temp_ini = 1000
    factor_friccion = 1 - 0.045
    mejor_num, mejor_dist, distancias = simulated_anneling("10011", nums, temp_ini, factor_friccion)

    print(f"mejor ruta: {mejor_num}")
    print(f"mejor distancia: {mejor_dist}")
    """
    return None


def recorrer_hacer_paises():
    """
    def distancia_euclidianda(p1,p2):
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    distancia_matrix=pd.DataFrame(index=paises.keys(),columns=paises.keys())

    for pais1 in paises:
    for pais2 in paises:
        if pais1==pais2:# evitamos la distancia entre el mismo pais , ejemplo eliminamos los interceptos entre el mismo pais
        distancia_matrix.loc[pais1,pais2]=0
        else:
        distancia_matrix.loc[pais1,pais2]=distancia_euclidianda(paises[pais1],paises[pais2]) #llenamos la matriz euclidiana con los paises
    distancia_matrix= distancia_matrix.astype(float)
    print(distancia_matrix)
    sns.heatmap(distancia_matrix, annot=True, cmap='viridis')
    plt.show()
    """
    return None

def recorrer_paises():
    """
    def total_distancia(ruta,piases): #calcula el esfuerzo que se hace al hacer el recorrido de una ruta
        distancia=0
        for i in range(len(ruta)):
            p1= paises[ruta[i]]
            p2= paises[ruta[(i+1)%len(ruta)]]
            distancia+=distancia_euclidianda(p1,p2)
        return distancia
    
    def simulated_anneling(paises,temperatura_inicial,factor_friccion):
        ruta_actual=list(paises.keys())
        random.shuffle(ruta_actual)#creamos una ruta aleatoria a partir de una ya exsistente
        distancia_actual=total_distancia(ruta_actual,paises)

        #guardamos la mejor ruta
        mejor_ruta=ruta_actual
        mejor_distancia=distancia_actual
        temperatura=temperatura_inicial
        #para guardar las distancias resultadntes
        distancias=[]
        #Bucle que valida que tengamos una "alta temperatura"
        while temperatura>1:
            #creamos una nueva ruta cambiando las dos ciudades
            nueva_ruta=ruta_actual.copy()
            i,j=random.sample(range(len(nueva_ruta)),2)#cambiamos 2 valores random de la ruta
            nueva_ruta[i],nueva_ruta[j]=nueva_ruta[j],nueva_ruta[i] #cambiamos el 4 por el 6 por ejemplo
            #calculamos la distancia de esta nueva ruta
            nueva_distancia =total_distancia(nueva_ruta,paises)
            #calculamos la diferencia
            diferencia=nueva_distancia-distancia_actual
            #si la nueva ruta es mejor que la actual
            if diferencia<0 or random.random()<math.exp(-diferencia/temperatura):#aqui se evalua primero si la diferencia es menor que 0 y se le aplica la formula de la temp
            ruta_actual=nueva_ruta
            distancia_actual=nueva_distancia
            if nueva_distancia<mejor_distancia:
                mejor_ruta=nueva_ruta
                mejor_distancia=nueva_distancia
            #guardamos las distancias
            distancias.append(distancia_actual)
            #mostrar os resultados relevantes
            print (f"resultado de la iteracion: ")
            print ("----------------------------")
            print(f"ruta actual: {ruta_actual}")
            print(f"distancia actual: {distancia_actual}")

            print(f"mejor ruta: {mejor_ruta}")
            print(f"mejor distancia: {mejor_distancia}")

            print(f"Variacion de Distancia: {diferencia}")
            print(f"temperatura: {temperatura}")


            #actualizar el valor de la temperatura con el factor que viene por parametro
            temperatura*=factor_friccion
        return mejor_ruta,mejor_distancia,distancias
    """
    return None

def plot_mejor_ruta(ruta,paises):
  """
  x=[paises[ciudad][0] for ciudad in ruta]+[paises[ruta[0]][0]]
  y=[paises[ciudad][1] for ciudad in ruta]+[paises[ruta[0]][1]]
  plt.plot(x,y,'ro-', label="buenas", color="blue")
  for i, ciudad in enumerate(ruta):
    plt.annotate(ciudad, (paises[ciudad][0],paises[ciudad][1]))
  plt.legend()
  plt.show()
  """
  return None
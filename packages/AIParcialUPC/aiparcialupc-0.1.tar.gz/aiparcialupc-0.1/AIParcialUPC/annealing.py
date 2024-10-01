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

class objeto:
  def __init__(self, valor, peso):
    self.valor = valor
    self.peso = peso
    self.valor_por_peso = valor/peso


def ramificacion_poda(objetos, capacidad):
  """
  #ordenar los objetos descendente
  objetos = sorted(objetos, key=lambda x: x.valor_por_peso, reverse=True)

  mejor_valor = 0
  mejor_solucion = []

  #recursividad para analizar los "hijos"
  def explorar_nodo(nivel, valor_actual, peso_actual, solucion_actual):
    nonlocal mejor_valor, mejor_solucion

    #verificamos si hemos perocesado todo el arbol
    if nivel == len(objetos):
      if valor_actual > mejor_valor:
        mejor_valor = valor_actual
        mejor_solucion = solucion_actual[:]
      return

    #calcular el beneficio superior
    cota_superior = valor_actual
    peso_restante = capacidad - peso_actual
    for i in range(nivel, len(objetos)):
      if peso_restante > objetos[i].peso:
        cota_superior += objetos[i].valor
        peso_restante -= objetos[i].peso
      else:
        break


    #podar siempre y cuando la cota superior sea menor o igual que el nuevo valor encontrado
    if cota_superior <= mejor_valor:
      return

    #realizamos recursividad retirando, reduciendo el nivel
    explorar_nodo(nivel + 1, valor_actual, peso_actual, solucion_actual)

    #si el objeto actual no excede la capacidad
    if peso_actual + objetos[nivel].peso <= capacidad:
      solucion_actual.append(objetos[nivel])
      explorar_nodo(nivel + 1, valor_actual + objetos[nivel].valor, peso_actual + objetos[nivel].peso, solucion_actual)
      solucion_actual.pop() #deshace la ultima insersion


  #inica la exploracion desde 0
  explorar_nodo(0,0,0,[])

  return mejor_valor, mejor_solucion
  """
  return None

def uso():
  """
    objetos = [objeto(10,2), objeto(10,4), objeto(12,6), objeto(18,9)]
    capacidad_mochila = 14

    mejor_valor, mejor_solucion = ramificacion_poda(objetos, capacidad_mochila)
  """
  return None
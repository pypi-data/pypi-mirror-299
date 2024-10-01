def funcion_activasion(z):
  """
  return 1 if z>=0 else 0
  """
  return None

#funcion para entrenar al perceptron
def entrenar_perceptron(X,y,w,theta, learning_rate, epochs=1):
  """
  x=np.array([ [0,0],[1,0],[0,1],[1,1]])
  y=np.array([0,1,1,1])

  # se debe de definir hiperparametros
  w=np.array([0.0, 2.0])
  learning_rate=1.0
  theta=-0.5

  for epoch in range(epochs):
    print(f"\n Epoca:{epoch}")
    for i in range(len(X)):
      z=np.dot(X[i],w)+theta #valor+peso
      y_prediction=funcion_activasion(z)

      print(f"\n Entrada {X[i]}")
      print(f"\n Salida {y[i]}")
      print(f"\n Salida predicha {y_prediction}")
      print(f"\n VAlor Z: {z}")
      if y_prediction != y[i]:
        error=y[i]-y_prediction #tenemos que definir el error y guardarlo
        #peso
        w+=learning_rate*error*X[i]# como nos hemos equivocado nuestro peso debe cambiar en funcion a nuestro ratio ed aprendiazaje
        #umbreal
        theta+=learning_rate*error
        print(f"\n peso actualizado: {w}")
        print(f"\n umbral theta actualizado: {theta}")
      else:
        print("No hay error")

  return w,theta
  """
  return None
def calcular_ingresos_totales(aumento):
    """
    precio = 21
    p = Producto(producto_id=0, demanda=60, precio=precio, costo=17, elasticidad=.3, precio_competencia=23.2).update_price(precio + aumento)
    return p.ingreso_total(), p.precio
    """
    return None

def hill_climbing(n_iter=1000, paso=1):
    """
    mejor_ingreso, mejor_precio = calcular_ingresos_totales(0)

    print("inicial: ", mejor_precio, mejor_ingreso)

    for _ in range(n_iter):
        variaciones = np.random.normal(-paso, paso, size=10000)
        opciones = np.array([calcular_ingresos_totales(variacion) for variacion in variaciones])
        ingresos, precios = opciones[:, 0], opciones[:, 1]

        indice_max = np.argmax(ingresos)
        ingreso = ingresos[indice_max]

        if ingreso > mejor_ingreso:
            mejor_precio = precios[indice_max]
            mejor_ingreso = ingreso
        else: break


    return mejor_precio, mejor_ingreso
    """
    return None

def uso():
    """
    precio_prediccion, ingreso_prediccion = hill_climbing(1000, paso=1)
    print(precio_prediccion, ingreso_prediccion)
    data = np.array([[p.precio, p.ingreso_total()] for p in productos])
    plt.scatter(data[:, 0], data[:, 1])
    plt.scatter(precio_prediccion, ingreso_prediccion, color='red', label='Predicción')

    plt.xlabel('Precio')
    plt.ylabel('Ingreso Total')
    plt.title('Relación Precio - Ingreso Total')
    plt.show()
    """
    return None
# Sistema experto para análisis financiero personal

def evaluar_ahorro(porcentaje_ahorro, umbral_saludable):
    if porcentaje_ahorro >= umbral_saludable:
        return "saludable"
    elif porcentaje_ahorro >= umbral_saludable / 2:
        return "aceptable"
    else:
        return "bajo"

def evaluar_deuda(porcentaje_deuda, umbral_alerta, umbral_peligro):
    if porcentaje_deuda <= umbral_alerta:
        return "adecuado"
    elif porcentaje_deuda <= umbral_peligro:
        return "moderado"
    else:
        return "alto"

def evaluar_patrimonio(patrimonio_neto):
    if patrimonio_neto > 0:
        return "favorable"
    else:
        return "negativo"

def recomendaciones_inversion(saldo_libre, nivel_deuda, ahorro, saldo_libre_alto):
    if saldo_libre <= 0:
        return ["No hay capacidad de inversión"]

    if nivel_deuda == "adecuado":
        return [
            "Invertir según perfil de riesgo:",
            " - Conservador: Depósitos a plazo",
            " - Moderado: Fondos balanceados",
            " - Agresivo: Acciones/ETF"
        ]
    elif nivel_deuda == "moderado":
        return ["Invertir 50% del saldo libre, destinar 50% a reducir deuda"]

    if ahorro == "saludable" and saldo_libre_alto:
        return [
            "Diversificación recomendada:",
            " - Corto plazo: liquidez",
            " - Mediano plazo: inversiones moderadas",
            " - Largo plazo: planes de pensión"
        ]

    return []

def recomendaciones_deuda(nivel_deuda, ahorro):
    acciones = []
    if nivel_deuda == "alto":
        acciones.append("Estrategia anti-deuda:")
        acciones.append(" 1. Congelar nuevas deudas")
        acciones.append(" 2. Método bola de nieve o avalancha")
        acciones.append(" 3. Buscar asesoría crediticia")
        if ahorro == "bajo":
            acciones.insert(0, "Plan de emergencia:")
            acciones.insert(1, " 1. Reducir gastos no esenciales")
            acciones.insert(2, " 2. Reestructurar deudas")
            acciones.insert(3, " 3. Ahorro automático mínimo")
    return acciones

# Ejemplo de uso
if __name__ == "__main__":
    ingreso_mensual = float(input("Ingrese su ingreso mensual: "))
    gastos_fijos = float(input("Ingrese el total de sus gastos fijos: "))
    gastos_variables = float(input("Ingrese el total de sus gastos variables: "))
    deuda_mensual = float(input("Ingrese el pago mensual de sus deudas: "))
    patrimonio_neto = float(input("Ingrese su patrimonio neto: "))

    ahorro_mensual = ingreso_mensual - (gastos_fijos + gastos_variables + deuda_mensual)
    porcentaje_ahorro = ahorro_mensual / ingreso_mensual
    porcentaje_deuda = deuda_mensual / ingreso_mensual
    saldo_libre = ahorro_mensual

    umbral_ahorro_saludable = 0.15
    umbral_deuda_alerta = 0.20
    umbral_deuda_peligro = 0.35

    ahorro = evaluar_ahorro(porcentaje_ahorro, umbral_ahorro_saludable)
    deuda = evaluar_deuda(porcentaje_deuda, umbral_deuda_alerta, umbral_deuda_peligro)
    patrimonio = evaluar_patrimonio(patrimonio_neto)
    saldo_libre_alto = saldo_libre > 1000

    print("\nEvaluación del ahorro:", ahorro)
    print("Evaluación del endeudamiento:", deuda)
    print("Evaluación patrimonial:", patrimonio)

    print("\nRecomendaciones de inversión:")
    for r in recomendaciones_inversion(saldo_libre, deuda, ahorro, saldo_libre_alto):
        print(r)

    recomendaciones_deuda_lista = recomendaciones_deuda(deuda, ahorro)
    if recomendaciones_deuda_lista:
        print("\nRecomendaciones sobre deuda:")
        for r in recomendaciones_deuda_lista:
            print(r)

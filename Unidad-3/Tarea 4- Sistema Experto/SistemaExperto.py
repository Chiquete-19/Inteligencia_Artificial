import tkinter as tk
from tkinter import ttk, messagebox
import json
import statistics
import os
from datetime import datetime

class SistemaFinanciero:
    def __init__(self):
        # Umbrales iniciales
        self.umbral_ahorro_saludable = 0.15
        self.umbral_deuda_alerta = 0.20
        self.umbral_deuda_peligro = 0.35
        self.historico_file = "historico_financiero.json"
        
        # Cargar histórico o crear si no existe
        if not os.path.exists(self.historico_file):
            with open(self.historico_file, 'w') as f:
                json.dump({"usuarios": []}, f)
    
    def cargar_historico(self):
        with open(self.historico_file, 'r') as f:
            return json.load(f)
    
    def guardar_en_historico(self, datos):
        historico = self.cargar_historico()
        datos['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historico['usuarios'].append(datos)
        
        
        if len(historico['usuarios']) > 10:
            ahorros = [u['porcentaje_ahorro'] for u in historico['usuarios'] if 'porcentaje_ahorro' in u]
            if ahorros:
                self.umbral_ahorro_saludable = max(0.1, statistics.mean(ahorros) * 0.9)
        
        with open(self.historico_file, 'w') as f:
            json.dump(historico, f, indent=2)
    
    def evaluar_ahorro(self, porcentaje_ahorro):
        """Evalúa el nivel de ahorro con lógica difusa"""
        if porcentaje_ahorro >= self.umbral_ahorro_saludable * 0.9:
            return "saludable"
        elif porcentaje_ahorro >= self.umbral_ahorro_saludable * 0.6:
            return "aceptable"
        else:
            return "bajo"
    
    def evaluar_deuda(self, porcentaje_deuda):
        """Evalúa el nivel de deuda con márgenes de tolerancia"""
        if porcentaje_deuda <= self.umbral_deuda_alerta * 1.1:  # 10% de margen
            return "adecuado"
        elif porcentaje_deuda <= self.umbral_deuda_peligro * 1.1:
            return "moderado"
        else:
            return "alto"
    
    def evaluar_patrimonio(self, patrimonio_neto):
        """Evalúa el patrimonio con consideración de casos límite"""
        if patrimonio_neto > 1000:  
            return "favorable"
        elif patrimonio_neto >= 0:
            return "neutral"
        else:
            return "negativo"
    
    def recomendaciones_inversion(self, saldo_libre, nivel_deuda, ahorro, saldo_libre_alto, contexto):
        """Genera recomendaciones considerando el contexto del usuario"""
        recomendaciones = []
        
        if saldo_libre <= 0:
            return ["No hay capacidad de inversión en este momento"]
        
        
        if nivel_deuda == "adecuado":
            recomendaciones.extend([
                "Invertir según perfil de riesgo:",
                " - Conservador: Depósitos a plazo (CETES, pagarés)",
                " - Moderado: Fondos balanceados (ETF de bajo riesgo)",
                " - Agresivo: Acciones/ETF sectoriales"
            ])
        elif nivel_deuda == "moderado":
            recomendaciones.append("Invertir 50% del saldo libre y destinar 50% a reducir deuda")
        
        
        if contexto.get('estudiante', False):
            recomendaciones.append("\nComo estudiante, considera:")
            recomendaciones.append(" - Becas y financiamiento educativo")
            recomendaciones.append(" - Inversiones a muy largo plazo")
        
        
        if ahorro == "saludable" and saldo_libre_alto:
            recomendaciones.extend([
                "\nDiversificación recomendada:",
                " - Corto plazo: Cuentas de ahorro con rendimiento",
                " - Mediano plazo: Fondos de inversión",
                " - Largo plazo: Planes para el retiro"
            ])
        
        return recomendaciones if recomendaciones else ["Considera aumentar tus ingresos o reducir gastos para invertir"]
    
    def recomendaciones_deuda(self, nivel_deuda, ahorro, contexto):
        """Estrategias personalizadas para manejo de deuda"""
        acciones = []
        
        if nivel_deuda == "alto":
            acciones.extend([
                "🚨 Estrategia anti-deuda:",
                "1. Congelar nuevas deudas (no más créditos)",
                "2. Priorizar deudas con mayor interés (método avalancha)",
                "3. Negociar tasas de interés con acreedores"
            ])
            
            if ahorro == "bajo":
                acciones.extend([
                    "\n🔧 Plan de emergencia:",
                    "1. Eliminar gastos no esenciales (entretenimiento, suscripciones)",
                    "2. Reestructurar deudas (unificar pagos)",
                    "3. Establecer ahorro automático mínimo (aunque sea pequeño)"
                ])
        
        
        if contexto.get('vive_solo', False):
            acciones.append("\n💡 Como vives solo, considera compartir gastos fijos (vivienda, servicios)")
        
        return acciones
    
    def validar_datos(self, datos):
        """Valida la coherencia de los datos ingresados"""
        errores = []
        
        if datos['ingreso_mensual'] <= 0:
            errores.append("El ingreso debe ser mayor a cero")
        
        if datos['gastos_fijos'] + datos['gastos_variables'] > datos['ingreso_mensual'] * 0.9:
            errores.append("Advertencia: Tus gastos superan el 90% de tus ingresos")
        
        if datos['deuda_mensual'] > datos['ingreso_mensual'] * 0.5:
            errores.append("¡Alerta! Tus pagos de deuda son muy altos para tus ingresos")
        
        return errores
    
    def analizar_finanzas(self, datos_usuario):
        """Procesa todos los datos y genera recomendaciones completas"""
        
        if errores := self.validar_datos(datos_usuario):
            return {"errores": errores}
        
        
        ahorro_mensual = datos_usuario['ingreso_mensual'] - (datos_usuario['gastos_fijos'] + datos_usuario['gastos_variables'] + datos_usuario['deuda_mensual'])
        porcentaje_ahorro = ahorro_mensual / datos_usuario['ingreso_mensual']
        porcentaje_deuda = datos_usuario['deuda_mensual'] / datos_usuario['ingreso_mensual']
        saldo_libre = ahorro_mensual
        saldo_libre_alto = saldo_libre > (datos_usuario['ingreso_mensual'] * 0.2)  
        
        
        evaluaciones = {
            "ahorro": self.evaluar_ahorro(porcentaje_ahorro),
            "deuda": self.evaluar_deuda(porcentaje_deuda),
            "patrimonio": self.evaluar_patrimonio(datos_usuario['patrimonio_neto']),
            "porcentaje_ahorro": porcentaje_ahorro,
            "porcentaje_deuda": porcentaje_deuda
        }
        
        
        recomendaciones = {
            "inversion": self.recomendaciones_inversion(
                saldo_libre, 
                evaluaciones["deuda"], 
                evaluaciones["ahorro"], 
                saldo_libre_alto,
                datos_usuario.get('contexto', {})
            ),
            "deuda": self.recomendaciones_deuda(
                evaluaciones["deuda"], 
                evaluaciones["ahorro"],
                datos_usuario.get('contexto', {})
            )
        }
        
        
        datos_historico = {
            **datos_usuario,
            **evaluaciones,
            "saldo_libre": saldo_libre
        }
        self.guardar_en_historico(datos_historico)
        
        return {
            "evaluaciones": evaluaciones,
            "recomendaciones": recomendaciones,
            "metricas": {
                "ahorro_mensual": ahorro_mensual,
                "porcentaje_ahorro": porcentaje_ahorro,
                "porcentaje_deuda": porcentaje_deuda
            }
        }

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto Financiero - Culiacán")
        self.root.geometry("800x600")
        self.sistema = SistemaFinanciero()
        
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        
        self.crear_formulario()
        self.crear_area_resultados()
    
    def crear_formulario(self):
        """Crea el formulario de entrada de datos"""
        frame_form = ttk.Frame(self.root, padding="20")
        frame_form.pack(fill=tk.BOTH, expand=True)
        
        
        ttk.Label(frame_form, text="📊 Ingresa tus datos financieros", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos financieros
        campos = [
            ("Ingreso mensual:", "ingreso_mensual"),
            ("Gastos fijos (renta, servicios):", "gastos_fijos"),
            ("Gastos variables (comida, transporte):", "gastos_variables"),
            ("Pago mensual de deudas:", "deuda_mensual"),
            ("Patrimonio neto (ahorros - deudas):", "patrimonio_neto")
        ]
        
        self.entries = {}
        for i, (texto, nombre) in enumerate(campos, start=1):
            ttk.Label(frame_form, text=texto).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(frame_form)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            self.entries[nombre] = entry
        
        
        ttk.Label(frame_form, text="\nContexto personal (opcional):", style='Header.TLabel').grid(row=len(campos)+1, column=0, columnspan=2, pady=(15,5))
        
        self.contexto_vars = {
            'estudiante': tk.BooleanVar(),
            'vive_solo': tk.BooleanVar()
        }
        
        ttk.Checkbutton(frame_form, text="Soy estudiante", variable=self.contexto_vars['estudiante']).grid(row=len(campos)+2, column=0, sticky=tk.W)
        ttk.Checkbutton(frame_form, text="Vivo solo", variable=self.contexto_vars['vive_solo']).grid(row=len(campos)+2, column=1, sticky=tk.W)
        
        
        btn_analizar = ttk.Button(frame_form, text="Analizar mis finanzas", command=self.analizar_datos)
        btn_analizar.grid(row=len(campos)+3, column=0, columnspan=2, pady=20)
        
        
        frame_form.columnconfigure(1, weight=1)
    
    def crear_area_resultados(self):
        """Crea el área donde se mostrarán los resultados"""
        self.frame_resultados = ttk.Frame(self.root, padding="20")
        
        
        self.notebook = ttk.Notebook(self.frame_resultados)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        
        self.tab_evaluacion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_evaluacion, text="Evaluación")
        
        
        self.tab_recomendaciones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_recomendaciones, text="Recomendaciones")
        
        
        self.tab_metricas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_metricas, text="Métricas")
        
        
        self.inicializar_tab_evaluacion()
        self.inicializar_tab_recomendaciones()
        self.inicializar_tab_metricas()
    
    def inicializar_tab_recomendaciones(self):
        
        main_frame = ttk.Frame(self.tab_recomendaciones)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        
        ttk.Label(scrollable_frame, text="💡 Recomendaciones Personalizadas", style='Header.TLabel').pack(pady=(0, 15))
        
        
        inv_frame = ttk.LabelFrame(scrollable_frame, text="Inversiones", padding=10)
        inv_frame.pack(fill=tk.X, pady=5)
        
        
        inv_text_frame = ttk.Frame(inv_frame)
        inv_text_frame.pack(fill=tk.BOTH, expand=True)
        
        inv_scroll = ttk.Scrollbar(inv_text_frame)
        self.txt_inversion = tk.Text(inv_text_frame, height=6, wrap=tk.WORD, 
                                   font=('Arial', 9), yscrollcommand=inv_scroll.set)
        inv_scroll.config(command=self.txt_inversion.yview)
        
        self.txt_inversion.pack(side="left", fill=tk.BOTH, expand=True)
        inv_scroll.pack(side="right", fill=tk.Y)
        
        
        deuda_frame = ttk.LabelFrame(scrollable_frame, text="Manejo de Deudas", padding=10)
        deuda_frame.pack(fill=tk.X, pady=5)
        
        deuda_text_frame = ttk.Frame(deuda_frame)
        deuda_text_frame.pack(fill=tk.BOTH, expand=True)
        
        deuda_scroll = ttk.Scrollbar(deuda_text_frame)
        self.txt_deuda = tk.Text(deuda_text_frame, height=6, wrap=tk.WORD, 
                               font=('Arial', 9), yscrollcommand=deuda_scroll.set)
        deuda_scroll.config(command=self.txt_deuda.yview)
        
        self.txt_deuda.pack(side="left", fill=tk.BOTH, expand=True)
        deuda_scroll.pack(side="right", fill=tk.Y)

    def inicializar_tab_evaluacion(self):
        main_frame = ttk.Frame(self.tab_evaluacion)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        
        ttk.Label(scrollable_frame, text="📈 Evaluación Financiera", style='Header.TLabel').pack(pady=(0, 15))
        
        
        indicadores_frame = ttk.LabelFrame(scrollable_frame, text="Indicadores Clave", padding=10)
        indicadores_frame.pack(fill=tk.X, pady=5)
        
        
        self.lbl_ahorro = ttk.Label(indicadores_frame, text="Ahorro: ")
        self.lbl_ahorro.pack(anchor=tk.W, pady=2)
        
        self.lbl_deuda = ttk.Label(indicadores_frame, text="Nivel de deuda: ")
        self.lbl_deuda.pack(anchor=tk.W, pady=2)
        
        self.lbl_patrimonio = ttk.Label(indicadores_frame, text="Patrimonio: ")
        self.lbl_patrimonio.pack(anchor=tk.W, pady=2)
        
        
        consejos_frame = ttk.LabelFrame(scrollable_frame, text="Consejos Inmediatos", padding=10)
        consejos_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        text_frame = ttk.Frame(consejos_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        consejos_scroll = ttk.Scrollbar(text_frame)
        self.txt_consejos = tk.Text(text_frame, height=8, wrap=tk.WORD, 
                                  font=('Arial', 9), yscrollcommand=consejos_scroll.set)
        consejos_scroll.config(command=self.txt_consejos.yview)
        
        self.txt_consejos.pack(side="left", fill=tk.BOTH, expand=True)
        consejos_scroll.pack(side="right", fill=tk.Y)

    def inicializar_tab_metricas(self):
        
        main_frame = ttk.Frame(self.tab_metricas)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        
        ttk.Label(scrollable_frame, text="📊 Métricas Financieras", style='Header.TLabel').pack(pady=(0, 15))
        
        
        metricas_frame = ttk.LabelFrame(scrollable_frame, text="Indicadores Numéricos", padding=10)
        metricas_frame.pack(fill=tk.X, pady=5)
        
        
        ttk.Label(metricas_frame, text="Porcentaje de ahorro sobre ingresos:").pack(anchor=tk.W, pady=2)
        self.lbl_porc_ahorro = ttk.Label(metricas_frame, text="0%", font=('Arial', 10, 'bold'))
        self.lbl_porc_ahorro.pack(anchor=tk.W, pady=2)
        
        ttk.Label(metricas_frame, text="Porcentaje de deuda sobre ingresos:").pack(anchor=tk.W, pady=2)
        self.lbl_porc_deuda = ttk.Label(metricas_frame, text="0%", font=('Arial', 10, 'bold'))
        self.lbl_porc_deuda.pack(anchor=tk.W, pady=2)
        
        ttk.Label(metricas_frame, text="Saldo disponible mensual:").pack(anchor=tk.W, pady=2)
        self.lbl_saldo_libre = ttk.Label(metricas_frame, text="$0.00", font=('Arial', 10, 'bold'))
        self.lbl_saldo_libre.pack(anchor=tk.W, pady=2)
        
       
        ttk.Label(scrollable_frame, text="\nDistribución de tus ingresos:", style='Header.TLabel').pack(pady=(15,5))
        
        dist_frame = ttk.Frame(scrollable_frame)
        dist_frame.pack(fill=tk.BOTH, expand=True)
        
        dist_scroll = ttk.Scrollbar(dist_frame)
        self.txt_distribucion = tk.Text(dist_frame, height=8, wrap=tk.WORD, 
                                      font=('Arial', 9), yscrollcommand=dist_scroll.set)
        dist_scroll.config(command=self.txt_distribucion.yview)
        
        self.txt_distribucion.pack(side="left", fill=tk.BOTH, expand=True)
        dist_scroll.pack(side="right", fill=tk.Y)
    
    def analizar_datos(self):
        """Recoge los datos del formulario y ejecuta el análisis"""
        try:
            # Obtener datos financieros
            datos = {
                'ingreso_mensual': float(self.entries['ingreso_mensual'].get()),
                'gastos_fijos': float(self.entries['gastos_fijos'].get()),
                'gastos_variables': float(self.entries['gastos_variables'].get()),
                'deuda_mensual': float(self.entries['deuda_mensual'].get()),
                'patrimonio_neto': float(self.entries['patrimonio_neto'].get()),
                'contexto': {
                    'estudiante': self.contexto_vars['estudiante'].get(),
                    'vive_solo': self.contexto_vars['vive_solo'].get()
                }
            }
            
            # Ejecutar análisis
            resultados = self.sistema.analizar_finanzas(datos)
            
            if 'errores' in resultados:
                messagebox.showerror("Errores en los datos", "\n".join(resultados['errores']))
                return
            
            # Mostrar resultados
            self.mostrar_resultados(resultados)
            
            # Mostrar frame de resultados
            self.frame_resultados.pack(fill=tk.BOTH, expand=True)
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos en todos los campos")
    
    def mostrar_resultados(self, resultados):
        # Evaluación
        evaluaciones = resultados['evaluaciones']
        self.lbl_ahorro.config(text=f"Ahorro: {evaluaciones['ahorro'].capitalize()}")
        self.lbl_deuda.config(text=f"Nivel de deuda: {evaluaciones['deuda'].capitalize()}")
        self.lbl_patrimonio.config(text=f"Patrimonio: {evaluaciones['patrimonio'].capitalize()}")
        
        # Consejos inmediatos
        consejos = []
        if evaluaciones['ahorro'] == "bajo":
            consejos.append("🔴 Considera reducir gastos para aumentar tu ahorro mensual")
        if evaluaciones['deuda'] == "alto":
            consejos.append("🔴 Prioriza el pago de deudas para evitar problemas financieros")
        if evaluaciones['patrimonio'] == "negativo":
            consejos.append("🔴 Tu patrimonio neto es negativo - enfócate en reducir deudas")
        
        self.txt_consejos.config(state=tk.NORMAL)
        self.txt_consejos.delete(1.0, tk.END)
        self.txt_consejos.insert(tk.END, "\n".join(consejos) if consejos else "✅ Tus finanzas parecen estar en buen estado general")
        self.txt_consejos.config(state=tk.DISABLED)
        
        # Recomendaciones de inversión
        self.txt_inversion.config(state=tk.NORMAL)
        self.txt_inversion.delete(1.0, tk.END)
        self.txt_inversion.insert(tk.END, "\n".join(resultados['recomendaciones']['inversion']))
        self.txt_inversion.config(state=tk.DISABLED)
        
        # Recomendaciones de deuda
        self.txt_deuda.config(state=tk.NORMAL)
        self.txt_deuda.delete(1.0, tk.END)
        self.txt_deuda.insert(tk.END, "\n".join(resultados['recomendaciones']['deuda']) if resultados['recomendaciones']['deuda'] else "No se detectaron problemas graves de deuda")
        self.txt_deuda.config(state=tk.DISABLED)
        
        # Métricas
        metricas = resultados['metricas']
        self.lbl_porc_ahorro.config(text=f"{metricas['porcentaje_ahorro']*100:.1f}%")
        self.lbl_porc_deuda.config(text=f"{metricas['porcentaje_deuda']*100:.1f}%")
        self.lbl_saldo_libre.config(text=f"${metricas['ahorro_mensual']:,.2f}")
        
        ingresos = float(self.entries['ingreso_mensual'].get())
        gastos_fijos = float(self.entries['gastos_fijos'].get())
        gastos_variables = float(self.entries['gastos_variables'].get())
        deuda_mensual = float(self.entries['deuda_mensual'].get())
        ahorro_mensual = metricas['ahorro_mensual']
        
        distribucion = [
            f"💰 Ingresos totales: ${ingresos:,.2f}",
            f"🧾 Gastos fijos: {gastos_fijos/ingresos*100:.1f}%",
            f"🛍️ Gastos variables: {gastos_variables/ingresos*100:.1f}%",
            f"💳 Pagos de deuda: {deuda_mensual/ingresos*100:.1f}%",
            f"📈 Ahorro disponible: {metricas['porcentaje_ahorro']*100:.1f}%"
        ]
        
        self.txt_distribucion.config(state=tk.NORMAL)
        self.txt_distribucion.delete(1.0, tk.END)
        self.txt_distribucion.insert(tk.END, "\n".join(distribucion))
        self.txt_distribucion.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()

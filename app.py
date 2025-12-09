from flask import Flask, render_template, request, jsonify
import math
import traceback

app = Flask(__name__)
#
#
#
#
#
# --- RUTAS ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculadora')
def calculadora():
    return render_template('app.html')
#
#
#
#
#
#
#
# --- LÓGICA ---
def gcd(a, b):
    # Calcula Máximo Común Divisor para simplificar vectores
    try:
        a = int(round(abs(a)))
        b = int(round(abs(b)))
        if a == 0: return b
        if b == 0: return a
        while b:
            a, b = b, a % b
        return a
    except:
        return 1

def formato_num(n):
    """
    CORRECCIÓN IMPORTANTE:
    Esta función causaba el error de los '0'. Ahora maneja enteros correctamente.
    """
    try:
        if n is None: return 0
        if isinstance(n, (int, float)) and abs(n) < 0.0001: return 0
        
        # SI YA ES UN ENTERO (ej: 4), LO DEVOLVEMOS DIRECTO
        # Antes intentaba llamar a .is_integer() aquí y fallaba
        if isinstance(n, int): return n
        
        n = round(n, 4)
        if n.is_integer():
            return int(n)
        return round(n, 2)
    except:
        return n # Si falla, devuelve el número original en vez de 0

def safe_float(val):
    if not val: return 0.0
    try:
        val = str(val).replace(',', '.')
        return float(val)
    except:
        return 0.0

@app.route('/api/calcular', methods=['POST'])
def calcular():
    data = request.json
    try:
        a = safe_float(data.get('a'))
        b = safe_float(data.get('b'))
        c = safe_float(data.get('c'))
        d = safe_float(data.get('d'))
        return jsonify(resolver_matriz(a, b, c, d))
    except Exception as e:
        print(f"Error server: {traceback.format_exc()}")
        return jsonify({"status": "error", "mensaje": "Error interno."})

def resolver_matriz(a, b, c, d):
    # CÁLCULOS MATEMÁTICOS
    traza = a + d
    det = (a * d) - (b * c)
    coef_b = -traza
    coef_c = det
    discriminante = coef_b**2 - 4*coef_c
    
    pasos_fase1 = []
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # ---------------------------------------------------------
    # FASE 1: VALORES PROPIOS (DISEÑO VISUAL ORIGINAL)
    # ---------------------------------------------------------
    
    # PASO 1: MATRICIALIZACIÓN
    html_p1 = f"""
    <div class="flex flex-col items-center justify-center font-mono text-lg">
        <div class="mb-2 text-slate-400">A =</div>
        <div class="flex items-center gap-2">
            <div class="grid grid-cols-2 gap-x-8 gap-y-2 border-l-2 border-r-2 border-slate-500 px-4 py-2 bg-slate-900/50 rounded">
                <span class="text-right">{formato_num(a)}</span>
                <span class="text-right">{formato_num(b)}</span>
                <span class="text-right">{formato_num(c)}</span>
                <span class="text-right">{formato_num(d)}</span>
            </div>
        </div>
    </div>
    """
    pasos_fase1.append({
        "id": "p1",
        "titulo": "Paso 1: Matricialización de la Transformación",
        "desc": "Convierte la función T(x,y) en la matriz A:",
        "html": html_p1
    })
    #
    #
    #
    #
    #
    # PASO 2: DETERMINANTE
    html_p2 = f"""
    <div class="flex flex-col items-center justify-center font-mono text-lg space-y-4">
        <div class="text-yellow-400">|A - λI| = 0</div>
        <div class="flex items-center gap-3">
            <div class="grid grid-cols-2 gap-x-8 gap-y-4 border-l-2 border-r-2 border-slate-500 px-6 py-3 bg-slate-900/50 rounded">
                <div class="whitespace-nowrap">{formato_num(a)} - λ</div>
                <div class="whitespace-nowrap">{formato_num(b)}</div>
                <div class="whitespace-nowrap">{formato_num(c)}</div>
                <div class="whitespace-nowrap">{formato_num(d)} - λ</div>
            </div>
            <span class="text-2xl">= 0</span>
        </div>
    </div>
    """
    pasos_fase1.append({
        "id": "p2",
        "titulo": "Paso 2: Planteamiento del Determinante",
        "desc": "Restamos λ en la diagonal principal:",
        "html": html_p2
    })
    #
    #
    #
    #
    #
    # PASO 3: EXPANSIÓN POLINÓMICA
    signo_b = "-" if coef_b < 0 else "+"
    signo_c = "-" if coef_c < 0 else "+"
    polinomio = f"λ² {signo_b} {abs(formato_num(coef_b))}λ {signo_c} {abs(formato_num(coef_c))} = 0"
    
    term1 = f"({formato_num(a)} - λ)({formato_num(d)} - λ)"
    term2 = f"({formato_num(b)})({formato_num(c)})"
    
    html_p3 = f"""
    <div class="flex flex-col items-center justify-center font-mono space-y-3 text-lg">
        <div class="text-slate-300 text-center text-sm mb-2">Multiplica en cruz: (diagonal principal) - (diagonal secundaria)</div>
        <div class="text-blue-300">{term1} - {term2} = 0</div>
        <div class="text-slate-500 text-sm">Expandiendo y simplificando:</div>
        <div class="text-green-400 font-bold text-xl bg-slate-900 px-4 py-2 rounded border border-green-900/50">{polinomio}</div>
    </div>
    """
    pasos_fase1.append({"id": "p3", "titulo": "Paso 3: Expansión Polinómica", "html": html_p3})
    #
    #
    #
    #
    #
    # PASO 4: RESOLUCIÓN
    l1, l2 = 0, 0
    # Usamos un umbral pequeño para evitar errores de punto flotante en complejos
    es_complejo = discriminante < -0.0001

    if es_complejo:
        parte_real = -coef_b / 2
        parte_imag = math.sqrt(abs(discriminante)) / 2
        
        l1_str = f"{formato_num(parte_real)} + {formato_num(parte_imag)}i"
        l2_str = f"{formato_num(parte_real)} - {formato_num(parte_imag)}i"
        
        html_general = f"""
        <div class="flex flex-col items-center font-mono space-y-3">
            <div class="text-red-400 text-xl font-bold uppercase border-b border-red-500 pb-2">
                NO HAY VALORES PROPIOS REALES
            </div>
            <div class="text-slate-400 text-sm mt-2">
                El discriminante es negativo (Δ = {formato_num(discriminante)}), lo que indica soluciones imaginarias:
            </div>
            <div class="bg-slate-900 px-4 py-2 rounded text-slate-300 text-base font-bold">
                λ₁ = {l1_str} <br> 
                λ₂ = {l2_str}
            </div>
            <div class="text-xs text-slate-500 mt-2 p-2 border border-slate-700 rounded">
                Nota: No se grafican vectores para valores complejos en este plano 2D.
            </div>
        </div>
        """
        pasos_fase1.append({"id": "p4", "titulo": "Paso 4: Fórmula General (Complejos)", "html": html_general, "tipo": "general"})
        
        return {
            "status": "success",
            "eigenvalores": [],
            "pasos_fase1": pasos_fase1
        }

    else:
        # CASO REAL
        sqrt_delta = math.sqrt(max(0, discriminante))
        l1 = (-coef_b + sqrt_delta) / 2
        l2 = (-coef_b - sqrt_delta) / 2
        
        # Detectamos si es entero para usar el diseño de Aspa Simple
        es_entero = abs(l1 - round(l1)) < 0.001 and abs(l2 - round(l2)) < 0.001

        if es_entero:
            l1 = int(round(l1))
            l2 = int(round(l2))
            
            # Variables para el diseño de factorización
            f1 = -l1
            f2 = -l2
            signo_f1 = "-" if f1 < 0 else "+"
            signo_f2 = "-" if f2 < 0 else "+"
            
            html_aspa = f"""
            <div class="flex flex-col items-center font-mono">
                 <div class="mb-4 text-slate-300 text-sm">Buscamos dos números que multiplicados den <span class="text-cyan-400">{int(coef_c)}</span> y sumados den <span class="text-cyan-400">{int(coef_b)}</span></div>
                 <div class="bg-slate-900 p-6 rounded-lg border border-purple-500/30 min-w-[200px] text-center">
                    <div class="text-yellow-400 text-sm mb-2 font-bold uppercase tracking-wider">Aspa Simple</div>
                    <div class="flex flex-col gap-2 text-xl text-white">
                        <div class="flex justify-between gap-8 border-b border-slate-700 pb-2"><span>λ</span> <span>{signo_f1} {abs(int(f1))}</span></div>
                        <div class="flex justify-between gap-8"><span>λ</span> <span>{signo_f2} {abs(int(f2))}</span></div>
                    </div>
                 </div>
                 <div class="mt-4 text-green-400 font-bold text-lg border-t border-slate-700 pt-2 w-full text-center">
                    λ₁ = {formato_num(l1)}, λ₂ = {formato_num(l2)}
                 </div>
            </div>
            """
            pasos_fase1.append({"id": "p4", "titulo": "Paso 4: Factorización por Aspa Simple", "html": html_aspa, "tipo": "aspa"})
        else:
            l1, l2 = round(l1, 2), round(l2, 2)
            html_general = f"""
            <div class="flex flex-col items-center font-mono space-y-3">
                <div class="text-orange-400 text-sm font-bold">PLAN B: FÓRMULA GENERAL</div>
                <div class="bg-slate-900 px-4 py-2 rounded text-slate-300">Δ = ({formato_num(coef_b)})² - 4(1)({formato_num(coef_c)}) = {formato_num(discriminante)}</div>
                <div class="text-green-400 font-bold mt-2">λ₁ ≈ {formato_num(l1)}, λ₂ ≈ {formato_num(l2)}</div>
            </div>
            """
            pasos_fase1.append({"id": "p4", "titulo": "Paso 4: Fórmula General", "html": html_general, "tipo": "general"})
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # ---------------------------------------------------------
    # FASE 2: VECTORES PROPIOS (CORREGIDO PARA MOSTRARSE)
    # ---------------------------------------------------------
    vectores = []
    unique_lambdas = sorted(list(set([l1, l2])), reverse=True)
    
    for i, lam in enumerate(unique_lambdas):
        pasos_vec = []
        
        # Cálculos para matriz A - λI
        lam_val = float(lam)
        m11 = a - lam_val
        m12 = b
        m21 = c
        m22 = d - lam_val
        
        matriz_resta = f"""
        <div class="flex items-center gap-2 justify-center">
            <span class="text-slate-400">A - ({formato_num(lam)})I = </span>
            <div class="grid grid-cols-2 gap-x-6 gap-y-1 border-l-2 border-r-2 border-slate-500 px-3 py-1 bg-slate-900/50 rounded">
                <span class="text-right font-bold">{formato_num(m11)}</span> <span class="text-right font-bold">{formato_num(m12)}</span>
                <span class="text-right font-bold">{formato_num(m21)}</span> <span class="text-right font-bold">{formato_num(m22)}</span>
            </div>
        </div>
        """
        pasos_vec.append({"t": "Sub-paso A: Restamos λ a la diagonal", "c": matriz_resta})
        #
        #
        #
        #
        #
        # Sistema de Ecuaciones
        sistema_eq = f"""
        <div class="flex flex-col gap-2 text-sm bg-slate-900/50 p-3 rounded border border-slate-700">
            <div class="flex gap-2">
                <span class="text-slate-500 w-4">1)</span>
                <span class="text-white">{formato_num(m11)}x + {formato_num(m12)}y = 0</span>
            </div>
            <div class="flex gap-2">
                <span class="text-slate-500 w-4">2)</span>
                <span class="text-white">{formato_num(m21)}x + {formato_num(m22)}y = 0</span>
            </div>
        </div>
        """
        pasos_vec.append({"t": "Sub-paso B: Planteamos el Sistema", "c": sistema_eq})

        # Resolución (Método de Cruce)
        vx, vy = 1.0, 0.0
        explicacion_cruce = ""
        
        if abs(m12) > 0.0001: 
            vx = m12
            vy = -m11
            explicacion_cruce = f"""
            <div class="flex flex-col gap-3">
                <div class="text-slate-300 text-sm">
                    Usamos la <strong>Ecuación 1</strong>: <br>
                    <span class="text-blue-300 font-mono pl-4 block mt-1">{formato_num(m11)}x = {-formato_num(m12)}y</span>
                </div>
                <div class="bg-slate-900 p-3 rounded border-l-4 border-purple-500">
                    <div class="text-xs text-purple-400 font-bold uppercase mb-1">Método del Cruce</div>
                    <div class="grid grid-cols-2 gap-4 text-center">
                        <div>
                            <span class="block text-slate-500 text-xs">Valor para X</span>
                            <span class="text-xl font-bold text-white">{formato_num(vx)}</span>
                            <span class="block text-slate-600 text-[10px]">(Viene de Y)</span>
                        </div>
                        <div>
                            <span class="block text-slate-500 text-xs">Valor para Y</span>
                            <span class="text-xl font-bold text-white">{formato_num(vy)}</span>
                            <span class="block text-slate-600 text-[10px]">(Viene de X cambiado)</span>
                        </div>
                    </div>
                </div>
            </div>
            """
        elif abs(c) > 0.0001: 
            vx = -(d - lam_val) 
            vy = c
            explicacion_cruce = f"""
            <div class="flex flex-col gap-3">
                <div class="text-slate-300 text-sm">Usamos la <strong>Ecuación 2</strong> (Ecuación 1 es nula):</div>
                <div class="bg-slate-900 p-3 rounded border-l-4 border-purple-500">
                    <div class="text-xs text-purple-400 font-bold uppercase mb-1">Método del Cruce</div>
                    <div class="text-center text-white font-mono">x = {formato_num(vx)}, y = {formato_num(vy)}</div>
                </div>
            </div>
            """
        elif abs(m11) > 0.0001: 
            vx, vy = 0.0, 1.0
            explicacion_cruce = "Caso especial: x = 0. Variable y libre (y=1)."
        else:
            vx, vy = 1.0, 0.0
            explicacion_cruce = "Vector nulo. Caso identidad."

        pasos_vec.append({"t": "Sub-paso C: Método del Cruce", "c": explicacion_cruce})
        #
        #
        #
        #
        #
        # Simplificación
        vx = round(vx, 4)
        vy = round(vy, 4)
        
        if vx.is_integer() and vy.is_integer():
            vx_int, vy_int = int(vx), int(vy)
            comun = gcd(abs(vx_int), abs(vy_int))
            if comun != 0 and comun != 1:
                vx = vx_int // comun
                vy = vy_int // comun
                html_simpl = f"""
                <div class="flex items-center gap-3">
                    <div class="text-slate-400 line-through decoration-red-500">[{formato_num(vx_int)}, {formato_num(vy_int)}]</div>
                    <div class="text-slate-500">→</div>
                    <div class="text-green-400 font-bold">[{formato_num(vx)}, {formato_num(vy)}]</div>
                    <div class="text-xs text-slate-500 ml-2">(Dividido entre {comun})</div>
                </div>
                """
                pasos_vec.append({"t": "Sub-paso D: Simplificación", "c": html_simpl})
        
        # Signos estéticos
        if vx < 0 or (vx == 0 and vy < 0):
            vx, vy = -vx, -vy

        vec_str = f"[{formato_num(vx)}, {formato_num(vy)}]"
        pasos_vec.append({"t": "Resultado Final", "c": f"<span class='text-2xl font-bold text-white'>{vec_str}</span>"})
        
        # IMPORTANTE: Restauramos 'x' e 'y' para que el frontend grafique bien
        vectores.append({
            "id": i+1,
            "lambda": formato_num(lam),
            "vector": vec_str,
            "x": vx,
            "y": vy,
            "pasos": pasos_vec
        })

    return {
        "status": "success",
        "eigenvalores": vectores,
        "pasos_fase1": pasos_fase1
    }

if __name__ == '__main__':
    app.run(debug=True, port=8000)
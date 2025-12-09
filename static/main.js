// Variables globales para el gráfico
let currentVectors = [];
let currentScale = 40; // Zoom inicial
const baseSize = 500;
const center = baseSize / 2;

function switchTab(tabName) {
    document.querySelectorAll('.view-section').forEach(el => el.classList.add('hidden'));

    // Resetear estilos botones (Estilos inactivos por defecto)
    const inactiveClass = "px-6 py-3 rounded-lg font-bold text-sm uppercase tracking-wider bg-slate-800 text-slate-400 border border-slate-700 hover:bg-slate-700 transition-all";
    document.getElementById('tab-entrada').className = inactiveClass;
    document.getElementById('tab-resultados').className = inactiveClass;
    document.getElementById('tab-pasos').className = inactiveClass;

    // Activar botón actual (Estilo Morado Activo)
    const btn = document.getElementById(`tab-${tabName}`);
    btn.className = "px-6 py-3 rounded-lg font-bold text-sm uppercase tracking-wider bg-purple-600 text-white shadow-lg transition-all transform hover:-translate-y-1";
    btn.disabled = false; // Asegurar que el actual no esté disabled

    // Mostrar sección
    document.getElementById(`view-${tabName}`).classList.remove('hidden');
}

function cargarEjemplo(a, b, c, d) {
    document.getElementById('a').value = a;
    document.getElementById('b').value = b;
    document.getElementById('c').value = c;
    document.getElementById('d').value = d;
}

function limpiar() {
    document.querySelectorAll('input').forEach(i => i.value = '');

    switchTab('entrada');

    // Bloquear las otras pestañas
    document.getElementById('tab-resultados').disabled = true;
    document.getElementById('tab-pasos').disabled = true;

    // Añadir opacidad visual para indicar bloqueo
    document.getElementById('tab-resultados').classList.add('opacity-50', 'cursor-not-allowed');
    document.getElementById('tab-pasos').classList.add('opacity-50', 'cursor-not-allowed');
}

async function calcular() {
    const a = document.getElementById('a').value;
    const b = document.getElementById('b').value;
    const c = document.getElementById('c').value;
    const d = document.getElementById('d').value;

    if (!a || !b || !c || !d) {
        alert("Llena todos los campos");
        return;
    }

    try {
        const response = await fetch('/api/calcular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ a, b, c, d })
        });
        const data = await response.json();

        renderizarResultados(data);

        // Habilitamos explícitamente los botones
        const btnRes = document.getElementById('tab-resultados');
        const btnPasos = document.getElementById('tab-pasos');

        btnRes.disabled = false;
        btnPasos.disabled = false;

        // Quitamos las clases de bloqueo visual
        btnRes.classList.remove('opacity-50', 'cursor-not-allowed');
        btnPasos.classList.remove('opacity-50', 'cursor-not-allowed');

        // Cambiamos a la pestaña de resultados
        switchTab('resultados');

    } catch (error) {
        console.error(error);
        alert("Error de conexión");
    }
}

function renderizarResultados(data) {
    if (data.status === 'error') {
        document.getElementById('error-box').innerText = data.mensaje;
        document.getElementById('error-box').classList.remove('hidden');
        document.getElementById('success-content').classList.add('hidden');
        return;
    }

    document.getElementById('error-box').classList.add('hidden');
    document.getElementById('success-content').classList.remove('hidden');
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    // 1. Resumen Resultados
    const divLambdas = document.getElementById('res-lambdas');
    divLambdas.innerHTML = data.eigenvalores.map((ev, i) => `
        <div class="flex items-center justify-between p-4 bg-slate-900 rounded border-l-4 border-green-500 mb-2">
            <div>
                <span class="text-green-400 font-bold text-xs uppercase block">Valor Propio ${i + 1}</span>
                <span class="text-2xl font-mono text-white">λ${i + 1} = ${ev.lambda}</span>
            </div>
        </div>
    `).join('');

    const divVectores = document.getElementById('res-vectores');
    divVectores.innerHTML = data.eigenvalores.map((ev, i) => `
        <div class="p-4 bg-slate-900 rounded border-l-4 ${i === 0 ? 'border-blue-500' : 'border-cyan-500'} mb-2">
            <span class="text-blue-400 font-bold text-xs uppercase block">Para λ${i + 1} = ${ev.lambda}</span>
            <span class="text-xl font-mono text-white">v${i + 1} = ${ev.vector}</span>
        </div>
    `).join('');
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    // 2. FASE 1: Paso a Paso
    const divFase1 = document.getElementById('pasos-fase1');
    divFase1.innerHTML = data.pasos_fase1.map(p => {
        let borderColor = 'border-slate-600';
        let titleColor = 'text-slate-300';

        if (p.id === 'p1') { borderColor = 'border-blue-500'; titleColor = 'text-blue-400'; }
        if (p.id === 'p2') { borderColor = 'border-cyan-500'; titleColor = 'text-cyan-400'; }
        if (p.id === 'p3') { borderColor = 'border-green-500'; titleColor = 'text-green-400'; }
        if (p.id === 'p4') { borderColor = 'border-purple-500'; titleColor = 'text-purple-400'; }

        return `
        <div class="bg-slate-800 border-l-4 ${borderColor} rounded-lg p-6 shadow-lg">
            <h3 class="font-bold ${titleColor} text-lg mb-2">${p.titulo}</h3>
            ${p.desc ? `<p class="text-slate-400 text-sm mb-4 border-b border-slate-700 pb-2">${p.desc}</p>` : ''}
            <div class="mt-2">
                ${p.html}
            </div>
        </div>`;
    }).join('');
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    // 3. FASE 2 VECTORES PROPIOS
    const divFase2 = document.getElementById('pasos-fase2');
    divFase2.innerHTML = data.eigenvalores.map(ev => `
        <div class="bg-slate-800 border border-slate-900 rounded-lg p-6 relative overflow-hidden">
            <div class="absolute top-0 left-0 w-1 h-full bg-pink-500"></div>
            <h3 class="text-pink-400 font-bold text-xl mb-4 pb-2 border-b border-slate-700">Para λ = ${ev.lambda}</h3>
            <div class="space-y-4">
                ${ev.pasos.map(sp => `
                    <div class="bg-slate-900 p-3 rounded border-l-2 border-slate-600">
                        <div class="text-xs text-slate-400 uppercase font-bold tracking-wider">${sp.t}</div>
                        <div class="text-green-400 font-mono mt-1 text-lg">${sp.c}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    // 4. Gráfico
    currentVectors = data.eigenvalores;
    currentScale = 40;
    actualizarGrafico();
}

function zoomIn() {
    currentScale += 10;
    actualizarGrafico();
}

function zoomOut() {
    if (currentScale > 10) currentScale -= 10;
    actualizarGrafico();
}

function actualizarGrafico() {
    if (!currentVectors || currentVectors.length === 0) return;

    const divGrafico = document.getElementById('grafico-container');
    const divLeyenda = document.getElementById('grafico-leyenda');

    let svg = `
        <svg width="100%" height="100%" viewBox="0 0 ${baseSize} ${baseSize}">
            <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1"/>
                </pattern>
                <marker id="arrow-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#a855f7" />
                </marker>
                <marker id="arrow-cyan" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#06b6d4" />
                </marker>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            
            <!-- Ejes -->
            <line x1="0" y1="${center}" x2="${baseSize}" y2="${center}" stroke="#475569" stroke-width="2" />
            <line x1="${center}" y1="0" x2="${center}" y2="${baseSize}" stroke="#475569" stroke-width="2" />
            <text x="${baseSize - 20}" y="${center + 20}" fill="#94a3b8" font-size="14">X</text>
            <text x="${center + 10}" y="20" fill="#94a3b8" font-size="14">Y</text>
    `;

    currentVectors.forEach((v, i) => {
        const color = i === 0 ? '#a855f7' : '#06b6d4';
        const marker = i === 0 ? 'arrow-purple' : 'arrow-cyan';
        const x2 = center + (v.x * currentScale);
        const y2 = center - (v.y * currentScale);

        svg += `
            <g class="hover:opacity-80 transition-opacity">
                <line x1="${center}" y1="${center}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="4" marker-end="url(#${marker})" />
                <circle cx="${x2}" cy="${y2}" r="6" fill="${color}" stroke="#0f172a" stroke-width="2" />
            </g>
        `;
    });

    svg += `</svg>`;
    divGrafico.innerHTML = svg;

    divLeyenda.innerHTML = currentVectors.map((v, i) => {
        const colorClass = i === 0 ? 'text-purple-400 border-purple-500' : 'text-cyan-400 border-cyan-500';
        return `
            <div class="bg-slate-800 px-4 py-2 rounded border-l-4 ${colorClass} shadow-md">
                <div class="font-bold text-sm">V${i + 1} (λ=${v.lambda})</div>
                <div class="font-mono text-white text-xs mt-1">Coords: ${v.vector}</div>
            </div>
        `;
    }).join('');
}
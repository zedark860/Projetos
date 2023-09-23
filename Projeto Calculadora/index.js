var calculadora = {
    um: document.getElementById('um'),
    dois: document.getElementById('dois'),
    tres: document.getElementById('tres'),
    quatro: document.getElementById('quatro'),
    cinco: document.getElementById('cinco'),
    seis: document.getElementById('seis'),
    sete: document.getElementById('sete'),
    oito: document.getElementById('oito'),
    nove: document.getElementById('nove'),
    zero: document.getElementById('zero'),
    divisao: document.getElementById('divisao'),
    multiplicacao: document.getElementById('multiplicacao'),
    menos: document.getElementById('menos'),
    mais: document.getElementById('mais'),
    igual: document.getElementById('igual'),
    apagar: document.getElementById('apagar')
};
var resultados = document.querySelector('.resultados')
resultados.innerHTML = ''

var numeroAtual = ''
var resultadoParcial = 0
var operacaoAnterior = ''
var calculoFinalizado = false

function handleNumeroclick(event) {
    if (calculoFinalizado) {
        numeroAtual = ''
        resultadoParcial = 0
        operacaoAnterior = ''
        calculoFinalizado = false
        resultados.textContent = ''
    }

    var numeroClicado = event.target.textContent
    numeroAtual += numeroClicado
    resultados.textContent = numeroAtual
}

function handleIgualClick() {
    if (numeroAtual !== '') {
        var numero = parseFloat(numeroAtual);
        if (operacaoAnterior === '+') {
            resultadoParcial += numero
        } else if (operacaoAnterior === '-') {
            resultadoParcial -= numero
        } else if (operacaoAnterior === '*') {
            resultadoParcial *= numero;
        } else if (operacaoAnterior === '/') {
            resultadoParcial /= numero
        } else {
            resultadoParcial = numero
        }
        resultados.textContent = resultadoParcial
        numeroAtual = ''
        operacaoAnterior = ''
        calculoFinalizado = true
    }
}

function handleOperacaoClick(event) {
    var operacao = event.target.textContent

    if (numeroAtual !== '') {
        handleIgualClick() 
    }

    operacaoAnterior = operacao
    calculoFinalizado = false
}

for (var procurar in calculadora) {
    if (calculadora.hasOwnProperty(procurar)) {
        switch (procurar) {
            case 'igual':
                calculadora[procurar].addEventListener('click', handleIgualClick);
                break;
            case 'apagar':
                calculadora[procurar].addEventListener('click', function () {
                    resultados.textContent = ''
                    numeroAtual = ''
                    resultadoParcial = 0
                    operacaoAnterior = ''
                    calculoFinalizado = false
                });
                break;
            case 'mais':
            case 'menos':
            case 'multiplicacao':
            case 'divisao':
                calculadora[procurar].addEventListener('click', handleOperacaoClick)
                break
            default:
                calculadora[procurar].addEventListener('click', handleNumeroclick)
                break;
        }
    }
}
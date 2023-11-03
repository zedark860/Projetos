function formatarCPF(campo) {
    // Remove qualquer caractere não numérico
    var cpf = campo.value.replace(/\D/g, '');

    // Adiciona pontos e traço no formato de CPF
    if (cpf.length >= 4) {
        cpf = cpf.substring(0, 3) + '.' + cpf.substring(3);
    }
    if (cpf.length >= 7) {
        cpf = cpf.substring(0, 7) + '.' + cpf.substring(7);
    }
    if (cpf.length >= 11) {
        cpf = cpf.substring(0, 11) + '-' + cpf.substring(11);
    }

    // Define o valor formatado de volta no campo
    campo.value = cpf;
}

function formatarNumero(campo) {
    var numero = campo.value.replace(/\D/g, ''); // Remove caracteres não numéricos

    numero.substring(4, 13) + "4444";

    // Formata o número como (XX) XXXX-XXXX
    if (numero.length === 11) {
        numero = '(' + numero.substring(0, 2) + ') ' + numero.substring(2, 7) + '-' + numero.substring(7);
    }

    // Define o valor formatado de volta no campo
    campo.value = numero;
}

    // Selecionar o elemento de entrada de texto pelo ID
var nomeInput = document.getElementById('nome');

    // Adicionar um ouvinte de evento para o evento "input" no campo de entrada
nomeInput.addEventListener('input', function () {
        // Obter o valor atual do campo de entrada
    var valor = nomeInput.value;

        // Substituir todos os caracteres não alfabéticos por uma string vazia
    valor = valor.replace(/[^a-zA-ZÀ-ú\s]/g, '');

        // Atualizar o valor do campo de entrada apenas com os caracteres válidos
     nomeInput.value = valor;
});

function mostrarOcultarSenha(checkbox, senhaInput) {
    senhaInput.type = checkbox.checked ? 'text' : 'password';
}
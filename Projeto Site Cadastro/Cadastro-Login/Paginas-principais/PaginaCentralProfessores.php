<?php
// Inicie a sessão para acessar a variável da sessão
session_start();

// Verifique se a variável da sessão 'matricula' está definida
if (isset($_SESSION['id'])) {
    $id = $_SESSION['id'];
} else {
    $id = "Id não encontrado";
}

if (isset($_GET['logout']) && $_GET['logout'] === 'true') {
    // Limpe a variável de sessão
    unset($_SESSION['id']);
}
?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../style.css">
    <link rel="shortcut icon" href="../../assets/favicon.ico" type="image/x-icon">
    <title>Línguas Quebec</title>
</head>
<body>
    <header>
        <div class="elementos-header">
            <a href="../../index.html?logout=true"><img src="../../assets/image 4.png" alt="logo-site"></a>
            <h1 style="padding-top: 10px; padding-left: 5px;">Línguas Quebec</h1>
        </div>
        <div style="display: flex; align-items: center; gap: 2px;">
            <img src="../../assets/icon _person_.png" alt="" style="height: 37px;">
            <p style="font-weight: bold; color: rgba(0, 25, 248, 0.61); text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);">Id: <?php echo $id; ?></p>
        </div>
    </header>
    <main class="pagina-central-centralizada">
        <div class="caixas-pag-prin">
            <h2>Área do Professor</h2>
            <img src="../../assets/image 10.png" alt="imagem professor">
        </div>
        <div class="caixas-pag-prin">
            <img src="../../assets/image 5.png" alt="imagem Alunos Matriculados">
            <h3>Alunos Matriculados</h3>
            <button type="button" class="botao-acesso"><a href="">Acessar</a></button>
        </div>
        <div class="caixas-pag-prin">
            <img src="../../assets/image frequenci.png" alt="imagem Frequência">
            <h3>Frequência</h3>
            <button type="button" class="botao-acesso"><a href="">Acessar</a></button>
        </div>
        <div class="caixas-pag-prin">
            <img src="../../assets/image notas.png" alt="imagem Notas">
            <h3>Notas</h3>
            <button type="button" class="botao-acesso"><a href="">Acessar</a></button>
        </div>
        <div class="caixas-pag-prin">
            <img src="../../assets/image calendario.png" alt="">
            <h3>Calendário</h3>
            <button type="button" class="botao-acesso"><a href="">Acessar</a></button>
        </div>
        <div class="caixas-pag-prin">
            <img src="../../assets/image exercicio.png" alt="">
            <h3>Exercícios</h3>
            <button type="button" class="botao-acesso"><a href="">Acessar</a></button>
        </div>
        <div class="caixas-pag-prin">
            <img src="../../assets/image mural.png" alt="">
            <h3>Mural</h3>
            <button type="button" class="botao-acesso"><a href="">Acessar</a></button>
        </div>
        <div class="caixas-pag-prin">
            <img src="../../assets/image suporte.png" alt="">
            <h3>Suporte</h3>
            <button type="button" class="botao-acesso"><a href="">Acessar</a></button>
        </div>
    </main>
    <script>
        function logoutOnPageClose() {
            var xhr = new XMLHttpRequest()
            xhr.open('GET', 'logout.php', true)
            xhr.send()
        }
        // Adicione o evento 'beforeunload' para fazer logout apenas quando a página é fechada
        window.addEventListener('beforeunload', function(event) {
            var target = event.target
            if (target.tagName === 'A' && target.getAttribute('href') === '../../index.html?logout=true') {
                logoutOnPageClose()
            }
        })
    </script>
    <script src="../Index.js"></script>
</body>
</html>
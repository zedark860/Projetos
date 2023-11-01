<?php

$servername = "localhost";
$username = "root";
$password = "";
$database = "cadastroelogin";

$conn = new mysqli($servername, $username, $password, $database);

if ($conn->connect_error) {
    die("Conexão com o banco de dados falhou: " . $conn->connect_error);
}

$nome = $_POST['nome'];
$matricula = $_POST['matricula'];
$email = $_POST['email'];
$senha = $_POST['senha'];
$cpf = $_POST['cpf'];
$numero = $_POST['numero'];

// Inicia a transação
$conn->begin_transaction();

try {
    // Inserir dados na tabela "alunos"
    $sql_alunos = "INSERT INTO alunos (matricula, senha) VALUES ('$matricula', '$senha')";
    $conn->query($sql_alunos);

    // Inserir dados na tabela "dados_alunos" relacionados à matrícula
    $sql_dados_alunos = "INSERT INTO dados_alunos (matricula_aluno, email_aluno, senha_aluno, cpf_aluno, numero_aluno) VALUES ('$matricula', '$email', '$senha', '$cpf', '$numero')";
    $conn->query($sql_dados_alunos);

    // Confirma a transação
    $conn->commit();
    echo "Cadastro realizado com sucesso.";
} catch (Exception $e) {
    // Em caso de erro, desfaz a transação
    $conn->rollback();
    echo "Erro ao cadastrar: " . $e->getMessage();
}

$conn->close();
?>

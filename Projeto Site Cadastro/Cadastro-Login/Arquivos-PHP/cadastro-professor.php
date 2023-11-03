<?php

$servername = "localhost";
$username = "root";
$password = "1234";
$database = "cadastroelogin";

$conn = new mysqli($servername, $username, $password, $database);

if ($conn->connect_error) {
    die("Conexão com o banco de dados falhou: " . $conn->connect_error);
}

$nome = $_POST['nome'];
$id = $_POST['id'];
$email = $_POST['email'];
$senha = $_POST['senha'];
$cpf = $_POST['cpf'];
$numero = $_POST['numero'];

// Inicia a transação
$conn->begin_transaction();

try {
    // Inserir dados na tabela "professores"
    $sql_professores = "INSERT INTO professores (id, senha) VALUES ('$id', '$senha')";
    $conn->query($sql_professores);

    // Inserir dados na tabela "dados_professores" relacionados ao "id"
    $sql_dados_professores = "INSERT INTO dados_professores (id_professor, email_professor, senha_professor, cpf_professor, numero_professor, nome_professor) VALUES ('$id', '$email', '$senha', '$cpf', '$numero', '$nome')";
    $conn->query($sql_dados_professores);

    // Confirma a transação
    $conn->commit();

    // Redireciona o usuário para outra página
    echo "<script>";
    echo 'alert("Cadastro bem-sucedido!");';
    echo 'window.location.href = "../Paginas-principais/PaginaCentralProfessores.php";';
    echo '</script>';

    session_start();
    $_SESSION['id'] = $id;

} catch (Exception $e) {
    // Em caso de erro, desfaz a transação
    $conn->rollback();
}

$conn->close();
?>

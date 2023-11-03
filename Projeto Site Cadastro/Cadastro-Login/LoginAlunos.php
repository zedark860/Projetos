<?php

if ($_SERVER["REQUEST_METHOD"] == "POST"){

    $matricula = $_POST["matricula"];
    $senha = $_POST["senha"];

    $conn = mysqli_connect("localhost", "root", "1234", "cadastroelogin");

    if (!$conn) {
        die("Falha ao conectar no banco de dados: " . mysqli_connect_error());
    }

    $sql = "SELECT * FROM alunos WHERE matricula = '$matricula' AND senha = '$senha'";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) == 1) {
        echo "<script>";
        echo 'alert("Login bem-sucedido!");';
        echo 'window.location.href = "Paginas-principais/PaginaCentralAlunos.php";';
        echo '</script>';
    } else {
        echo "<script>";
        echo 'alert("Algo deu errado verifique sua credencias!");';
        echo '</script>';
    }

    session_start();
    $_SESSION['matricula'] = $matricula;

    mysqli_close($conn);
}
?>
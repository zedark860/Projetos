<?php

// Inicie a sessão
session_start();

// Limpe todas as variáveis de sessão
session_unset();

// Destrua a sessão
session_destroy();

// Redirecione o usuário de volta para a página inicial
header("Location: ../../index.html");
exit;
?>

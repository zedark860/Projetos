document.addEventListener('DOMContentLoaded', function() {
    var dropButton = document.getElementById('drop-button');
    var menuList = document.getElementById('menu-list');
  
    dropButton.addEventListener('click', function() {
      // Verifique se o menu está aberto ou fechado usando a classe "open"
      if (menuList.classList.contains('open')) {
        // Se estiver aberto, remova a classe "open" para fechar suavemente
        menuList.classList.remove('open');
      } else {
        // Se estiver fechado, adicione a classe "open" para abrir suavemente
        menuList.classList.add('open');
      }
    });
  });
  
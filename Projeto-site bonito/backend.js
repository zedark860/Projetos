document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.querySelector(".bt1"); 
    const navBar = document.querySelector(".ul-menu"); 

    toggleButton.addEventListener("click", function (e) {
        e.preventDefault(); 
        if (navBar.classList.contains("active")) {
            navBar.classList.remove("active");
        } else {
            navBar.classList.add("active");
        }
    });
});

let count = 1;
document.getElementById("radio1").checked = true;

setInterval(function() {
    nextImage();
}, 5000);

function nextImage() {
    count++;
    if (count > 3) {
        count = 1;
    }

    document.getElementById("radio" + count).checked = true;
}

document.addEventListener('DOMContentLoaded', function() {
    const loadingOverlay = document.getElementById('loading-overlay');
    const linksWithLoading = document.querySelectorAll('.opcoes');

    linksWithLoading.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            loadingOverlay.style.display = 'flex';

            setTimeout(function() {
                window.location.href = link.getAttribute('href');
            }, 1000); 
            
            setTimeout(function() {
                loadingOverlay.style.display = 'none';
            }, 1500); 
        });
    });
});


window.onload = function () {
    var popup = document.getElementById('popup');

    popup.style.display = 'flex';
    setTimeout(function () {
        popup.style.opacity = '1';
    }, 100); 

    var close = document.getElementById('close');
    close.onclick = function () {
        
        popup.style.opacity = '0';
        setTimeout(function () {
            popup.style.display = 'none';
        }, 300); 
    };
};

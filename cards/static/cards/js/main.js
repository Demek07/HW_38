// cards/static/cards/js/main.js
// Главный файл для всего приложения, подключается в шаблоне base.html


// Листнер при клике на заголовок H1 добавляет/убирает класс бутсрап 5
// желтый фон и красный текст
// document.querySelector('h1').addEventListener('click', () => {
//     document.querySelector('h1').classList.toggle('text-danger');
//     document.querySelector('h1').classList.toggle('bg-warning');
// });

// function getInputValue() {
//     var inputField = document.getElementById("inputField");
//     var inputValue = inputField.value;
//     alert("Input value: " + inputValue);
// }

// $(document).ready(function(){
//     $(".nav-bar a").hover(
//         function () {
//             // Удалите класс active у всех кнопок
//             $(".nav-bar a").removeClass("active");
//             console.log("hover");

//             // Добавьте класс active к текущей кнопке
//             $(this).addClass("active");
//         }

//     );
// });
$(document).ready(function() {
    $( ".mr-auto .nav-item" ).bind( "click", function(event) {
        event.preventDefault();
        var clickedItem = $( this );
        $( ".mr-auto .nav-item" ).each( function() {
            $( this ).removeClass( "active" );
        });
        clickedItem.addClass( "active" );
    });
});

// $(function () {
//     var url = window.location.href.substr(window.location.href.lastIndexOf('/') + 1);
//     $('.navbar-nav a').each(function () {
//         if ($(this).attr('href') === url || $(this).attr('href') === '') {
//             $(this).parent('li').addClass('active');
//         }
//     });
// }
// );
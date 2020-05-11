document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('button[data-dismiss].btn.btn-secondary').onclick = () => {check_form()}
    
    
    document.querySelectorAll('.card').forEach(ch => {
        ch.addEventListener('mouseover', () => { 
            //alert(1)
            ch.querySelector('.cart_add').hidden = false
        })
        ch.addEventListener('mouseout', () => { 
            //alert(2)
            ch.querySelector('.cart_add').hidden = true
            
        })
    })

    document.querySelectorAll('.cart_add').forEach(button => {
        button.onclick = function(){
            var size = ''
            this.parentElement.querySelectorAll('.custom-control-input').forEach(x => {
                if (x.checked){
                    size = x.id.split('_')[0]
                    document.querySelector('.modal-body p').innerHTML = 'Price: $' + x.value;
                    //query_for_array()
                }
                x.checked = false
            })
            card = this.parentElement.parentElement
            document.querySelector('.modal-title').innerHTML = capitalize(size)+ ' ' + 
                card.querySelector('.card-title').innerHTML + 
                ' ' + document.querySelector('h1').innerHTML
            document.querySelector('.modal-title').dataset.toppings = card.dataset.toppings
        }
    })   
})

function check_form() {
    tops = document.querySelector('.modal-title').dataset.toppings
    if (tops){
        alert(1)
    }
    document.querySelectorAll('div.modal-body2 input').forEach(check => {
        check.checked = false
        //card.dataset.toppings
    })
    
}

function capitalize(string){
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function query_for_array(){
    const request = new XMLHttpRequest();    
    request.open('POST', '/menu_adds');

    var csrftoken = getCookie('csrftoken');

    request.onreadystatechange = function() {//Вызывает функцию при смене состояния.
        if(request.readyState == XMLHttpRequest.DONE && request.status == 200) {
            // Запрос завершен. Здесь можно обрабатывать результат.            
            document.querySelector('.modal-body2 p').innerHTML = request.response
        }
    }
    
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

    const data = new FormData();
    data.append('type_id', 'ssdsdfcvx');
    
    request.send(data);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
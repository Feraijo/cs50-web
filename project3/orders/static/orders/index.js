document.addEventListener('DOMContentLoaded', () => {
    var adds = []

    document.querySelector('#purch_form').onsubmit = function(){
        //var data = new FormData(this)
        inp_id = document.querySelector('#inp_id').value
        var prod_type = document.querySelector('div.modal-body2').dataset.prod_type.trim()
        tops = document.querySelector('div.modal-body2').dataset.toppings
        if (tops && adds.length < tops){
            alert("Choose your toppings!")
            return false;
        }
        data = {
            'type': prod_type,
            'id': inp_id, 
            'adds':adds,
        }
        alert(JSON.stringify(data))        
        return false;
    }

    document.querySelectorAll('.closebut').forEach(but => {
        but.onclick = () => {adds = check_form(adds)}
    })
    
    document.querySelectorAll('.custom-control-input.checkbox').forEach(check => {
        check.onchange = () => {   
            if (check.checked){
                var prod_type = document.querySelector('div.modal-body2').dataset.prod_type
                if (prod_type.trim() === 'Pizza'){
                    var tops = document.querySelector('div.modal-body2').dataset.toppings                    
                    if (isEmpty(tops) || adds.length >= tops){
                            check.checked = false                    
                    } else {
                        adds.push(check.id)
                    }
                } else 
                    adds.push(check.id)
            } else {
                adds.pop(check.id)
            }
        }
    })

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
            this.parentElement.querySelectorAll('.custom-control-input.radio').forEach(x => {
                if (x.checked){                                      
                    size = x.id.split('_')[0]
                    document.querySelector('.modal-body p').innerHTML = 'Price: $' + x.value;
                    document.querySelector('#inp_id').value = x.id;
                    //query_for_array()
                }
                x.checked = false
            })
            prod_type = document.querySelector('h1').innerHTML
            card = this.parentElement
            document.querySelector('.modal-title').innerHTML = capitalize(size)+ ' ' + 
                card.querySelector('.card-title').innerHTML + ' ' + prod_type
            document.querySelector('div.modal-body2').dataset.toppings = card.dataset.toppings
            document.querySelector('div.modal-body2').dataset.prod_type = prod_type
        }
    })   
})

function isEmpty(str) {
    return (!str || 0 === str.length);
}

function check_form(adds) {
    document.querySelectorAll('div.modal-body2 input').forEach(check => {
        check.checked = false        
    })
    adds = []
    return adds
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
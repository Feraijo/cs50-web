document.addEventListener('DOMContentLoaded', () => {
    
    var adds = []

    if (document.querySelector('.cart_item')){
        add_total_price(update_total_price)   
        // document.querySelector('#confirm_order').onclick = () => {
        //     if (confirm('Are you sure?')) {
        //         var form_data = new FormData();
        //         form_data.append('remove', true)
        //         form_data.append('id', close.id)
        //         query_server('/cart', form_data)
        //     }            
        // }    
    }

    document.querySelectorAll('.cart_item').forEach(row => {
        if (row.querySelector('.cancel_purchase')){
            row.addEventListener('mouseover', () => {
                row.querySelector('.cancel_purchase').hidden = false
            })
            row.addEventListener('mouseout', () => {
                row.querySelector('.cancel_purchase').hidden = true
            })        
        }
    })

    document.querySelectorAll('.cancel_purchase').forEach(close => {
        close.onclick = () => {
            if (confirm('Are you sure?')){
                var form_data = new FormData();
                form_data.append('remove', true)
                form_data.append('id', close.id)
                query_server('/cart', form_data)
                row = close.parentElement.parentElement
                row.style.animationPlayState = 'running';
                row.addEventListener('animationend', () =>  {
                    removeElement(row, renumerate_rows)
                    update_total_price()
                })
                
            }            
        }
    })
    
    if (document.querySelector('#purch_form')){
        plus_minus()

        document.querySelector('#form_submit').onclick = function(){
            //var data = new FormData(this)
            amount = document.querySelector('#amount').value
            inp_id = document.querySelector('#inp_id').value
            size = capitalize(inp_id.split('_')[0])
            id = inp_id.split('_')[1]        
            prod_type = document.querySelector('div.modal-body2').dataset.prod_type.trim()
            tops = document.querySelector('div.modal-body2').dataset.toppings
            if (tops && adds.length < tops){
                alert("Choose your toppings!")
                return false;
            }       
             
            var form_data = new FormData();
            form_data.append('remove', false)
            form_data.append('amount', amount)
            form_data.append('type', prod_type)
            form_data.append('id', id)        
            form_data.append('size', size)
            form_data.append('adds', adds)
            //alert(JSON.stringify(form_data))
            query_server('/cart', form_data)
            cart_size = document.querySelector('#cart_size')
            cart_size.innerHTML = parseInt(cart_size.innerHTML) + 1            
            
            return false;
        }
    }

    document.querySelectorAll('.closebut').forEach(but => {
        but.onclick = () => {adds = check_form(adds)}
    })
    
    document.querySelectorAll('.custom-control-input.checkbox').forEach(check => {
        check.onchange = () => {  
            check_val = check.parentElement.querySelector('label').innerHTML.trim()
            id = check.id.split('_')[1]
            if (check.checked){
                var prod_type = document.querySelector('div.modal-body2').dataset.prod_type

                if (prod_type.trim() === 'Pizza'){
                    var tops = document.querySelector('div.modal-body2').dataset.toppings                    
                    if (isEmpty(tops) || adds.length >= tops){
                            check.checked = false                    
                    } else {                        
                        adds.push(id)
                    }
                } else 
                    adds.push(id)
            } else {
                adds.pop(id)
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
            radios = this.parentElement.querySelectorAll('.custom-control-input.radio')
            if (Array.from(radios).some(x => x.checked)){
                var size = ''
                radios.forEach(x => {
                    if (x.checked){                                      
                        size = x.id.split('_')[0]
                        document.querySelector('.modal-body p').innerHTML = 'Price: $' + x.value;
                        document.querySelector('#inp_id').value = x.id;                        
                    }
                    x.checked = false
                })
                prod_type = document.querySelector('h1').innerHTML.trim()
                card = this.parentElement
                document.querySelector('.modal-title').innerHTML = capitalize(size)+ ' ' + 
                    card.querySelector('.card-title').innerHTML.trim() + ' ' + prod_type
                document.querySelector('div.modal-body2').dataset.toppings = card.dataset.toppings
                document.querySelector('div.modal-body2').dataset.prod_type = prod_type
                $('#mymodal').modal('show')
            } else {
                return false;
            }
        }
    })   
})

function plus_minus(){    
    
    document.querySelector('#amount_minus').onclick = () => {
        if (document.querySelector('#amount').value > 1) 
            document.querySelector('#amount').value = parseInt(document.querySelector('#amount').value) - 1            
    }
    document.querySelector('#amount_plus').onclick = () => {
        document.querySelector('#amount').value = parseInt(document.querySelector('#amount').value) + 1
    }
}

function update_total_price(){
    var total = 0.0
    document.querySelectorAll(".total_price").forEach(price => {
        var pp = parseFloat(price.innerHTML.split('$')[1])
        total += pp
    })
    document.querySelector('#total_price_all').innerHTML = '$' + total.toFixed(2)
}

function add_total_price(callback){
    const tot_prc = document.createElement('tr');
    tot_prc.className = 'cart_item';
    tot_prc.append(document.createElement('th'))
    r = document.createElement('td')
    r.innerHTML = "Total price:"
    tot_prc.append(r)
    tot_prc.append(document.createElement('td'))
    tot_prc.append(document.createElement('td'))
    tot_prc.append(document.createElement('td'))
    ppp = document.createElement('th')
    ppp.id = 'total_price_all'
    tot_prc.append(ppp)
    document.querySelector('.table.table-hover').append(tot_prc);
    callback()
}

function renumerate_rows(){
    rows = document.querySelectorAll('.counter')
    update_cart_size(rows.length)
    rows.forEach(function(row_num, index) {
        row_num.innerHTML = index + 1
    })
}

function update_cart_size(num){
    document.querySelector('#cart_size').innerHTML = num
}

function removeElement(element, callback) {
    // Removes an element from the document
    //var element = document.querySelector(elementId);
    element.parentNode.removeChild(element);
    callback()
}

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

function query_server(url, data){
    const request = new XMLHttpRequest();    
    request.open('POST', url, true);
    request.onreadystatechange = function() {//Вызывает функцию при смене состояния.
        if(request.readyState == XMLHttpRequest.DONE){
            if (request.status == 200) {
                // Запрос завершен. Здесь можно обрабатывать результат.            
                //alert(JSON.stringify(request.response))
            } else
                alert('crap')
        }  
    }
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.send(data);
}

function set_message(){

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
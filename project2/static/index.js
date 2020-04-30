
function onclick_switch_channel(socket){
    // add switch active channel on click

    // let active = document.querySelector('#channel_list a .active')
    // //#alert(active)

    let def_ch = document.querySelector('#channel_list :not(.active)')
    var a_class = def_ch.className    
    //def_ch.className = a_class + " active"

    //document.querySelector('#content').innerHTML = def_ch.id + ' content'
    document.querySelectorAll('#channel_list a').forEach(item => {
        item.onclick = function(){
            document.querySelectorAll('#channel_list a').forEach(inner => {
                inner.className = a_class
            });
            item.className = item.className + " active"
            cont = document.querySelector('#content')
            cont.hidden = false
            load_chan_history(item.id, socket)
            //document.querySelector('#content').innerHTML = item.id + ' content'
            //document.querySelector(`#${item.id}_content`).className = cont_class + " active"
            //alert(item.id)
        };
    })
}

function load_chan_history(id, socket){
    socket.emit('load_history', {'id': id});
    //alert(id)
}

function greet(){
    //greet user with name from localStorage

    document.querySelector('#greeting').innerHTML = `Hello, ${localStorage.getItem('name')}`
}

function onsubmit_add_channel(socket){
    // add new channel on submit
    document.querySelector('#add_channel').onsubmit = () => {  
        document.querySelector('#content').hidden = true
        const name = document.querySelector('#new_channel_name').value
        if (name){
            socket.emit('add channel', {'name': name});
        }
        document.querySelector('#new_channel_name').value = ''
        
        return false;
    }
}

function get_username_and_greet() {
    //get name from form and greet

    document.querySelector('#nameform').onsubmit = () => {
        // set localStorage variable 'name' to whatever is in text input
        localStorage.setItem('name', document.querySelector('#InputName').value);
        //hide the form
        document.querySelector('#nameform').hidden = true
        document.querySelector('#content ').hidden = false  
        //if user is known, greet him
        greet()
        // Stop form from submitting
        return false;
    };
}

function send_chat_message(socket) {

    document.querySelector('#text_form').onsubmit = () => {
        // set localStorage variable 'name' to whatever is in text input
        //
        inp = document.querySelector('#text_input')
        let text = inp.value
        let name = localStorage.getItem('name')
        if (text){
            socket.emit('new message', {'name': name, 'text':text});
        }        
        inp.value = ''
        return false;
    };
}

function create_chan(d){
    
}

//////////////////////////////
// on page load
document.addEventListener('DOMContentLoaded', () => {
    get_username_and_greet()
    // show the form if user is unknown
    if (!localStorage.getItem('name')) {
        document.querySelector('#nameform').hidden = false  
        document.querySelector('#content ').hidden = true  
    } else {
        greet()
    }

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    socket.on('connect', () => {
        socket.emit('get_chans');
    })

    socket.on('channel list', data => {
        document.querySelector('#channel_list').innerHTML = ''
        for (d in data){
            const a = document.createElement('a');
            a.className = 'list-group-item list-group-item-action';
            a.setAttribute("data-toggle", "list");
            a.setAttribute("id", d);
            a.setAttribute("role", "tab");
            a.innerHTML = data[d]
            document.querySelector('#channel_list').append(a)            
        }
        onclick_switch_channel(socket)
    });

    onsubmit_add_channel(socket)
    send_chat_message(socket)

    socket.on('history', data => {
        lst = document.querySelector('#messages')
        for (m in data[1]){
            const a = document.createElement('li');
            a.innerHTML = m
            lst.append(a)
        }
        
    })
    

});

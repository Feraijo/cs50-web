function greet(){
    //greet user with name from localStorage

    document.querySelector('#greeting').innerHTML = `Hello, ${localStorage.getItem('name')}`
}

function add_single_msg(id, s, socket, callback){  
    chat = document.querySelector('.msg_history')  
    if (chat.id === id){
        let inc_msg = add_msg_to_html(s);
        if (!inc_msg){
            l = chat.children.length;
            c = chat.children[l-1]
            callback(c, socket);
        }
    }
}   

function add_post_events(ch, socket){    
    ch.addEventListener('mouseover', () => { 
        ch.querySelector('.hide').style.opacity = '1'
    })
    ch.addEventListener('mouseout', () => { 
        ch.querySelector('.hide').style.opacity = '0'
    })  
    ch.querySelector('.hide').addEventListener('click', () => {
        ch.style.animationPlayState = 'running';
        ch.addEventListener('animationend', () =>  {
            ch.remove();
        });                    
        chat_id = document.querySelector('.msg_history').id
        msg_id = ch.querySelector("p").id
        socket.emit('remove msg', {'chat_id': chat_id, 'msg_id':msg_id});                    
    })    
}

function add_msg_to_html(js){
    //adding message to chat
    //example: {"user": "Eli", "text": "sdfsdf 0", "timestamp": "25-01-2020 16:45"}
    var s = JSON.parse(js);    
    timestamp = s.timestamp
    if (s.user === localStorage.getItem('name'))
        inc = false
    else
        inc = true
    var body = document.querySelector(".msg_history");
    type = inc ? "inc_msg" : "out_msg"
    
    var template = document.querySelector(`#${type}`);
    var clone = template.content.cloneNode(true);
    if (inc)
        clone.querySelector(".username").innerHTML = s.user
    clone.querySelector("p").id = s.id
    clone.querySelector("p").innerHTML = s.text
    
    clone.querySelector(".time_date").innerHTML = timestamp
    
    body.appendChild(clone)
    body.scrollTo(0, body.scrollHeight);    
    return inc
}

function submit_message(socket){
    inp = document.querySelector('#text_input')
    let text = inp.value
    if (text){
        let name = localStorage.getItem('name')
        timestamp = new Date().toLocaleString()
        id = document.querySelector('.msg_history').id           
        
        socket.emit('new message', {'name': name, 'text':text, 'timestamp':timestamp, 'id':id});
    }        
    inp.value = ''
    return false;
}

function set_channel_active(item, socket){
    item.className = item.className + " active_chat"
    cont = document.querySelector('#content')
    cont.hidden = false
    document.querySelector('.msg_history').id = item.id
    socket.emit('load_history', {'id': item.id});
}



//////////////////////////////
// on page load
document.addEventListener('DOMContentLoaded', () => {
    
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

    // show the form if user is unknown
    if (!localStorage.getItem('name')) {
        document.querySelector('#nameform').hidden = false  
        //document.querySelector('#content ').hidden = true  
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
            const content = document.createElement('h6');
            content.innerHTML = data[d];
            const div = document.createElement('div');
            div.setAttribute("id", d);
            div.className = "chat_list"
            div.append(content); 

            document.querySelector('#channel_list').append(div);   
                 
        }

        let def_ch = document.querySelector('#channel_list :not(.active_chat)')
        var a_class = def_ch.className        
        document.querySelectorAll('#channel_list div').forEach(item => {
            item.onclick = function(){
                document.querySelectorAll('#channel_list div').forEach(inner => {
                    inner.className = a_class
                });
                localStorage.setItem('chan', item.id)
                set_channel_active(item, socket)
                
            };
        })

        if (localStorage.getItem('chan')){
            ch = document.querySelector(`#${localStorage.getItem('chan')}`)
            set_channel_active(ch, socket)
        }
    });

    document.querySelector('#add_channel').onsubmit = () => {
        const name = document.querySelector('#new_channel_name').value
        if (name){
            socket.emit('add channel', {'name': name});
        }
        document.querySelector('#new_channel_name').value = ''
        return false;
    }

    

    document.querySelector('.msg_send_btn').addEventListener('click', () => {
        submit_message(socket)})
    document.querySelector('#text_input').addEventListener('keypress', (e) => {
        if (e.keyCode === 13)
            submit_message(socket)})
    
    socket.on('history', data => {
        msgs = document.querySelector(".msg_history")
        msgs.innerHTML = ''        
        for (m in data){
            add_msg_to_html(data[m])
        }  
        
        children = Array.from(msgs.children);
        children.forEach((ch) => {
            if (ch.className === 'outgoing_msg'){
                add_post_events(ch, socket)
            } 
        })
    })
    
    socket.on('chat', data =>{
        add_single_msg(data[0], data[1], socket, add_post_events);
    })


    socket.on('deleted msg', data =>{
        if (document.querySelector('.msg_history').id === data[0]){            
            document.querySelector(`#${data[1]}`).parentElement.parentElement.remove()
        }        
    })

});

// on page load
document.addEventListener('DOMContentLoaded', () => {

    let a_class = document.querySelector('#ch0').className    
    document.querySelector('#ch0').className = a_class + " active"

    // switch active channel
    document.querySelectorAll('#channel_list a').forEach(item => {
        item.onclick = function(){
            document.querySelectorAll('#channel_list a').forEach(inner => {
                inner.className = a_class
            });
            item.className = item.className + " active"

            //document.querySelector(`#${item.id}_content`).className = cont_class + " active"
            //alert(item.id)
        };
    }) 
    
    
   

    function greet(){
        document.querySelector('#greeting').innerHTML = `Hello, ${localStorage.getItem('name')}`
    }

    // show the form if user is unknown
    if (!localStorage.getItem('name')) {
        document.querySelector('#nameform').hidden = false        
    } else 
        greet()
    

    document.querySelector('#nameform').onsubmit = () => {
        // set localStorage variable 'name' to whatever is in text input
        localStorage.setItem('name', document.querySelector('#InputName').value);

        //hide the form
        document.querySelector('#nameform').hidden = true

        //if user is known, greet him
        greet()

        // Stop form from submitting
        return false;
    };

    document.querySelector('#add_channel').onclick = () => {
        alert('click')
    }


    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const selection = button.dataset.vote;
                socket.emit('submit vote', {'selection': selection});
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('vote totals', data => {
        document.querySelector('#yes').innerHTML = data.yes;
        document.querySelector('#no').innerHTML = data.no;
        document.querySelector('#maybe').innerHTML = data.maybe;
    });
});

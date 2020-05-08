document.addEventListener('DOMContentLoaded', () => {
    //alert(`${menu_id}`)
    var keys = []
    document.querySelectorAll('.keys').forEach(x => {
        keys.push(x.id)
    })
    

    //cont = '#content'
    //document.querySelector(cont).innerHTML = '123'
    // document.querySelectorAll('img').forEach(item => {
    //     item.onclick = function() {
    //         const request = new XMLHttpRequest();
    //         s =`/menu/${item.id}`

    //         request.open('GET', s);
    //         request.send();
    //         alert(s)
    // }})
    //query('/menu/Pizza', cont)
})

function query(path, cont){
    const request = new XMLHttpRequest();
    //const currency = document.querySelector('#currency').value;
    request.open('GET', path);

    // Callback function for when request completes
    request.onload = () => {
        //document.querySelector(cont).innerHTML = 'zxczxc';
        alert(request.responseText)
        

        // // Extract JSON data from request
        // const data = JSON.parse(request.responseText);

        // // Update the result div
        // if (data.success) {
            
        //     document.querySelector(cont).innerHTML = 'zxczxc';
        // }
        // else {
        //     document.querySelector(cont).innerHTML = 'qweqwe';
        // }
    }

    // Add data to send with request
    // const data = new FormData();
    // data.append('currency', currency);

    // Send request
    request.send();
    
}
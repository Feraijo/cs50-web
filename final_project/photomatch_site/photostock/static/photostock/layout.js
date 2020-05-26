document.addEventListener('DOMContentLoaded', () => {
    // display current yeat at the footer
    document.querySelector("#year").innerHTML = new Date().getFullYear();
    
    //autohide alerts
    setTimeout(() => {
        $('.alert').alert('close')        
    }, 3500);
    
})
document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('img').forEach(item => {
        item.onclick = function() {
        alert(this.className)
    }})
})
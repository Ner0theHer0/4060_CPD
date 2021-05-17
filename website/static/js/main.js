let s1 = document.getElementById("test")




window.onload = function() {
    s1.onclick = function(){
        document.getElementById("qwe").innerHTML = "Paragraph changed.";
    }
}
// let s1 = document.getElementById("test")



let s1 = document.getElementById("test")

let s2 = document.getElementById("try")

let s3 = document.getElementById("getter")

var img = document.createElement("img");

window.onload = function() {
    s1.onclick = function() {
        img.src = "static/js/img/tmp.jpg"

        var src = document.getElementById("forImg")

        src.appendChild(img)
    }

    s2.onclick = function() {
        // var input = document.createElement('input');
        // input.type = 'file';

        // input.onchange = e => { 
        //     var tmpFile = e.target.files[0];
        //     // Grab the destination URL
        //     $.post( "/upload", {
        //         javascript_data: tmpFile 
        //     });
            
        // }

        // input.click();

        console.log("wow")
    }

    s3.onclick = function() {
        fetch('/upload')
            .then(function (response) {
                return response.json();
            }).then(function (text) {
                document.getElementById("line1").innerHTML = text.names[0] + ": " + text.prob[0];
                document.getElementById("line2").innerHTML = text.names[1] + ": " + text.prob[1];
                document.getElementById("line3").innerHTML = text.names[2] + ": " + text.prob[2];
                document.getElementById("line4").innerHTML = text.names[3] + ": " + text.prob[3];
                document.getElementById("line5").innerHTML = text.names[4] + ": " + text.prob[4];
                console.log('GET response:');
                console.log(text.names[0]); 
            });
    }
}




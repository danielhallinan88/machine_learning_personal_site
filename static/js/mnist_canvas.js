var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;

var x = "black",
    y = 2;

function init() {
    canvas = document.getElementById('can');
    ctx = canvas.getContext("2d");
    w = canvas.width;
    h = canvas.height;

    canvas.addEventListener("mousemove", function (e) {
        findxy('move', e)
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        findxy('down', e)
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        findxy('up', e)
    }, false);
    canvas.addEventListener("mouseout", function (e) {
        findxy('out', e)
    }, false);
}

function color(obj) {
    switch (obj.id) {
        case "green":
            x = "green";
            break;
        case "blue":
            x = "blue";
            break;
        case "red":
            x = "red";
            break;
        case "yellow":
            x = "yellow";
            break;
        case "orange":
            x = "orange";
            break;
        case "black":
            x = "black";
            break;
        case "white":
            x = "white";
            break;
    }
    if (x == "white") y = 14;
    else y = 2;

}

function draw() {
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = x;
    ctx.lineWidth = y;
    ctx.stroke();
    ctx.closePath();
}

function erase() {
    var m = confirm("Want to clear");
    if (m) {
        ctx.clearRect(0, 0, w, h);
        document.getElementById("canvasimg").style.display = "none";
    }
}

const upload = (file) => {

};

function save() {
    document.getElementById("can").style.border = "2px solid";
    var dataURL = canvas.toDataURL('image/jpeg');
    //console.log(dataURL);
    //document.getElementById("can").src = dataURL;
    //document.getElementById("can").style.display = "inline";
    testImage = new Image(28, 28);
    testImage.src = canvas.toDataURL('image/jpeg');
    //document.body.appendChild(testImage);

    //test_digit = new Image();
    //test_digit.src = '../images/test_image_1.jpg'
    //var test_digit = document.getElementById('test_digit').src ;
    //console.log(test_digit);

    //const input = document.getElementById('test_button');
    //console.log("TEST FILE: " + input.files[0]);
    

    document.querySelector('#test_button').addEventListener('change', event => {
      handleImageUpload(event)
    })

    const handleImageUpload = event => {
      const files = event.target.files
      const formData = new FormData()
      formData.append('image', files[0])

      fetch('http://3.19.232.79:8888/mnist', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data)
      })
      .catch(error => {
        console.error(error)
      })
    }

/*
    const options = {
      method: 'PUT',
      body: data,
      //body: testImage,
      //headers: {
      //  'Content-Type' : 'image/jpg'
      //},
    };
    fetch('http://3.19.232.79:8888/mnist', options)
    //fetch('http://3.19.232.79:8888/test')
      .then((response) => {
        return response.json();
      })
      .then((myJson) => {
        console.log(myJson);
      });
*/
}

function findxy(res, e) {
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        currX = e.clientX - canvas.offsetLeft;
        currY = e.clientY - canvas.offsetTop;

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (res == 'up' || res == "out") {
        flag = false;
    }
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
            draw();
        }
    }
}

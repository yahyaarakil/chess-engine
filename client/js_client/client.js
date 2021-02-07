const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
var scale = 1.5;

canvas.setAttribute("width", (400*scale).toString());
canvas.setAttribute("height", (400*scale).toString());

var colors = ['darkgreen', 'lightgrey'];
var color = 0;

function switchColor(){
    color+=1;
    if(color > 1){
        color = 0;
    }
}

for(var i = 0; i < 8; i++){
    for(var j = 0; j < 8; j++){
        switchColor();
        ctx.fillStyle = colors[color];
        ctx.fillRect(i*50*scale, j*50*scale, scale*(i*50+50), scale*(j*50+50));
    }
    switchColor();
}
class Piece{
    Piece(identifier, owner, spriteu, posx, posy){
        this.identifier = identifier;
        this.owner = owner;
        this.spriteu = spriteu;
        this.sprite = new Image();
        this.sprite.src = spriteu;
        this.posx = posx;
        this.posy = posy;

        this.width = 32;
        this.height = 32;
    }
}



// set up
var scale = 1.5;
var initColor = 0;

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left)/(50*scale));
    const y = Math.floor((event.clientY - rect.top)/(50*scale));
}

canvas.addEventListener('mousedown', function(e) {
    getCursorPosition(canvas, e);
})

var rightBar = document.getElementById("rightBar");
//new game button
rightBar.innerHTML += "<button onclick='newGame();'/>New Game"
function newGame(){
    socket.send(ID + " new_game");
}

//join game button
rightBar.innerHTML += "<input id='toJoin' placeholder='ID';'/>"
rightBar.innerHTML += "<button onclick='joinGame();'/>Join Game"
function joinGame(){
    window.alert("joining " + document.getElementById("toJoin").value);
    socket.send(ID + " join_game " + document.getElementById("toJoin").value);
}

//status text
rightBar.innerHTML += "<p id='id'>ID: </p>"
var idText = document.getElementById("id");

let socket = new WebSocket("ws:/localhost:5000");

socket.onopen = function(e) {
    socket.send("new_connection");
};

var ID = "";
var status = "connecting";
var game_stat = 0;
var pieces = [];

function setStatus(newStatus){
    status = newStatus;
    idText.innerHTML = "ID: "+ID+"<br/>Status: "+newStatus;
}

function setupGame(welcome){
    pieces = [];
    welcome = welcome.split('>');
    initColor = parseInt(welcome[welcome.length-1]);
    for(var i = 0; i < welcome.length-1; i++){
        if(i == 0){
            continue;
        }
        var piece = welcome[i].split(',');
        var pieceObj = new Piece(parseInt(piece[2]), piece[1], "/Users/yahyaarakil/Desktop/chessGine/client/js_client/sprites/"+piece[1]+"/"+piece[0]+".png", parseInt(piece[3]), parseInt(piece[4]));
        pieces.push(pieceObj);
    }
    pieces.shift();
    resizeCanvas();
}

socket.onmessage = function(event) {
    console.log(`[message] Data received from server: ${event.data}`);
    message = event.data.toString().split(' ')
    if(message[0] == "id:"){
        ID = message[1];
        console.log(message[1]);
        setStatus("Connected");
    }
    else if(message[0] == "status:"){
        setStatus(message[1]);
        if(status=="in_game" && game_stat==0){
            socket.send(ID+" welcome_me");
            game_stat++;
        }
    }
    else if(message[0]=="welcome"){
        pieces = setupGame(message[1], pieces);
    }
    return false;
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    setStatus("Disconnected");
  }
};

// Event handler to resize the canvas when the document view is changed
window.addEventListener('resize', resizeCanvas, false);
resizeCanvas();

function resizeCanvas() {
    scale = window.innerHeight/450;

    // Redraw everything after resizing the window
    renderBoard(canvas, ctx, initColor);
    drawPieces(canvas, ctx, initColor);
}

function drawPieces(canvas, ctx, side = 0,){
    function rotate(pos){
        x = 7-pos[0];
        y = 7-pos[1];
        return [x, y];
    }

    for(var i = 0; i < pieces.length; i ++){
        piece = pieces[i];
        pos = [piece.posx, piece.posy];
        if(side == 1){
            pos = rotate(pos);
        }
        window.alert(piece.spriteu);
        ctx.drawImage(piece.sprite, pos[0]*50*scale, pos[1]*50*scale);
    }
}

function renderBoard(canvas, ctx, firstColor = 1){
    canvas.setAttribute("width", (400*scale).toString());
    canvas.setAttribute("height", (400*scale).toString());
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var colors = ['darkgreen', 'lightgrey'];
    var color = firstColor;

    var offsetx = 0;
    var offsety = 0;

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
            ctx.fillRect(j*50*scale + offsetx, i*50*scale + offsety, scale*(j*50+50) + offsetx, scale*(i*50+50) + offsety);
        }
        switchColor();
    }
}
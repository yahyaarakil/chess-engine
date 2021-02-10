class Piece{
    constructor(identifier, owner, spriteu, posx, posy){
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
    var x = Math.floor((event.clientX - rect.left)/(50*scale));
    var y = Math.floor((event.clientY - rect.top)/(50*scale));
    return [x, y];
}

canvas.addEventListener('mousedown', function(e) {
    var pos = getCursorPosition(canvas, e);
    if(myTurn){
        interface(pos);
    }
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
var piecesArr = [];
var myTurn = false;

function setStatus(newStatus){
    status = newStatus;
    idText.innerHTML = "ID: "+ID+"<br/>Status: "+newStatus;
}

function inter_pieces(welcome){
    piecesArr = [];
    welcome = welcome.split('>');
    for(var i = 1; i < welcome.length-2; i++){
        if(i == 0){
            continue;
        }
        var piece = welcome[i].split(',');
        var pieceObj = new Piece(parseInt(piece[2]), piece[1], "/Users/yahyaarakil/Desktop/chessGine/client/js_client/sprites/"+piece[1]+"/"+piece[0]+".png", parseInt(piece[3]), parseInt(piece[4]));
        piecesArr.push(pieceObj);
    }
}

function updateGame(message){
    inter_pieces(message);
    if(parseInt(message[message.length-1]) == initColor){
        myTurn = true;
    }else{
        myTurn = false;
    }
}

function setupGame(welcome){
    var welcomecut = welcome.split('>');
    window.alert("setting up game");
    initColor = parseInt(welcomecut[welcomecut.length-2]);
    updateGame(welcome);
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
        setupGame(message[1]);
    }
    else if(message[0]=="game_update"){
        updateGame(message[1]);
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

function resizeCanvas() {
    scale = window.innerHeight/450;

    // Redraw everything after resizing the window
    renderBoard(canvas, ctx, initColor);
    drawPieces(canvas, ctx, initColor);
}

function drawPieces(canvas, ctx, side = 0){
    var offset = 0.05 * scale;
    var size = 32 * scale * 1.5;
    function rotate(pos){
        x = 7-pos[0];
        y = 7-pos[1];
        return [x, y];
    }

    for(var i = 0; i < piecesArr.length; i ++){
        piece = piecesArr[i];
        pos = [piece.posx, piece.posy];
        if(side == 1){
            pos = rotate(pos);
        }
        ctx.drawImage(piece.sprite, pos[0]*50*scale + offset, pos[1]*50*scale + offset, size, size);
    }
}

function renderBoard(canvas, ctx, firstColor = 1){
    canvas.setAttribute("width", (400*scale).toString());
    canvas.setAttribute("height", (400*scale).toString());
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var colors = ['rgb(208, 139, 78)', 'rgb(254, 206, 161)'];
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
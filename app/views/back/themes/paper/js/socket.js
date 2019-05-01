//var wsUri = "ws://127.0.0.1/ws"; 
var wsUri = "ws://socket.mysitio.cl:8000/ws";
var wsUri_start = "http://socket.mysitio.cl/";
var intento = 0;
websocket = null;

function websocket_start() {
    if (window.WebSocket !== undefined) {
        websocket = new WebSocket(wsUri);
        websocket.onopen = function(evt) {
            onOpen(evt)
        };
        websocket.onclose = function(evt) {
            onClose(evt)
        };
        websocket.onmessage = function(evt) {
            onMessage(evt)
        };
        websocket.onerror = function(evt) {
            onError(evt)
        };
    } else {
        console.log("sockets not supported");
    }
}


function websocket_stop() {
    if (websocket != null) {
        websocket.close();
    }
}

function onOpen(evt) {
    console.log("Log conectado");
}

function onClose(evt) {
    console.log("Log desconectado");
    websocket == null;
}

function onMessage(evt) {
    // There are two types of messages: 
    // 1. a chat participant message itself 
    // 2. a message with a number of connected chat participants 
    var message = evt.data;
    if (message.startsWith("log:")) {
        message = message.slice("log:".length);
    } else if (message.startsWith("connected:")) {
        message = message.slice("connected:".length);
    }

    if (message.indexOf("{") != -1) {
        message = message.slice(message.indexOf("{"));
        try {
            data = JSON.parse(message)
            if (data.porcentaje) {
                barra(data.porcentaje);
            }
            if (data.mensaje) {
                message = data.mensaje;
            }
        } catch (error) {}
    }else{
        console.log(message);
    }
    notificacion_footer(message);
}

function onError(evt) {
    websocket == null;
    notificacion_footer("Error al conectar log");
    if (intento < 3) {
        intento++;
        $.ajax({
            url: wsUri_start,
            timeout: 500,
            complete: function(data) {
                websocket_start();
            }
        });
    }
}

function addMessage(message) {
    websocket.send(message);
    notificacion_footer(message);
}
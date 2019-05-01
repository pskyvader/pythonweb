//var wsUri = "ws://127.0.0.1/ws";
var wsUri = "ws://socket.mysitio.cl:8000/ws";
var wsUri_start = "http://socket.mysitio.cl/";
var intento = 0;

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

function onOpen(evt) {
    notificacion_footer("Log conectado");
}

function onClose(evt) {
    notificacion_footer("Log desconectado");
}

function onMessage(evt) {
    // There are two types of messages:
    // 1. a chat participant message itself
    // 2. a message with a number of connected chat participants
    var message = evt.data;

    if (message.startsWith("log:")) {
        message = message.slice("log:".length);
        notificacion_footer(message);
    } else if (message.startsWith("connected:")) {
        message = message.slice("connected:".length);
        notificacion_footer(message);
    }
}

function onError(evt) {
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
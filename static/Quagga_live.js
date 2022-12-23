// This is the code for the barcode scanner
$(function () {
    var App = {
        init: function () {
            var self = this;

            Quagga.init(this.state, function (err) {
                if (err) {
                    return self.handleError(err);
                }
                //self.setState(ean_reader,value)
                Quagga.start();
            });
        },

        handleError: function (err) {
            console.log(err);
        },

        state: {
            inputStream: {
                type: "LiveStream",
                target: document.querySelector('#live_scanner'),
                // constraints: {
                //     width: {min: 100},
                //     height: {min: 200},
                //     facingMode: "environment",
                //     aspectRatio: { min: 1, max: 2 }
                // }
            },
            locator: {
                patchSize: "medium",
                halfSample: true
            },
            numOfWorkers: 2,
            frequency: 10,
            decoder: {
                readers: ['ean_reader']
            },
            locate: true
        },
        lastResult: null
    };

    App.init();

    Quagga.onProcessed(function (result) {
        var drawingCtx = Quagga.canvas.ctx.overlay,
            drawingCanvas = Quagga.canvas.dom.overlay;

        if (result) {
            if (result.boxes) {
                drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
                result.boxes.filter(function (box) {
                    return box !== result.box;
                }).forEach(function (box) {
                    Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, { color: "green", lineWidth: 2 });
                });
            }

            if (result.box) {
                Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, { color: "#00F", lineWidth: 2 });
            }

            if (result.codeResult && result.codeResult.code) {
                Quagga.ImageDebug.drawPath(result.line, { x: 'x', y: 'y' }, drawingCtx, { color: 'red', lineWidth: 3 });
            }
        }
    });

    Quagga.onDetected(function (result) {
        var code = result.codeResult.code;
        console.log('Barcode Scanned', code);
        document.getElementById('barcode_search').value = code;
        BarcodeLookup();
    });
});
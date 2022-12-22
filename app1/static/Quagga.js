document.getElementById('start-button').addEventListener('click', function () {
    Quagga.init({
        inputStream: {
            type: 'LiveStream',
            constraints: {
                width: 640,
                height: 480,
                facingMode: "environment",
            },
        },
        decoder: {
            readers: [{
                format: "ean_reader",
                config: {
                    supplements: [
                        'ean_5_reader', 'ean_2_reader'
                    ]
                }
            }],
            debug: {
                drawBoundingBox: true,
                showFrequency: true,
                drawScanline: true,
                showPattern: true
            },
            // multiple: false,
        },
        locate: true,
        halfSample: false,
        patchSize: "medium",
        numOfWorkers: 4,
        frequency: 10,

    }, function (err) {
        if (err) {
            console.error(err);
            return;
        }
        console.log('Initialization finished. Ready to start');
        Quagga.start();
    });

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
        console.log(result.codeResult.code);
        Quagga.stop();
        BarcodeLookup(result.codeResult.code);
    });
});
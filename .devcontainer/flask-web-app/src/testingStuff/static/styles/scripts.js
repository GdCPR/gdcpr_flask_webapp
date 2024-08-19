function openNav() {
  document.getElementById("myMenu").style.width = "100%";
  console.log("Menu opened")
}

function closeNav() {
  document.getElementById("myMenu").style.width = "0";
  console.log("Menu closed")
}

// start map zoom-pan
var transformMatrix = [1, 0, 0, 1, 0, 0];
var svg = document.getElementById('map');
var viewbox = svg.getAttributeNS(null, "viewBox").split(" ");
var centerX = parseFloat(viewbox[2]) / 2;
var centerY = parseFloat(viewbox[3]) / 2;
var matrixGroup = svg.getElementById("matrix-group");

function pan(dx, dy) {
    transformMatrix[4] += dx;
    transformMatrix[5] += dy;
    var newMatrix = "matrix(" +  transformMatrix.join(' ') + ")";
    matrixGroup.setAttributeNS(null, "transform", newMatrix);
    logMessage = 
    `
    Panning function:
    svg with transform:${newMatrix}
    `;
    console.log(logMessage);
}

function zoom(scale) {
    for (var i = 0; i < transformMatrix.length; i++) {
        transformMatrix[i] *= scale;
    }

    transformMatrix[4] += (1 - scale) * centerX;
    transformMatrix[5] += (1 - scale) * centerY;

    var newMatrix = "matrix(" +  transformMatrix.join(' ') + ")";
    matrixGroup.setAttributeNS(null, "transform", newMatrix);
    logMessage = 
    `
    Zoom function:
    svg with transform:${newMatrix}
    `;
    console.log(logMessage)
}

function home() {
  transformMatrix = [1, 0, 0, 1, 0, 0];
  var newMatrix = "matrix(" +  transformMatrix.join(' ') + ")";
  matrixGroup.setAttributeNS(null, "transform", newMatrix);
  logMessage = 
  `
  Home function:
  svg with transform:${newMatrix}
  `;
  console.log(logMessage)
}
// end map zoom-pan

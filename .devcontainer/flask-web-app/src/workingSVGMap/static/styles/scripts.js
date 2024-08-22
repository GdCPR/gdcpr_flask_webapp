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


// Functions from library: https://github.com/anvaka/panzoom
var instance = panzoom(document.getElementById('matrix-group'));

instance.on('panstart', function(e) {
  console.log('Fired when pan is just started ', e);
  // Note: e === instance.
});

instance.on('pan', function(e) {
  console.log('Fired when the scene is being panned', e);
});

instance.on('panend', function(e) {
  console.log('Fired when pan ended', e);
});

instance.on('zoom', function(e) {
  console.log('Fired when scene is zoomed', e);
});

instance.on('transform', function(e) {
  // This event will be called along with events above.
  console.log('Fired when any transformation has happened', e);
});

// The zoomming panning library requires the element being absolute positioned
// To fix the elements below to the refular dom flow, I have insert a blank element
// below the absolute positioned one and use the lines below to get the absolute positioned
// elemet height and make the blank element this height to force the other elements follow
// through
// Solution from: https://stackoverflow.com/a/55418299
// Some changes added from original solution to work with my DOM structure
let absoluteDivHeight = document.getElementsByTagName("svg")[0].height.animVal.value;
let blankDiv = document.getElementsByClassName("blankDiv")[0];

blankDiv.style.height = absoluteDivHeight - 20 + "px";
blankDiv.style.width = "0px";

let containerMapInfo = document.getElementsByClassName("container-map-info")[0];
document.addEventListener('DOMContentLoaded', function() {
  // Show the element
  containerMapInfo.style.display = "block";
});
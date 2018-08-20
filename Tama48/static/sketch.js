// GUI MAIN CODE
// FLASK integration: https://github.com/shiffman/NOC-S17-2-Intelligence-Learning

var amazingAlgorithm; // alg selection radio input
var submitButton;
var score = 0;
var scores = [1, 0.5, 1, 1, 0.25]; // init values
var satisfaction; // element
var algscore; // element
// find colors on http://www.december.com/html/spec/colorsvg.html
var functionalityColors = {"residential":"pink" ,
                        "clinic":"blue" ,
                        "community_center":"green",
                        "elderly_center":"crimson",
                        "high_school":"purple",
                        "hospital":"orange",
                        "kindergarden":"tomato",
                        "mikve":"tan",
                        "police":"dodgerblue",
                        "primary_school":"silver",
                        "sport":"magenta",
                        "synagogue":"mediumturquoise",
                       };
var easycam;
var gui;
// alg parameters
var unitsToAdd = 300;
// var KforGenetic = 8; // rename population
// var iterationsOfAlgorithm = 5;
// var mutationProbability = 0.5;

function setup() {
  var canvas = createCanvas(windowWidth,windowHeight-300,WEBGL);
  canvas.parent('sketch-holder');

  // update init buildings, note it's a static file!
  loadJSON('INITdata.json',updateData); // async, load data, when you are done, tell me(callback) and put it in var

  //initiate camera
  easycam = createEasyCam();
  var initState = {
    distance: 500,
    center  : [windowHeight/3, 0, windowWidth/3], // x place is y, z place is x
    rotation: [0.2686100362577888, 0.780483875898701, -0.2814650231707926, -0.48935775115471325],
  };
  easycam.setState(initState);

  // P5 GUI sliders:

  var gui = createGui(' ');
  sliderRange(0, 10000, 10); // (min, max, step) , init is in var init
  gui.addGlobals('unitsToAdd');
  // sliderRange(8, 64, 1);
  // gui.addGlobals('KforGenetic');
  // sliderRange(1, 50, 1);
  // gui.addGlobals('iterationsOfAlgorithm');
  // sliderRange(0.01, 0.9, 0.01);
  // gui.addGlobals('mutationProbability');

  // DOM GUI elements:

  // radio input
  amazingAlgorithm = createRadio('alg');
  amazingAlgorithm.parent('sketch-holder');
  amazingAlgorithm.option("genetic");
  amazingAlgorithm.option("minconflict");
  amazingAlgorithm.style('margin-left','40px');
  amazingAlgorithm.style('margin-bottom','10px');

  // show score
  algscore = createElement("algscore", "current score: "+score).style('margin-left','40px');
  algscore.parent(amazingAlgorithm);
  algscore.hide(); // stay hidden until code run

  // alg parameters in dom
  // createElement("inUnitsToAdd","units to add").style('margin-left','40px'); // here we move the title, in the html we move the box
  // inUnitsToAdd = createSlider(0, 100000, 100);
  // createInput('');

  // Submit button
  var runButton = createButton('run TAMA48');
  runButton.parent('sketch-holder');
  runButton.style('margin-left','40px');
  runButton.style('margin-right','30px');
  // runButton.style('margin-top','10px');
  runButton.mousePressed(submit);

  // MIKRA - color legend
  for(var key in functionalityColors) {
    var value = functionalityColors[key];
    var m = createElement("mik",key);
    m.parent('sketch-holder');
    m.style('background-color',value);
    m.style('margin-right','5px');
  }
  createDiv("<br>").parent('sketch-holder');

  // user satisfaction scores
  satisfaction = createElement("uss","user satisfaction scores:");
  satisfaction.parent('sketch-holder');
  satisfaction.hide(); // stay hidden until code run
  createElement("uss","secular child "+scores[0]).parent(satisfaction);
  createElement("uss","secular single "+scores[1]).parent(satisfaction);
  createElement("uss","religious single "+scores[2]).parent(satisfaction);
  createElement("uss","secular parent "+scores[3]).parent(satisfaction);
  createElement("uss","religious elderly "+scores[4]).parent(satisfaction);

  // var sec_child = 0; // id = 0
  // var sec_single = 0; // id = 1
  // var rel_single = 0; // id = 2
  // var sec_parent = 0; // id = 3
  // var rel_elder = 0; // id = 4

  createDiv("<br>").parent('sketch-holder');
}

// Send data to python Flask server
function submit() {
  var dataToPost = {
    alg: amazingAlgorithm.value(),
    units: unitsToAdd,
    // mut: mutationProbability.value(),
    // k: KforGenetic.value(),
    // it:iterationsOfAlgorithm.value(),
  }
  console.log(dataToPost);
  httpPost('/upload','json',dataToPost, success, error); // post call
}

// Reply back from flask server
function success(data) {
  console.log(data);
  // TODO updated building data
  loadJSON('data.json',updateData);
  //TODO update score in dom
  // score = ;
  // algscore.value(score);

  // update user scores - happens with updateData? TODO
  satisfaction.show();
  algscore.show();
  algscore.style("display", "inline-block");
}

function error(reply) {
 console.log(reply);
}

function draw(){
  background(0);
  ambientLight(255, 255, 255);
  for (var b = 0 ; b < buildingsToBuild.length ; b++){
    buildingsToBuild[b].constructBuilding();
  }
  //TODO update score in dom
  // algscore.value(score);

}

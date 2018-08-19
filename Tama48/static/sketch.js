// GUI MAIN CODE
// FLASK integration: https://github.com/shiffman/NOC-S17-2-Intelligence-Learning

var amazingAlgorithm; // alg selection radio input
var submitButton;
// find colors on http://www.december.com/html/spec/colorsvg.html
var functionalityColors = {"residential":"pink" ,
                        "clinic":"blue" ,
                        "community_center":"green",
                        "elderly_center":"crimson",
                        "high_school":"purple",
                        "hospital":"orange",
                        "kindergarden":"yellow",
                        "mikve":"snow",
                        "police":"dodgerblue",
                        "primary_school":"",
                        "sport":"magenta",
                        "synagogue":"mediumturquoise",
                       };
var easycam;
var gui;
var unitsToAdd = 300;
var KforGenetic = 8;
var iterationsOfAlgorithm = 5;
var mutationProbability = 0.5;

function setup() {
  createCanvas(windowWidth,windowHeight-150,WEBGL);

  // update init buildings, note it's a static file!
  loadJSON('INITdata.json',updateData); // async, load data, when you are done, tell me(callback) and put it in var

  //initiate camera
  easycam = createEasyCam();
  var initState = {
    distance: 800,
    center  : [windowHeight/3, 0, windowWidth/3], // x place is y, z place is x
    rotation: [0.31224481585400304, 0.7361780896684853, -0.22704505805832742, -0.5558736698888078],
  };
  easycam.setState(initState);

  // P5 GUI sliders:

  var gui = createGui('select parameters');
  sliderRange(0, 10000, 10); // (min, max, step) , init is in var init
  gui.addGlobals('unitsToAdd');
  sliderRange(8, 64, 1);
  gui.addGlobals('KforGenetic');
  sliderRange(1, 50, 1);
  gui.addGlobals('iterationsOfAlgorithm');
  sliderRange(0.01, 0.9, 0.01);
  gui.addGlobals('mutationProbability');

  // DOM GUI elements:

  // radio input
  amazingAlgorithm = createRadio('alg');
  amazingAlgorithm.option("genetic");
  amazingAlgorithm.option("minconflict");
  amazingAlgorithm.style('margin-left','40px');
  amazingAlgorithm.style('margin-bottom','10px');
  amazingAlgorithm.style('padding','0px');

  // createDiv(" ");
  //
  // // alg parameters
  // createElement("inUnitsToAdd","units to add").style('margin-left','40px'); // here we move the title, in the html we move the box
  // inUnitsToAdd = createSlider(0, 100000, 100);
  // //createInput('');
  // createElement("inK","choose K for genetic").style('margin-left','30px');
  // var inK = createInput('');
  // createElement("inIter","choose number of iterations for genetic").style('margin-left','30px');
  // var inIter = createInput('');

  createDiv(" ");

  // Submit button
  var runButton = createButton('run TAMA48');
  runButton.style('margin-left','40px');
  runButton.style('margin-top','10px');
  runButton.mousePressed(submit);

}

  // Send data to python Flask server
  function submit() {
    var dataToPost = {
      alg: amazingAlgorithm.value(),
      units: unitsToAdd.value(),
      mut: mutationProbability.value(),
      k: KforGenetic.value(),
      it:iterationsOfAlgorithm.value(),
    }
    console.log(dataToPost);
    httpPost('/upload','json',dataToPost, success, error); // post call
  }

  // Reply back from flask server
  function success(data) {
    console.log(data);
    // TODO updated building data
    loadJSON('data.json',updateData);
    //TODO show score in dom?
  }

  function error(reply) {
   console.log(reply);
 }


function draw(){
  background(0);
  ambientLight(255, 255, 255);
  for (var b = 0 ; b < buildingsToBuild.length ; b++){
    // for (var a = 0 ; a < 2 ; a++){
    buildingsToBuild[b].constructBuilding();
    //
  }
  // createElement("inUnitsToAdd", inUnitsToAdd.value()).style('margin-left','40px'); // here we move the title, in the html we move the box

}

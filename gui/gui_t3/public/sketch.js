// view control : super intuitive, scroll for zoom
// used libraries:


// ********************* TEMP VALS
var socket;
dim = 50;
currcolor = 255;
buildingsInBlock = 1;
var thisIsASlider = -20;



// ********************* VARIABLES
sectionsInBuilding = 2; // each building has a old and new section
groundLevel = 0;
var functionalityColors = {"residential":"pink"};
var amazingAlgorithm = ['genetic', 'minconflict'];


var gui;
var easycam;

//TODO show score

function setup() {
  createCanvas(windowWidth,windowHeight,WEBGL);

  // GUI
  gui = createGui('TAMA48');
  gui.addGlobals('thisIsASlider','amazingAlgorithm'); //gui params

  // TODO amazingAlgorithm should call the python with right input and recalc from data;

  // client side
  socket = io.connect('http://localhost:3000');

  //camera
  easycam = createEasyCam();
  var initState = {
    distance: 1000,
    center  : [0, 0, 0],
    rotation: [0.9665546209855814,
               -0.1827328716755022,
               -0.1628566031987059,
               0.07654142052001892],
  };
  easycam.setState(initState);
}


function draw() {
  // background and lighting
  background(0);
  ambientLight(255, 255, 255);

  // what alg?
  switch(amazingAlgorithm) {
		  case 'genetic':
        ambientMaterial("green");
        box(); // data = genetic
		    break;

		  case 'minconflict':
        ambientMaterial("blue");
		    sphere(); // data = minconf
		    break;
    }


	// TODO :

  	var buildings = [];
    for (var j=0 ; j<buildingsInBlock ; j++){
  		var sections = [];
  		for (var i=0 ; i < sectionsInBuilding ; i++){ // create building with old and new sections
  			sections.push(new Section(dim,dim,dim));
  		}
      var ax = j*(dim*400);//%(dim*4.4);
      var ay = groundLevel;
      var az = j*10;//%3*(dim*10);
      var a = new Building(ax,ay,az,sections,'residential').constructBuilding();//.constructBuilding();
      buildings.push(a);
  	}
}


// ********************* CLASSES

class Section {
	constructor(w,h,d){
		this.w = w;
		this.h = dim;//h;
		this.d = d;
	}

  constructSection(){
    // box(this.w, this.h, this.d);
    beginShape();
    //ground shape
    vertex(0, groundLevel, 0);
    vertex(80, groundLevel, 0);
    vertex(80, groundLevel, 50);
    vertex(40, groundLevel, 50);
    vertex(40, groundLevel, 90);
    vertex(0, groundLevel, 90);
    //wall
    vertex(0, groundLevel, 0);
    vertex(0, this.h, 0);
    vertex(0, this.h, 90);
    vertex(0, groundLevel, 90);
    //wall
    vertex(0, groundLevel, 90);
    vertex(40, groundLevel, 90);
    vertex(40, this.h, 90);
    vertex(0, this.h, 90);
    //topshape - reverse order
    vertex(0, this.h, 90);
    vertex(40, this.h, 90);
    vertex(40, this.h, 50);
    vertex(80, this.h, 50);
    vertex(80, this.h, 0);
    vertex(0, this.h, 0);
    //wall
    vertex(0, this.h, 0);
    vertex(80, this.h, 0);
    vertex(80, groundLevel, 0);
    vertex(0, groundLevel, 0);
    //wall
    vertex(80, groundLevel, 0);
    vertex(80, this.h, 0);
    vertex(80, this.h, 50);
    vertex(80, groundLevel, 50);
    endShape(); // note: not "closed"
  }

	getHeight(){
		return this.h;
	}
}

class Building {
	constructor(x,y,z,sections,functionality) { //sections is an array
		this.x = x;
		this.y = y;
		this.z = z;
		this.sections = sections;
		this.func = functionality;
		this.funcColor = 255; // init on white for debugging
	}

	setfuncColor(){
		this.funcColor = color(functionalityColors[this.func]);
	}

	constructBuilding(){
		this.setfuncColor();
		push();
		translate(this.x,this.y,this.z);
		for (var s = 0 ; s < this.sections.length ; s++){
			push();
			if (s){ // new section has index 1
        noFill();
				stroke(this.funcColor);
				translate(0,-this.sections[s-1].getHeight(),0); // place on the top of the old section
			}
			else {
        // stroke(0);
        ambientMaterial(this.funcColor); // change from framework to fill
			}
			this.sections[s].constructSection();
			pop();
		}
		pop();
	}
}

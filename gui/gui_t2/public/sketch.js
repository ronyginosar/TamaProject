// ********************* TEMP VALS
var socket;
dim = 50;
// loc = ;
currcolor = 255;
buildingsInBlock = 9;
blocksInCity = 2;
yRotation = -37;
xRotation = -25;
zRotation = 23;
var thisIsASlider = -20;
var amazingAlgorithm = ['genetic', 'minconflict'];


// ********************* VARIABLES
sectionsInBuilding = 2; // each building has a old and new section
groundLevel = 0;
var functionalityColors = {"residential":"pink"};
var zoom = 0;
var gui;

//TODO show score


// extract_GIS_data: building, x,y, init height, functionalityColors
// from code: additional height, w,d , alg score toogle button alg
// calc in code or json? call funcions or parse?



function setup() {
  createCanvas(windowWidth,windowHeight,WEBGL);
  var fov = 60 / 180 * PI; //Number: camera frustum vertical field of view, from bottom to top of view, in angleMode units
  var cameraZ = height / 2.0 / tan(fov / 2.0);
  // perspective(60 / 180 * PI, width / height, cameraZ * 0.1, cameraZ * 10);
  perspective(60 / 180 * PI, width / height, cameraZ * 0.1, cameraZ*10);

  // GUI
  gui = createGui('TAMA48');
  gui.addGlobals('thisIsASlider','xRotation','yRotation','zRotation','amazingAlgorithm');

  // client side
  socket = io.connect('http://localhost:3000');
  // socket.on('block', newData); // and make another function
}

// function newDraw(){} // basically copy draw()

function draw() {
  // orbitControl();
  background(0);
  ambientLight(255, 255, 255);
	//TODO perspective(fovy,aspect,near,far)
	//TODO move with arrows? or scrolling?
  rotateY(radians(yRotation));
	rotateX(radians(xRotation));
  rotateZ(radians(zRotation));



	// TODO 1. read dummy from file 2. read whole array from file
  var blocks = [];

  for (var b=0 ; b<blocksInCity ; b++){
  	var buildings = [];

    for (var j=0 ; j<buildingsInBlock ; j++){
  		var sections = [];
  		for (var i=0 ; i < sectionsInBuilding ; i++){ // create building with old and new sections
  			sections.push(new Section(dim,dim,dim));
  		}

  		// b1 = new Building(0,groundLevel,0,sections);
  		// b1.constructBuilding();
  		//
  		// b2 = new Building(120,groundLevel,0,sections);
  		// b2.constructBuilding();
      var ax = j*(dim*1.1)%(dim*4.4);
      var ay = groundLevel;
      var az = j%3*(dim*1.1);
      var a = new Building(ax,ay,az,sections,'residential');//.constructBuilding();
      buildings.push(a);
  	}

    var newB = new Block(b*dim,groundLevel,b*dim*5,buildings).constructBlock();
    blocks.push(newB);
	  // blocks.push(new Block(b,groundLevel,b,buildings));
  }
}

function keyPressed() { // TODO a bit of a pain :)
  if (keyCode === LEFT_ARROW) {
    yRotation --;
	}
	else if (keyCode === RIGHT_ARROW) {
    yRotation ++;
	}
	else if (keyCode === UP_ARROW) {
		xRotation ++;
	}
	else if (keyCode === DOWN_ARROW) {
		xRotation --;
	} else {
		return false;
	}
}

// zoom in with wheel
function mouseWheel(event) {
  zoom += event.delta;
  // console.log(zoom);
  // translate(0,0,zoom);
}

// ********************* CLASSES

class Section {
	constructor(w,h,d){
		this.w = w;
		this.h = h;
		this.d = d;
	}

  constructSection(){
    box(this.w, this.h, this.d);
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
		this.funcColor = 255;
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
				stroke(0);
				ambientMaterial(this.funcColor); // change from framework to fill
				translate(0,-this.sections[s-1].getHeight(),0); // place on the top of the old section
			}
			else { // there is probably a smarter way.
				noFill();
				stroke(this.funcColor);
			}
			this.sections[s].constructSection();
			pop();
		}
		pop();
	}
}

class Block {
	constructor(x,y,z,buildings) {
		this.x = x;
		this.y = y;
		this.z = z;
		this.buildings = buildings;
	}

  constructBlock(){
    // console.log("translate");
    for (var b = 0 ; b < this.buildings.length ; b++){
      push();
		  translate(this.x,this.y,this.z+zoom); // zoom exec
      this.buildings[b].constructBuilding();
      pop();
      }

      var data = {
        x:'built'
      }
      socket.emit('block', data);
  }
}

// ********************* TEMP VALS
dim = 100;
loc = 50;
currcolor = 255;
buildingsInBlock = 9;
var newOnTheBlock;

// ********************* VARIABLES
sectionsInBuilding = 2; // each building has a old and new section
groundLevel = 0;
yRotation = -37;
xRotation = -25;
var functionalityColors = {"residential":"pink"};




function setup() {
  createCanvas(windowWidth,windowHeight,WEBGL);
}

function draw() {
  background(0);
  ambientLight(255, 255, 255);
	//TODO perspective(fovy,aspect,near,far)
	// TODO: move with arrows? or scrolling?
  rotateY(radians(yRotation));
	rotateX(radians(xRotation));



	// TODO 1. read dummy from file 2. read whole array from file

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
		buildings.push(new Building((j*110%440),groundLevel,(j%3*110),sections,'residential').constructBuilding()); //TODO why?!
	}
	newOnTheBlock = new Block(0,groundLevel,0,buildings);
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

// TODO zoom in with wheel
// function mouseWheel(event) {
//   pos += event.delta;
// }

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
		// console.log(functionalityColors['residential']);
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
}

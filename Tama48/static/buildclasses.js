// GUI BUILDING CLASSES

class Section {
	constructor(polygon,inHeight){
		this.p = polygon;
		this.h = inHeight;
	}

  constructSection(){
    // begin custom building shape
    beginShape();

    //ground shape
    for (var v = 0 ; v < this.p.length ; v++){
      vertex(this.p[v][0], groundLevel, this.p[v][1]);
    }

		 // close the shape for better controled fill
		vertex(this.p[this.p.length-1][0], groundLevel, this.p[0][1]);

    // for every two ajacent vertecies, we need to build a wall
    for (var v = 0 ; v < this.p.length-1 ; v++){
      vertex(this.p[v+1][0], groundLevel, this.p[v+1][1]);
      vertex(this.p[v][0], groundLevel, this.p[v][1]);
      vertex(this.p[v][0], this.h, this.p[v][1]);
      vertex(this.p[v+1][0], this.h, this.p[v+1][1]);
      vertex(this.p[v+1][0], groundLevel, this.p[v+1][1]);
    }

    // duplicate the ground shape at the top height
    for (var v = 0 ; v < this.p.length ; v++){
      vertex(this.p[v][0], this.h, this.p[v][1]);
    }

		// end custom shape
    endShape();
  }

	getHeight(){
		return this.h;
	}

  getPolygon(){
    return this.p;
  }
}

class Building {
	constructor(sections,functionality) { //sections is an array, location in polygon data
		this.sections = sections;
		this.func = functionality;
		this.funcColor = 255; // init on white for debugging
	}

	setfuncColor(){
		this.funcColor = color(functionalityColors[this.func]);
	}

	constructBuilding(){
		this.setfuncColor();
    strokeWeight(1);
		for (var s = 0 ; s < this.sections.length ; s++){
			push();
			if (s){ // new section has index 1
        noFill();
				stroke(this.funcColor);
				translate(0,this.sections[s-1].getHeight(),0); // place on the top of the old section
			}
			else {
        stroke(0);
        ambientMaterial(this.funcColor); // change from framework to fill
				this.sections[s].constructSection(); //TODO
      }
			// this.sections[s].constructSection(); //TODO
			pop();
		}
	}
}

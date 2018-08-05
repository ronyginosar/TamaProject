var building = [];

function setup() {
  createCanvas(700,900,WEBGL);
  for (var i=0;i<3;i++){
    building.push(new Section(100,100,100,i));
  }
}

function draw() {
  //background(0);
  //ambientLight(255, 255, 255);
  //stroke(255);
  //noFill();
  //normalMaterial();

  
  rotateY(radians(45));
  //rotateX(mouseX- width/2);
  //rotateY(mouseY - height/2);
  
  for (var i=0;i<building.length;i++){
    //print(building[i].y);
    building[i].display();
  } 
}

function Section(x,y,z,i){
  this.x = x;
  this.y = y;
  this.z = z;
  this.i = i;
  
  this.display = function(){
    //stroke(0);
    //ambientMaterial(this.i*200,255,255);
    
    push();
    //stroke(0);
    translate(0, this.y+(this.i*this.y*1.1)- height/3 ,0);
    box(this.x , this.y, this.z);
    pop();
  };


}

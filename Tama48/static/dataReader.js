// GUI PARSING

var buildingData;
var buildingsToBuild = [];
const floorHeight = 3;
const groundLevel = 0;
const xCorrection = 254482;
const yCorrection = 808933;

function updateData(data) {
  buildingData = data;
  parseData();
}

function parseData() {
    for ( var b = 0 ; b < buildingData.buildings.length ; b++){
      currBuilding = buildingData.buildings[b].building;
      // Building polygon
      for (var v = 0 ; v < currBuilding.polygon.length ; v++){
          currBuilding.polygon[v][0] = round(currBuilding.polygon[v][0] - xCorrection);
          currBuilding.polygon[v][1] = round(currBuilding.polygon[v][1] - yCorrection);
      }
      // Building location
      var x = round(currBuilding.location[0] - xCorrection);
      var y = groundLevel;
      var z = round(currBuilding.location[1] - yCorrection);
      // additional data
      functionality = 'residential';//currBuilding.type; TODO
      var initFloors = currBuilding.init_height;
      var addedFloors = currBuilding.extra_height;
      // if valid polygon - construct sections
      if (currBuilding.polygon){
        var initSection = new Section(currBuilding.polygon,initFloors*floorHeight*2);
        var addedSection = new Section(currBuilding.polygon,addedFloors*floorHeight*2);
        // construct building
        var build = new Building(x,y,z,[initSection,addedSection],functionality);
        buildingsToBuild.push(build);
      }
    }
}

//  loadJSON(path,callbackfunc(varToStoreData, 'jsonp')) // async, load data, when you are done, tell me(callback) and put it in var . last arg for security when using url json

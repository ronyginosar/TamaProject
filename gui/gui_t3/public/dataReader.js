// // init_building_data = {list} <class 'list'>: [('clinic', [<building.Building object at 0x0000022E725DB0B8>, <building.Building object at 0x0000022E725DB0F0>, <building.Building object at 0x0000022E725DB2B0>, <building.Building object at 0x0000022E725DB1D0>]), ('community_center', [<bu
// var cityBuildings = [];
// const loc = 5;
// const added = 0;
// const init = 4;
// const func = 0;
// const floorHeight = 3;



// extract_GIS_data: building, x,y, init height, functionalityColors
// from code: additional height, w,d , alg score toogle button alg
// calc in code or json? call funcions or parse?


//
//
// for (var buildtype = 0 ; buildtype < init_building_data.length ; buildtype++){
//   functionality = init_building_data[buildtype][func];
//   buildingList = init_building_data[buildtype][1];
//   for (var buildingIndex = 0 ; buildingIndex < buildingList.length ; buildingIndex++){
//     var HaddedFloors = buildingList[buildingIndex][added]*floorHeight;
//     var addedFloors = new Section(W,HaddedFloors,D) // TODO get W,D
//     var HinitFloors = buildingList[buildingIndex][init]*floorHeight;
//     var initFloors = new Section(W,initFloors,D) // TODO get W,D
//     // = buildingList[buildingIndex][0]; // there is area but it's better to have w,d
//     var xLoc = buildingList[buildingIndex][loc][0]; //x,z,y?
//     var yLoc = buildingList[buildingIndex][loc][2]; // 0, ground level
//     var zLoc = buildingList[buildingIndex][loc][1];
//     cityBuildings.push(new Building(xLoc,yLoc,zLoc,[initFloors,addedFloors],functionality));
//   }
// }

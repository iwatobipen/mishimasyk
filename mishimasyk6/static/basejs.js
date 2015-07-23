// var RDKit = rdk();
var padding = 30;
var h = 200;
var w = 500;
function  calc_mw_fsp3( smi ){
    var mol = RDKit.Molecule.fromSmiles( smi );
    var mw = mol.getMW();
    var fr_sp3 = mol.FractionCSP3();
    return { mw:mw, fr_sp3: fr_sp3,smi: smi };
};

function calc_smiles_data( smiles_data ){
    var dataset = [];
    var smiles_array = smiles_data.split("\n");
    var n = smiles_array.length;
    for( var i = 0; i < n; i ++)
        {
        var res = calc_mw_fsp3( smiles_array[i] );
        dataset.push( res );
        };
    return dataset;
    };

function moldraw( smi ){
  var mol = RDKit.Molecule.fromSmiles( smi );
  var mol2d = mol.Drawing2D();
  var remol = mol2d.replace( /svg:/g, '' );
  document.getElementById( 'molstructure' ).innerHTML = remol;
};

function darwchart( smiles_data ){
   d3.select("#scatterplot").remove();
   var svg = d3.select("#chart").append("svg")
                                .attr("id", "scatterplot")
                                .attr("width", w)
                                .attr("height", h);
   var dataset = calc_smiles_data( smiles_data );
   var xScale = d3.scale.linear()
               .domain([0, d3.max(dataset, function(d){return d["mw"];})] )
               .range([padding,w-padding]);

   var yScale = d3.scale.linear()
               .domain([0, d3.max(dataset, function(d){return d["fr_sp3"];})] )
               .range([h-padding,padding]);

   var xAxis = d3.svg.axis()
                     .scale(xScale)
                     .orient("bottom");
   svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + (h - padding) + ")")
      .call(xAxis);

   var yAxis = d3.svg.axis()
                     .scale(yScale)
                     .orient("left");
   svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + padding + ",0 )")
      .call(yAxis);


   svg.selectAll( "circle" )
      .data(dataset)
      .enter()
      .append("circle")
      .attr("cx", function(d){
                         return xScale(d["mw"]);
                         })
      .attr("cy", function(d){
                         return yScale(d["fr_sp3"]);
                         })
      .attr("r", 5)
      .attr("fill", "magenta")
      .on("mouseover", function(d){
                         return moldraw(d["smi"]);
                       })
      .on("mouseout", function(d){
                         return document.getElementById( 'molstructure' ).innerHTML = "";
                       })

};


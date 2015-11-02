d3.sankey = function() {
  var sankey = {},
      nodeWidth = 24,
      nodePadding = 8,
      size = [1, 1],
      nodes = [],
      links = [];

  sankey.nodeWidth = function(_) {
    if (!arguments.length) return nodeWidth;
    nodeWidth = +_;
    return sankey;
  };

  sankey.nodePadding = function(_) {
    if (!arguments.length) return nodePadding;
    nodePadding = +_;
    return sankey;
  };

  sankey.nodes = function(_) {
    if (!arguments.length) return nodes;
    nodes = _;
    return sankey;
  };

  sankey.links = function(_) {
    if (!arguments.length) return links;
    links = _;
    return sankey;
  };

  sankey.size = function(_) {
    if (!arguments.length) return size;
    size = _;
    return sankey;
  };

  sankey.layout = function(iterations) {
    computeNodeLinks();
    computeNodeValues();
    computeNodeBreadths();
    computeNodeDepths(iterations);
    computeLinkDepths();
    return sankey;
  };

  sankey.relayout = function() {
    computeLinkDepths();
    return sankey;
  };

function clone(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}


  sankey.link = function() {
    var curvature = .5;

    function link(d) {
      var x0 = d.source.x + d.source.dx,
          x1 = d.target.x,
          xi = d3.interpolateNumber(x0, x1),
          x2 = xi(curvature),
          x3 = xi(1 - curvature),
          y0 = d.source.y + d.sy + d.dy / 2,
          y1 = d.target.y + d.ty + d.dy / 2;
      return "M" + x0 + "," + y0
           + "C" + x2 + "," + y0
           + " " + x3 + "," + y1
           + " " + x1 + "," + y1;
    }

    link.curvature = function(_) {
      if (!arguments.length) return curvature;
      curvature = +_;
      return link;
    };

    return link;
  };

  // Populate the sourceLinks and targetLinks for each node.
  // Also, if the source and target are not objects, assume they are indices.
  function computeNodeLinks() {
    nodes.forEach(function(node) {
      node.sourceLinks = [];
      node.targetLinks = [];
    });
    
    links.forEach(function(link) {

      var source = link.source,
          target = link.target;
      if (typeof source === "number") {
		  var targetLink=clone(source);
		  source = link.source = nodes[link.source];
		}      
	  if (typeof target === "number") {
		  nodes[link.target].targetLink=targetLink;
		  target = link.target = nodes[link.target];
	  }
      source.sourceLinks.push(link);
      target.targetLinks.push(link);
      
    });
  }

  // Compute the value (size) of each node by summing the associated links.
  function computeNodeValues() {
    nodes.forEach(function(node) {
      node.value = Math.max(
        d3.sum(node.sourceLinks, value),
        d3.sum(node.targetLinks, value)
      );
    });
  }

  // Iteratively assign the breadth (x-position) for each node.
  // Nodes are assigned the maximum breadth of incoming neighbors plus one;
  // nodes with no incoming links are assigned breadth zero, while
  // nodes with no outgoing links are assigned the maximum breadth.
  function computeNodeBreadths() {
    var remainingNodes = nodes,
        nextNodes,
        x = 0;

    while (remainingNodes.length) {
      nextNodes = [];
      remainingNodes.forEach(function(node) {
        node.x = x;
        node.dx = nodeWidth;
        node.sourceLinks.forEach(function(link) {
          nextNodes.push(link.target);
        });
      });
      remainingNodes = nextNodes;
      ++x;
    }

    //
//     moveSinksRight(x);
    scaleNodeBreadths((width - nodeWidth) / (x - 1));
  }

  function moveSourcesRight() {
    nodes.forEach(function(node) {
      if (!node.targetLinks.length) {
        node.x = d3.min(node.sourceLinks, function(d) { return d.target.x; }) - 1;
      }
    });
  }

  function moveSinksRight(x) {
    nodes.forEach(function(node) {
      if (!node.sourceLinks.length) {
        node.x = x - 1;
      }
    });
  }

  function scaleNodeBreadths(kx) {
    nodes.forEach(function(node) {
      node.x *= kx;
    });
  }

    var highestnode=0;
    var lowestnode=0;
    var highestrank=0;
    var lowestrank=0;

  function computeNodeDepths(iterations) {
    var nodesByBreadth = d3.nest()
        .key(function(d) {return d.x; }).sortKeys(d3.ascending)
        .entries(nodes)
        .map(function(d) {return d.values; }); //the next function
        	//creates a new values field that contains all the info fitting the key

	console.log('nodesbybreadth',nodesByBreadth);

	var alpha = 1;

    initializeNodeDepth();
    relaxRightToLeft2(alpha);
  		//~ relaxLeftToRight2(alpha);  
     	relaxRightToLeft3(alpha);
     	
     	
// 		resolveCollisions();

// 		resolveCollisions();
      
    //~ for (var alpha = 1; iterations >0; --iterations) {
          //~ relaxLeftToRight2(alpha);
      //~ resolveCollisions();
//~ //       relaxRightToLeft2(alpha *= .99);
//~ //       resolveCollisions();
      //~ relaxRightToLeft3(alpha *= .99);
      //~ resolveCollisions();
//~ // 
    //~ }
    

    function initializeNodeDepth() {
		var ky = d3.min(nodesByBreadth, function(nodes) {  //ky is the multiplying factor
		// (1- (total # of nodes * node padding))
		return (size[1] - (nodes.length - 1) * nodePadding) / d3.sum(nodes, value);
		});

		var rankcount=0;
		var prevnodecount=0;
								
		nodesByBreadth.forEach(function(nodes)	{		
	
			nodes.forEach(function(node, i) { //assume for now that i is iterator				
				node.dy = node.value * ky;
			});		

			nodes.forEach(function(node, i) { //assume for now that i is iterator	
				if (node.targetLinks.length) {
					node.targetLinks.forEach(function (obj) {
						node.targeti=obj.source.i;
					});					
				} else {
					node.targeti=i;					
				};
				node.i=i;
			});	
			
			nodes.sort(
				firstBy(function (a, b) { return a.targeti-b.targeti; })
				.thenBy(function (a, b) { return b.value-a.value; })
			);				

			var templinkrank = 0;
			var temptarget = 0;
			var j=0;
			var rankSum=0;		
			var nodecount=-1;
			
			nodes.forEach(function (node) {++nodecount;});
				
			//~ console.log('nodecount',nodecount);	
				
			nodes.forEach(function(node, i) { //assume for now that i is iterator	
				if (j==0) {
					templinkrank = j;
					temptarget = node.targeti;
					if (node.targeti==0) {
						highestnode=node.node;
						highestrank=rankcount;
						}
					//~ j+=1;
				} else {
					if (temptarget == node.targeti) {
						templinkrank += 1;
						//~ j+=1;
					} else {
						temptarget = node.targeti;
						templinkrank=0;
						//~ j=0;
					}
				}
								
				if (i==nodecount) {
					//~ console.log('processing max node',i, node.node,nodecount,node.targeti,prevnodecount);
					if (node.targeti==prevnodecount) {
						lowestnode=node.node;
						lowestrank=rankcount;
					} 
					prevnodecount=nodecount;
				}
				
				node.i=i;
				node.y=i;
				node.templinkrank=templinkrank;
				j+=1;			
			});		
			
			rankcount+=1;

		});
					
		links.forEach(function(link) {
			link.dy = link.value * ky;
		});
					
    }



	var firstY, temprankSum;

	function relaxLeftToRight2(alpha) {
	  nodesByBreadth.forEach(function(nodes, breadth) {
		nodes.sort(
			firstBy(function (a, b) { return a.targeti-b.targeti; })
			.thenBy(function (a, b) { return b.value-a.value; })
		);
		
		nodes.forEach(function(node) {
		  if (node.sourceLinks.length>0) {
			var firstY=0, ranksum=0;
			node.sourceLinks.forEach(function(obj) {
				if (obj.target.templinkrank==0) {
					firstY=obj.target.y;
				} 
				ranksum +=obj.target.dy;			
			});
			ranksum += ((node.sourceLinks.length-1) * nodePadding)
			node.ranksum=ranksum;   
			node.y = (((firstY+ranksum)/2)-node.dy/2);      	
		  }
		});
	  });

	}


	function relaxRightToLeft2(alpha) {
			
			nodesByBreadth.slice().reverse().forEach(function(subnodes) {

			subnodes.sort(
				firstBy(function (a, b) { return a.targeti-b.targeti; })
				.thenBy(function (a, b) { return b.value-a.value; })
			);

			subnodes.forEach(function(node) {
				var ranksum=0;	
				node.hassourcelinks=0;
				if (node.sourceLinks.length>0) {				
					node.sourceLinks.forEach(function(obj) {
						ranksum +=obj.target.ranksum;				
					});
					ranksum += ((node.sourceLinks.length-1) * nodePadding)
					node.ranksum=ranksum;
					node.hassourcelinks=1;
				} else {
					node.ranksum=node.dy;
				}

			});
			
		});
	}

 	function relaxRightToLeft3(alpha) {
			
		nodesByBreadth.slice().reverse().forEach(function(subnodes) {

				var j=0;
				if (j<=highestrank) {
					
					subnodes.sort(
						firstBy(function (a, b) { return a.targeti-b.targeti; })
						.thenBy(function (a, b) { return b.value-a.value; })
					);
		
					var tempy=0;
					
					subnodes.forEach(function(node) {
						console.log('node',node.node);
						//	if node is top node and highest node, then set it at 0 + padding

						if (node.node==highestnode) {
							//~ console.log('highestnode');
							node.y=nodePadding;
							tempy=node.y+node.ranksum+nodePadding;
						//~ } else if (node.i==0) {
								//~ var firstY=0;
								//~ var endY=0;
								//~ node.sourceLinks.forEach(function(obj) {
									//~ if (obj.target.templinkrank==0) {
										//~ firstY=obj.target.y;										
									//~ } 		
									//~ endY=obj.target.y+obj.target.dy
								//~ });
								//~ node.y=firstY+((firstY-endY)/2)-(node.dy/2)
								//~ tempy=node.y+node.ranksum+nodePadding;								
						} else {
							//~ console.log('lowernodes');
							
							if (node.sourceLinks.length>0) {
								var firstY=0;
								var endY=0;
								node.sourceLinks.forEach(function(obj) {
									if (obj.target.templinkrank==0) {
										firstY=obj.target.y;										
									} 		
									endY=Math.max(obj.target.y+obj.target.dy,endY);
								});
								node.y=firstY+((endY-firstY)/2)-(node.dy/2)
								tempy=node.y+node.ranksum+nodePadding;	
							} else {
								node.y=tempy;
								tempy=node.y+node.ranksum+nodePadding;							
							}

						}														
					});
					
					j+=1;
				}
		});
	}
      
    function resolveCollisions() {
      nodesByBreadth.forEach(function(nodes) {
        var node, dy, y0 = 0, n = nodes.length,i;

        // Push any overlapping nodes down.
// 		nodes.sort(
// 			firstBy(function (a, b) { return a.targeti-b.targeti; })
// 			.thenBy(function (a, b) { return b.value-a.value; })
// 		);

		nodes.forEach(function(node) {
		  if (node.sourceLinks.length>0) {
			var firstY=0, ranksum=0;
			node.sourceLinks.forEach(function(obj) {
				if (obj.target.templinkrank==0) {
					firstY=obj.target.y;
				} 
				ranksum +=obj.target.dy;
			});

			ranksum += ((node.sourceLinks.length-1) * nodePadding)
				    
			node.y = (((firstY+ranksum)/2)-node.dy/2);         	
		  }
		});
		
        for (i = 0; i < n; ++i) {
          node = nodes[i];
		  
          dy = y0 - node.y;
          if (dy > 0) node.y += dy;
          y0 = node.y + node.dy + nodePadding;
        }
       
        // If the bottommost node goes outside the bounds, push it back up.
        dy = y0 - nodePadding - size[1];
        if (dy > 0) {
          y0 = node.y -= dy;

          // Push any overlapping nodes back up.
          for (i = n - 2; i >= 0; --i) {
            node = nodes[i];
            dy = node.y + node.dy + nodePadding - y0;
            if (dy > 0) node.y -= dy;
            y0 = node.y;
          	}
        }
    
        
      });
    }

//     function ascendingDepth(a, b) {
// 	  return a.i - b.i;
// //       return a.y - b.y;
//     }
  }

  function computeLinkDepths() {
    nodes.forEach(function(node) {
      node.sourceLinks.sort(ascendingTargetDepth);
      node.targetLinks.sort(ascendingSourceDepth);
    });
    nodes.forEach(function(node) {
      var sy = 0, ty = 0;
      node.sourceLinks.forEach(function(link) {
        link.sy = sy;
        sy += link.dy;
      });
      node.targetLinks.forEach(function(link) {
        link.ty = ty;
        ty += link.dy;
      });
    });

    function ascendingSourceDepth(a, b) {
      return a.source.y - b.source.y;
    }

    function ascendingTargetDepth(a, b) {
      return a.target.y - b.target.y;
    }
  }

  function center(node) {
    	var ycenter=node.y + node.dy / 2
    return node.y + node.dy / 2;
  }

  function value(link) {
    return link.value;
  }

  firstBy=(function(){function e(f){f.thenBy=t;return f}function t(y,x){x=this;return e(function(a,b){return x(a,b)||y(a,b)})}return e})();

  return sankey;
};


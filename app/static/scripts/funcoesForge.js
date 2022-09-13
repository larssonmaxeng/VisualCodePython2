/////////////////////////////////////////////////////////////////////
// Copyright (c) Autodesk, Inc. All rights reserved
// Written by Forge Partner Development
//
// Permission to use, copy, modify, and distribute this software in
// object code form for any purpose and without fee is hereby granted,
// provided that the above copyright notice appears in all copies and
// that both that copyright notice and the limited warranty and
// restricted rights notice below appear in all supporting
// documentation.
//
// AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS.
// AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
// MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.  AUTODESK, INC.
// DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
// UNINTERRUPTED OR ERROR FREE.
/////////////////////////////////////////////////////////////////////

var viewer;

function onDocumentLoadSuccess(doc) {

    // A document contains references to 3D and 2D viewables.
    var viewables = Autodesk.Viewing.Document.getSubItemsWithProperties(doc.getRootItem(), {'type':'geometry'}, true);
    if (viewables.length === 0) {
        console.error('Document contains no viewables.');
        return;
    }
    console.log("AQUIIIIIIIIIIIII");
    
    console.log(viewables);
    // Choose any of the avialble viewables
    var initialViewable = viewables[0];
    var svfUrl = doc.getViewablePath(initialViewable);
    var modelOptions = {
        sharedPropertyDbPath: doc.getPropertyDbPath()
    };

    var viewerDiv = document.getElementById('MyViewerDiv');
    viewer = new Autodesk.Viewing.Private.GuiViewer3D(viewerDiv);
    viewer.start(svfUrl, modelOptions, onLoadModelSuccess, onLoadModelError);
}

/**
 * Autodesk.Viewing.Document.load() failuire callback.
 */
function onDocumentLoadFailure(viewerErrorCode) {
    console.error('onDocumentLoadFailure() - errorCode:' + viewerErrorCode);
}

/**
 * viewer.loadModel() success callback.
 * Invoked after the model's SVF has been initially loaded.
 * It may trigger before any geometry has been downloaded and displayed on-screen.
 */
function onLoadModelSuccess(model) {
    console.log('onLoadModelSuccess()!');
    console.log('Validate model loaded: ' + (viewer.model === model));
    console.log(model);
}

/**
 * viewer.loadModel() failure callback.
 * Invoked when there's an error fetching the SVF file.
 */
function onLoadModelError(viewerErrorCode) {
    console.error('onLoadModelError() - errorCode:' + viewerErrorCode);
}

function Clicar(){

  var token = obterDados1()
  alert(token)
  var options = {
    env: 'AutodeskProduction',
    accessToken: token
  };
  console.log(options);
    /*console.log(options)
    Autodesk.Viewing.Initializer(options, () => {
    viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('MyViewerDiv'));
    viewer.start();
    var documentId = 'urn:' + 'dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6cHVvd2NocWtncWJrZ3hzY212ajM4ZjhxcmhlamxjbG42Mzc5ODMwOTM4NTcwMTM5MDcvU09ZLUFSUS1NT0RFTE8tUlZUMjAyMC1SMDIlMjAtJTIwQ29waWEucnZ0';
    Autodesk.Viewing.Document.load(documentId, onDocumentLoadSuccess, onDocumentLoadFailure);
  });*/
  var documentId = 'urn:' + 'dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6cHVvd2NocWtncWJrZ3hzY212ajM4ZjhxcmhlamxjbG42Mzc5ODMwOTM4NTcwMTM5MDcvU09ZLUFSUS1NT0RFTE8tUlZUMjAyMC1SMDIlMjAtJTIwQ29waWEucnZ0';
  Autodesk.Viewing.Initializer(options, function onInitialized(){
  Autodesk.Viewing.Document.load(documentId, onDocumentLoadSuccess, onDocumentLoadFailure);
});
}

function AbrirModelo(urn){
    var jsonData = {};
   /*var jsonData = {};
    for (let i = 0; i < subcriterios.length; i++) {
        var ele  = document.getElementById(subcriterios[i]);
        jsonData[subcriterios[i]] = ele.value;
    }*/
    jsonData["Teste"] = "Teste";
    var your_data =  jsonData

    fetch(`${window.origin}/access_token`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(your_data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
        }).then(response => response.json())
        .then(function(data){         
            console.log(data)
            var options = {
                env: 'AutodeskProduction',
                accessToken: data["access_token"]
              };
              console.log(options);
               
              var documentId = 'urn:' + urn;//'dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6cHVvd2NocWtncWJrZ3hzY212ajM4ZjhxcmhlamxjbG42Mzc5ODMwOTM4NTcwMTM5MDcvU09ZLUFSUS1NT0RFTE8tUlZUMjAyMC1SMDIlMjAtJTIwQ29waWEucnZ0';
              Autodesk.Viewing.Initializer(options, function onInitialized(){
              Autodesk.Viewing.Document.load(documentId, onDocumentLoadSuccess, onDocumentLoadFailure);
            });
            data["access_token"]    
                });
}


function getDataTreeViewModels(){
        var jsonData = {};
       /*var jsonData = {};
        for (let i = 0; i < subcriterios.length; i++) {
            var ele  = document.getElementById(subcriterios[i]);
            jsonData[subcriterios[i]] = ele.value;
        }*/
        jsonData["Teste"] = "Teste";
        var your_data =  jsonData
    
        fetch(`${window.origin}/GetTreeViewModels`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(your_data),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
            }).then(response => response.json())
            .then(function(data){ 
                var jsonData = [];         
                console.log(data);

                data.forEach(function(data1, index) { 
                    var bucket = {};     
                        
                    bucket['text'] = data1["bucketKey"].split("-")[1] ;
                    bucket['state'] = 'open';
                    jsonObjetos = [];
                    //console.log(data1['objetos']);
                        if(data1['objetos']!=undefined){    
                            data1['objetos'].forEach(function(objeto, index) {
                            var jsonObjeto = {};
                            jsonObjeto['text']= objeto["objectKey"];
                            jsonObjeto['data'] = objeto;
                            jsonNiveis01 = []
                            if(objeto['ListBom']!=undefined){    
                               
                                objeto['ListBom'].forEach(function(nivel01, index) {
                                //for aqui nivel 01
                                var  jsonNivel1 = {}
                                jsonNivel1['text']=(nivel01['bom'])["NIVEL01"]
                                jsonNivel1['data']=nivel01
                                
                                var jsonNiveis2=[]
                                if(nivel01['bom']!=undefined){    
                                    console.log(nivel01['bom'])
                                    var nivel02 = (nivel01['bom'])["NIVEL02"];
                                    //console.log('***********************')    
                                    //console.log(nivel02)
                                    //console.log((nivel01['bom'])["NIVEL01"])
                                    nivel02.forEach(function(nivel2, index) {
                                    //console.log('//for aqui nivel 02');
                                    //console.log(nivel2)

                                    var  jsonNivel2 = {}
                                    jsonNivel2['text']=nivel2['NIVEL02']
                                    jsonNivel2['data']=nivel2
                                    jsonNiveis2.push(jsonNivel2)

                                    });

                                    jsonNivel1['children'] = jsonNiveis2
                                    
                                }          
                                jsonNiveis01.push(jsonNivel1);
                                console.log('***Inserir jsonNivel01***')
                                console.log(jsonNivel1);
                                }
                               
                                );

                            }
                            jsonObjeto['children'] = jsonNiveis01
                           
                            jsonObjetos.push(jsonObjeto);
                        });
                        }
                        bucket['children'] = jsonObjetos;
                        
                        jsonData.push(bucket);
    
                    });   
                    $('#appBuckets').jstree({
                        'core': {
                            "themes": {
                                "responsive": false
                            },
                            "check_callback": true,
                            'data': []
                        },
                        "types": {
                            "default": {
                                "icon": "fa fa-folder icon-state-warning icon-lg"
                            },
                            "file": {
                                "icon": "fa fa-file icon-state-warning icon-lg"
                            }
                        },
                        "state": { "key": "demo2" },
                        "plugins": ["state", "types", "unique", "json_data", "search"]
                    }).bind("activate_node.jstree", function (evt, data) {
                        console.log("Clicou");
                        
                       
                        if (data != null && data.node != null && data.node.data != []) {
                          //$("#forgeViewer").empty();
                          console.log(data.node)
                          console.log(btoa(data.node.data["objectId"]));
                          var urn = btoa(data.node.data["objectId"]);
                          console.log("tentarAbrir");
                          AbrirModelo(urn);
                          
                            /*var options = {
                                env: 'AutodeskProduction',
                                getAccessToken: getForgeToken
                            };

                            Autodesk.Viewing.Initializer(options, () => {
                                viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('forgeViewer'));
                                viewer.start();
                                var documentId = 'urn:' + 'dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6cHVvd2NocWtncWJrZ3hzY212ajM4ZjhxcmhlamxjbG42Mzc5ODMwOTM4NTcwMTM5MDcvU09ZLUFSUS1NT0RFTE8tUlZUMjAyMC1SMDIlMjAtJTIwQ29waWEucnZ0';
                                Autodesk.Viewing.Document.load(documentId, onDocumentLoadSuccess, onDocumentLoadFailure);
                            });*/
                          
                          //alert("Teste")
                          //alert(urn)
                          
                          /*getForgeToken(function (access_token) {
                            jQuery.ajax({
                              url: 'https://developer.api.autodesk.com/modelderivative/v2/designdata/' + urn + '/manifest',
                              headers: { 'Authorization': 'Bearer ' + access_token },
                              success: function (res) {
                                if (res.progress === 'success' || res.progress === 'complete') launchViewer(urn);
                                else $("#forgeViewer").html('The translation job still running: ' + res.progress + '. Please try again in a moment.');
                              },
                              error: function (err) {
                                var msgButton = 'This file is not translated yet! ' +
                                  '<button class="btn btn-xs btn-info" onclick="translateObject()"><span class="glyphicon glyphicon-eye-open"></span> ' +
                                  'Start translation</button>'
                                $("#forgeViewer").html(msgButton);
                              }
                            });
                          })*/
                        }
                      });
                    $('#appBuckets').jstree(true).settings.core.data = jsonData;
                    $('#appBuckets').jstree(true).refresh();
                    $('#appBuckets').jstree("open_all");
                    $('#appBuckets').jstree("deselect_all");
                console.log(jsonData);
            }
                //var jsonData = {};
                );
                
        }
function prepareAppBucketTreeFuzzy() {
            console.log("prepare")
            getDataTreeViewModels()
            /*//*var v =  document.getElementById("appBuckets");
            //console.log(v.id)*/
            var  lsTreeData = [{
                "text": "Factory 1: (1-1000)",
                "state": "closed",
                "children": [{
                    "text": 649
                }, {
                    "text": 108
                }, {
                    "text": 86
                }, {
                    "text": 46
                }]
            }, {
                "text": "Factory 2: (1001-2000)",
                "state": "closed",
                "children": {
                    "text": "No child nodes"
                }
            }, {
                "text": "Factory 3: (2001-3000)",
                "state": "closed",
                "children": [{
                    "text": 2435
                }, {
                    "text": 2951
                }, {
                    "text": 2313
                }]
            }, {
                "text": "Factory 4: (3001-4000)",
                "state": "closed",
                "children": [{
                    "text": 3952
                }, {
                    "text": 3722
                }, {
                    "text": 3593
                }, {
                    "text": 3252
                }, {
                    "text": 3893
                }, {
                    "text": 3854
                }, {
                    "text": 3320
                }, {
                    "text": 3092
                }]
            }, {
                "text": "Factory 5: (4001-5000)",
                "state": "closed",
                "children": {
                    "text": "No child nodes"
                }
            }];
           }
function autodeskCustomMenu1(autodeskNode) {
            var items;
          
            switch (autodeskNode.type) {
              case "bucket":
                items = {
                  uploadFile: {
                    label: "Upload file",
                    action: function () {
                      //uploadFile();
                    },
                    icon: 'glyphicon glyphicon-cloud-upload'
                  }
                };
                break;
              case "object":
                items = {
                  translateFile: {
                    label: "Translate",
                    action: function () {
                      //var treeNode = $('#appBuckets').jstree(true).get_selected(true)[0];
                      //translateObject(treeNode);
                    },
                    icon: 'glyphicon glyphicon-eye-open'
                  }
                };
                break;
            }
          
            return items;
          }

          
function GetAllIds(){

    var instanceTree = viewer.model.getData().instanceTree;
 
    var allDbIdsStr = Object.keys(instanceTree.nodeAccess.dbIdToIndex);
 
    return allDbIdsStr.map(function(id) { return parseInt(id)});
 }

function GetPropriedadesTeste(){

    console.log(GetAllIds());
    viewer.hide(GetAllIds());
  
}
function getSubset(dbIds, name, value, callback) {
    console.log("getSubset, dbIds.length before = " + dbIds.length)
    viewer.model.getBulkProperties(dbIds, {
        propFilter: [name],
        ignoreHidden: true
    }, function(data) {
        var newDbIds = []
        for (var key in data) {
            var item = data[key]
            /*if (item.properties[0].displayValue === value) {*/
                newDbIds.push(item.dbId)
           /* }*/
        }
        console.log("getSubset, dbIds.length after = " + newDbIds.length)
        callback(newDbIds)
    }, function(error) {})
}

function SucessoAoFiltrar(dbIds) {
    console.log(dbIds);
    Autodesk.Viewing.Viewer3D.prototype.turnOff = dbIds;  
    /*console.log(dbIds.length);
    getSubset(dbIds, propertyName, 10, function(dbIds) {
        viewer.isolate(dbIds)
    })*/
 
       /* console.log(dbIds);
        viewer.hide(dbIds);
        Autodesk.Viewing.Viewer3D.prototype.turnOff = dbIds; 
        

        viewer.model.getBulkProperties(dbIds,['Area'], 
        function(elements){
            var totalMass = 0;
            for(var i=0; i<elements.length; i++){
                
            }
            //console.log(totalMass);
          })*/
       
}
function SucessoGetBulk(){

}
function ErroGetBulk(){

}
function getBulkProperties(dbIds, options, SucessoGetBulk, ErroGetBulk){

}

function GetPropriedades(){
   arraydb = [];
   viewer.search('Floor',function(dbIds){
    
    viewer.model.getBulkProperties(dbIds, ['Area', 'Material estrutural'],
    function(elements){
        var v = [];
      var totalMass = 0;
      for(var i=0; i<elements.length; i++){
        console.log(elements[i].properties);
        
        //v.push(elements[i].dbId);
      try
      {
        if(elements[i].properties[1].displayValue=='.BLOCO'){
           
            v.push(elements[i].dbId);
        }
        }
        catch(error){
            console.log(error);
        }
        viewer.isolate(v);
      }
      
      
    });
   
 } , null, ['Material']);  
   

}
function GetEelemnets(){
     
     viewer.search('Floor',function(dbIds){
     viewer.model.getBulkProperties(dbIds, ['Area', 'Material estrutural'],
     function(elements){
         var v = [];
       var totalMass = 0;
       for(var i=0; i<elements.length; i++){
         console.log(elements[i].properties);
         
         //v.push(elements[i].dbId);
       try
       {
         if(elements[i].properties[1].displayValue=='.BLOCO'){
            
             v.push(elements[i].dbId);
         }
         }
         catch(error){
             console.log(error);
         }
         viewer.isolate(v);
       }
       
       
     });
    
  } , null, ['Material']);  
    
 
 }


 function getDataTreeViewAquisicoes(){
    var jsonData = {};
   /*var jsonData = {};
    for (let i = 0; i < subcriterios.length; i++) {
        var ele  = document.getElementById(subcriterios[i]);
        jsonData[subcriterios[i]] = ele.value;
    }*/
    jsonData["Teste"] = "Teste";
    var your_data =  jsonData

    fetch(`${window.origin}/GetTreeViewModels`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(your_data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
        }).then(response => response.json())
        .then(function(data){ 
            var jsonData = [];         
            console.log(data);

            data.forEach(function(data1, index) { 
                var bucket = {};     
                    
                bucket['text'] = data1["bucketKey"].split("-")[1] ;
                bucket['state'] = 'open';
                jsonObjetos = [];
                //console.log(data1['objetos']);
                    if(data1['objetos']!=undefined){    
                        data1['objetos'].forEach(function(objeto, index) {
                        var jsonObjeto = {};
                        jsonObjeto['text']= objeto["objectKey"];
                        jsonObjeto['data'] = objeto;
                        jsonNiveis01 = []
                        if(objeto['ListBom']!=undefined){    
                           
                            objeto['ListBom'].forEach(function(nivel01, index) {
                            //for aqui nivel 01
                            var  jsonNivel1 = {}
                            jsonNivel1['text']=(nivel01['bom'])["NIVEL01"]
                            jsonNivel1['data']=nivel01
                            
                            var jsonNiveis2=[]
                            if(nivel01['bom']!=undefined){    
                                console.log(nivel01['bom'])
                                var nivel02 = (nivel01['bom'])["NIVEL02"];
                                //console.log('***********************')    
                                //console.log(nivel02)
                                //console.log((nivel01['bom'])["NIVEL01"])
                                nivel02.forEach(function(nivel2, index) {
                                //console.log('//for aqui nivel 02');
                                //console.log(nivel2)

                                var  jsonNivel2 = {}
                                jsonNivel2['text']=nivel2['NIVEL02']
                                jsonNivel2['data']=nivel2
                                jsonNiveis2.push(jsonNivel2)

                                });

                                jsonNivel1['children'] = jsonNiveis2
                                
                            }          
                            jsonNiveis01.push(jsonNivel1);
                            console.log('***Inserir jsonNivel01***')
                            console.log(jsonNivel1);
                            }
                           
                            );

                        }
                        jsonObjeto['children'] = jsonNiveis01
                       
                        jsonObjetos.push(jsonObjeto);
                    });
                    }
                    bucket['children'] = jsonObjetos;
                    
                    jsonData.push(bucket);

                });   
                $('#comprasId').jstree({
                    'core': {
                        "themes": {
                            "responsive": false
                        },
                        "check_callback": true,
                        'data': []
                    },
                    "types": {
                        "default": {
                            "icon": "fa fa-folder icon-state-warning icon-lg"
                        },
                        "file": {
                            "icon": "fa fa-file icon-state-warning icon-lg"
                        }
                    },
                    "state": { "key": "demo2" },
                    "plugins": ["state", "types", "unique", "json_data", "search"]
                }).bind("activate_node.jstree", function (evt, data) {
                    console.log("Clicou");
                    
                   
                 /*   if (data != null && data.node != null && data.node.data != []) {
                      //$("#forgeViewer").empty();
                      console.log(data.node)
                      console.log(btoa(data.node.data["objectId"]));
                      var urn = btoa(data.node.data["objectId"]);
                      console.log("tentarAbrir");
                      AbrirModelo(urn);
                      
                        
                    }*/
                  });
                $('#comprasId').jstree(true).settings.core.data = jsonData;
                $('#comprasId').jstree(true).refresh();
                $('#comprasId').jstree("open_all");
                $('#comprasId').jstree("deselect_all");
            console.log(jsonData);
        }
            //var jsonData = {};
            );
            
    }

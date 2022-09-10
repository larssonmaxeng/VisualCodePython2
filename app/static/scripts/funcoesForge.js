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

function obterDados1(){
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
               
              var documentId = 'urn:' + 'dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6cHVvd2NocWtncWJrZ3hzY212ajM4ZjhxcmhlamxjbG42Mzc5ODMwOTM4NTcwMTM5MDcvU09ZLUFSUS1NT0RFTE8tUlZUMjAyMC1SMDIlMjAtJTIwQ29waWEucnZ0';
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
                        
                    bucket['text'] = data1["objectKey"];
                    bucket['state'] = 'open';
                    jsonFilhos = []
                    bucket['objetos'].forEach(function(filho, index) {
                        var jsonFilho = {};
                        jsonFilho['text']= filho["objectKey"];
                        jsonFilhos.push(jsonFilho);
                    });
                    bucket['children'] = jsonFilho;
                    jsonData.push();
 
                });         
                console.log(jsonData);
            }
                //var jsonData = {};
                );
                
        }
function prepareAppBucketTreeFuzzy() {
            console.log("prepare")
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
            $('#appBuckets').jstree({
                'core': {
                    "themes": {
                        "responsive": false
                    },
                    "check_callback": true,
                    'data': {
                    "url": `${window.origin}/GetTreeViewModels`,
                    "dataType": "json",
                    'multiple': false,
                    "data": function (node) {
                      return { "id": node.id };
                    
                  }
                }
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
            });
            /*
            
            
            .jstree({
              'core': {
                'themes': { "icons": true },
                'data': loDatas/*{/*
                    "url": `${window.origin}/GetTreeViewModels`,
                    "dataType": "json",
                    'multiple': false,
                    "data": function (node) {
                      return { "id": node.id };
                    
                  }
                }*/
            /*  },
              'types': {
                'default': {
                  'icon': 'glyphicon glyphicon-question-sign'
                },
                '#': {
                  'icon': 'glyphicon glyphicon-cloud'
                },
                'bucket': {
                  'icon': 'glyphicon glyphicon-folder-open'
                },
                'object': {
                  'icon': 'glyphicon glyphicon-file'
                }
              },
              "plugins": ["types", "state", "sort", "contextmenu"]
            });/*.on('loaded.jstree', function () {
              $('#appBuckets').jstree('open_all');
            }).bind("activate_node.jstree", function (evt, data) {
              if (data != null && data.node != null && data.node.type == 'object') {
                /*$("#forgeViewer").empty();
                var urn = data.node.id;
                alert("Teste")
                alert(urn)
                
                getForgeToken(function (access_token) {
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
                })
              }
            });*/
            
            //$('#maintree').jstree(true).settings.core.data = lsTreeData;
            $('#maintree').jstree(true).refresh();
            $("#maintree").jstree("open_all");
            $("#maintree").jstree("deselect_all");
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
          
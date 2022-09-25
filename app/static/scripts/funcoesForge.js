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
var noArvoreSelecionado;
var dadosModelo;
var  listaDeCores = [];
$(document).ready(function () {
    console.log("foi?")
   
    dia = new Date('2022 01 01');
   

    j = 0;
    while (j<30){
        dia.setMonth(dia.getMonth() + 1 );
        j = j+1;
        
        let ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(dia);
        let mo = new Intl.DateTimeFormat('en', { month: '2-digit' }).format(dia);
        let da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(dia);
        //console.log(`${da}-${mo}-${ye}`);             
        cor = {};
        cor['mes'] = `${ye}-${mo}-${da}`;
        corHex = gerar_cor_hexadecimal();
        corRGB = hexToRGBThree(hexToRGB(corHex), 0.9);
        cc = corRGB; 
        cor['cor'] = cc['cor'];
        cor['textoCor']= cc['textoCor'];
        cor['corhex'] = corHex;
        listaDeCores.push(cor);
    }
      console.log(listaDeCores);


      document.getElementById("abaHierarquiBOMButton").click();
      document.getElementById("dadosBOMButton").click();
      "use strict";
      //$("#grid").remove();
      
      //$("#divGridMaterial").prepend('<table id="grid"></table>');
      $("#grid").jqGrid({
          colModel: [
              //{ name: "idForge", label: "IDForge", width: 120 },
              //{ name: "ifcguid", label: "IfcGUID", width: 120 },
              { name: "descricao", label: "Descrição", width: 450 },
              { name: "unid", label: "Unidade", width: 80, align: "center"},
              { name: "qtde", label: "Quantidade", width: 110, template: "number" },
              { name: "pacote", label: "Pacote", width: 90},
              { name: "qtdePacote", label: "Qtde pacote", width: 110, template: "number" }
              
          ],
          data: [],
          iconSet: "fontAwesome",
          idPrefix: "g5_",
          rownumbers: true,
          sortorder: "desc",
          threeStateSort: true,
          sortable: true,
          guiStyle: "bootstrap",  
          sortIconsBeforeText: true,
          headertitles: true,
          toppager: true,
          navOptions: { add: false, edit: false, del: false, search: false },
          multiselect: true,
          pager: true,
          rowNum: 60,
          viewrecords: true,
          searching: {
              defaultSearch: "cn"
          },
          caption: "Quantidades para o modelo selecionado"
      }).jqGrid("filterToolbar").jqGrid("navGrid", { view: true })
          .jqGrid("inlineNav")
          .jqGrid("gridResize");

  
  });
 function hexToRGB(hex){
  return hex.replace(/^#?([a-f\d])([a-f\d])([a-f\d])$/i
             ,(m, r, g, b) => '#' + r + r + g + g + b + b)
    .substring(1).match(/.{2}/g)
    .map(x => parseInt(x, 16))
 }

function gerar_cor(opacidade) {
    let r = Math.random() * 255;
    let g = Math.random() * 255;
    let b = Math.random() * 255;
 
    return  {'cor':new THREE.Vector4(r/255, g/255, b/255, opacidade), 
              'textoCor':'rgba('+r/255+','+g/255+','+ b/255+','+ opacidade+')'};
 }
 function hexToRGBThree(obj, opacidade) {
    let r = obj[0];//  Math.random() * 255;
    let g = obj[1];// Math.random() * 255;
    let b = obj[2];// Math.random() * 255;
    return  {'cor':new THREE.Vector4(r/255, g/255, b/255, opacidade), 
              'textoCor':'rgba('+r/255+','+g/255+','+ b/255+','+ opacidade+')'};
 }
 function gerar_cor_hexadecimal()
 {
   return '#' + parseInt((Math.random() * 0xFFFFFF))
     .toString(16)
     .padStart(6, '0');
 }
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
                //console.log(data);

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
                                     
                                    
                                    //console.log((nivel01['bom'])["NIVEL01"])
                                    nivel02.forEach(function(nivel2, index) {
                                    //console.log('//for aqui nivel 02');
                                    //console.log(nivel2)
                                    //console.log('***********************')  
                                    //onsole.log(nivel2)
                                    var  jsonNivel2 = {}
                                    jsonNivel2['text']=nivel2['NIVEL02'];
                                    jsonNivel2['data']=nivel2;

                                    jsonNiveis2.push(jsonNivel2);

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
                    console.log(jsonData); 
                    $('#treeHierarquia').jstree({
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
                        "plugins": ["state", "types", "unique", "json_data", "search", "checkbox" ]
                    }).bind("activate_node.jstree", function (evt, data) {
                        console.log("Clicou");
                        
                        //noArvoreSelecionado = undefined;
                        if (data != null && data.node != null && data.node.data != []) {
                          //$("#forgeViewer").empty();
                          
                          if((noArvoreSelecionado != data.node.data)|
                             (noArvoreSelecionado==undefined)){
                                //console.log(data.node)
                                //console.log(btoa(data.node.data["objectId"]));
                                var urn = btoa(data.node.data["objectId"]);
                                console.log("tentarAbrir");
                                noArvoreSelecionado =data.node.data; 
                                AbrirModelo(urn);
                                
                          }
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
                    $('#treeHierarquia').jstree(true).settings.core.data = jsonData;
                    $('#treeHierarquia').jstree(true).refresh();
                    $('#treeHierarquia').jstree("open_all");
                    $('#treeHierarquia').jstree("deselect_all");
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

function GetIdProp(objeto, campoProcurado){
    //console.log(objeto)
    registrosEsperados = 7
    for(var i=0; i<registrosEsperados; i++){
        //console.log(objeto.properties[i].displayName)
        try
        {
            if(objeto.properties[i].displayName==campoProcurado){
                //console.log("Código: "+i);
                return i;    
            }
        }
        catch(error){
            //console.log(error);
        }
    }
    return undefined;

}

function GetPropriedadesVisiveis(){
    
    arraydb = [];
    vetorCategoriasAnalisadas = ['Revit Peças hidrossanitárias', 'Revit Tubulação', 'Revit Conexões de tubo'];
    if(noArvoreSelecionado!=undefined){
        viewer.search('Floor',function(dbIds){
        
            viewer.model.getBulkProperties(dbIds, ['Category', 'ExecutarEm', 'Pavimento', 'Localizacao','Comentários', 'HID-Descrição',  'Comprimento'],
            function(elements){
                var v = [];
                dadosModelo = [];
                categoriasListadas = [];
                for(var i=0; i<elements.length; i++){
                    //console.log('-------------------------------------------------');
                    //console.log(elements[i]);
                    /*try
                    {*/
                        if(noArvoreSelecionado["NIVEL02"]!=undefined){
                            localizacaoId = GetIdProp(elements[i],'Localizacao');
                            unidId = GetIdProp(elements[i],'Comentários');
                            pavimentoId = GetIdProp(elements[i],'Pavimento');
                            comprimentoId = GetIdProp(elements[i],'Comprimento');
                            hidDescricao = GetIdProp(elements[i],'HID-Descrição');
                            ExecutarEmId = GetIdProp(elements[i],'ExecutarEm');
                            // ifcGuidId = GetIdProp(elements[i],'IfcGUID');
                            CategoriaId = GetIdProp(elements[i],'Category');
                            if((localizacaoId!=undefined)&
                               (unidId!=undefined)&
                               (pavimentoId!=undefined)&
                               (hidDescricao!=undefined)){
                                if((elements[i].properties[localizacaoId].displayValue==noArvoreSelecionado["NIVEL02"])&
                                (elements[i].properties[pavimentoId].displayValue==noArvoreSelecionado["NIVEL01"])&
                                (vetorCategoriasAnalisadas.indexOf(elements[i].properties[CategoriaId].displayValue)!=-1)){
                                    //categoriaListada = {};
                                   /* viewer.model.getProperties(elements[i].dbId, function(propriedades){
                                        console.log(propriedades);
                                    }, null);*/
                                    /*categoriaListada = elements[i].properties[CategoriaId].displayValue;
                                    if(categoriasListadas.indexOf(categoriaListada)==-1){
                                        categoriasListadas.push(categoriaListada);
                                    }*/


                                   
                                    v.push(elements[i].dbId);
                                    var dadoModelo = {};
                                    //dadoModelo['idForge'] = elements[i]["dbId"];
                                    //dadoModelo['ifcguid'] = elements[i].properties[ifcGuidId].displayValue;
                                    dadoModelo['descricao'] = elements[i].properties[hidDescricao].displayValue;
                                    dadoModelo['unid'] = elements[i].properties[unidId].displayValue;
                                    executarEm = elements[i].properties[ExecutarEmId].displayValue;
                                    
                                    if((executarEm!=undefined)&
                                       (executarEm!="")&
                                       (executarEm!='') ){
                                        var arrDia = executarEm.split('/');
                                        var stringFormatada = arrDia[2] + '-' + arrDia[1] + '-' +arrDia[0];  
                                        dadoModelo['mes'] = /*new Date(*/stringFormatada /*)*/;
                                       
                                    }else{
                                        //console.log(executarEm);
                                        
                                        dadoModelo['mes'] ="2022-01-01";
                                    }
                                    if(elements[i].properties[unidId].displayValue=='m'){
                                       try{
                                        dadoModelo['qtde'] = elements[i].properties[comprimentoId].displayValue;
                                       }
                                       catch{

                                       }
                                    } else{
                                        dadoModelo['qtde'] = 1;        
                                    }
                                    dadosModelo.push(dadoModelo);
                                      

                                }
                            }
                        }

                    /*}
                        catch(error){
                            //console.log(error);
                    }*/
                };
                viewer.isolate(v);    
                console.log('*******************************************')
                listaOriginal = JSON.parse(JSON.stringify(dadosModelo));
                $("#pivot").pivotUI(listaOriginal, {
                    derivedAttributes: {
                        /*"Age Bin": derivers.bin("Age", 10),
                        "Gender Imbalance": function(mp) {
                            return mp["Gender"] == "Male" ? 1 : -1;
                            }*/
                        }
                    });
                
                resumo = [];

                dadosModelo.forEach(function(data1, index) { 
                    
                    reg = resumo.find(o => o.descricao === data1['descricao']);
                    //console.log(data1['descricao']);
                    //console.log(reg);
                    
                    if(reg==undefined){
                        resumo.push(data1);
                    }  else{
                       reg['qtde'] =      reg['qtde'] + data1['qtde'];
                    }
   
                });
               
               
                //navigator.clipboard.writeText(JSON.stringify(resumo));
                filename='reports.xlsx';
                    /*data=[{Market: "IN", New Arrivals: "6", Upcoming Appointments: "2", Pending - 1st Attempt: "4"},
                            {Market: "KS/MO", New Arrivals: "4", Upcoming Appointments: "4", Pending - 1st Attempt: "2"},
                            {Market: "KS/MO", New Arrivals: "4", Upcoming Appointments: "4", Pending - 1st Attempt: "2"},
                            {Market: "KS/MO", New Arrivals: "4", Upcoming Appointments: "4", Pending - 1st Attempt: "2"}]*/
                        var ws = XLSX.utils.json_to_sheet(listaOriginal);
                        var wb = XLSX.utils.book_new();
                        XLSX.utils.book_append_sheet(wb, ws, "Resumo");
                        XLSX.writeFile(wb,filename);
                $("#grid").jqGrid('setGridParam',
                { 
                    datatype: 'local',
                    data:resumo
                }).trigger("reloadGrid");
                var derivers = $.pivotUtilities.derivers;
            
            });
        
         } , null, ['Material']);  
    }
    else{
        console.log("No arvore vazio")
    }

    $("body").css("cursor", "default");
 }
/*esse deu certo*/
function GetPropriedades(){
   arraydb = [];
   viewer.search('Floor',function(dbIds){
    
    viewer.model.getBulkProperties(dbIds, ['Pavimento', 'Localização', 'HID-Descrição'],
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

 function openCity(evt, cityName, divpai) {
    console.log(evt);
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    
    for (i = 0; i < tabcontent.length; i++) {
      if(tabcontent[i].id.includes(divpai)){
          console.log(tabcontent[i].id);
          tabcontent[i].style.display = "none";
        }
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      if(tablinks[i].id.includes(divpai)){
        console.log(tablinks[i].id);
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }


  function GetColorirModeloBaseadoEmData(){
    
    arraydb = [];
    $("#tabelaDeCores").remove();
      
    mesesUsado =[];
    vetorCategoriasAnalisadas = ['Revit Peças hidrossanitárias', 'Revit Tubulação', 'Revit Conexões de tubo'];
    if(noArvoreSelecionado!=undefined){
        viewer.search('Floor',function(dbIds){
        
            viewer.model.getBulkProperties(dbIds, ['Category', 'ExecutarEm', 'Pavimento', 'Localizacao','Comentários', 'HID-Descrição',  'Comprimento'],
            function(elements){
                var v = [];
               
               
               
                for(var i=0; i<elements.length; i++){
                    //console.log('-------------------------------------------------');
                    //console.log(elements[i]);
                    /*try
                    {*/
                        if(noArvoreSelecionado["NIVEL02"]!=undefined){
                            localizacaoId = GetIdProp(elements[i],'Localizacao');
                            unidId = GetIdProp(elements[i],'Comentários');
                            pavimentoId = GetIdProp(elements[i],'Pavimento');
                            comprimentoId = GetIdProp(elements[i],'Comprimento');
                            hidDescricao = GetIdProp(elements[i],'HID-Descrição');
                            ExecutarEmId = GetIdProp(elements[i],'ExecutarEm');
                            // ifcGuidId = GetIdProp(elements[i],'IfcGUID');
                            CategoriaId = GetIdProp(elements[i],'Category');
                            if((localizacaoId!=undefined)&
                               (unidId!=undefined)&
                               (pavimentoId!=undefined)&
                               (hidDescricao!=undefined)){
                                if((elements[i].properties[localizacaoId].displayValue==noArvoreSelecionado["NIVEL02"])&
                                (elements[i].properties[pavimentoId].displayValue==noArvoreSelecionado["NIVEL01"])&
                                (vetorCategoriasAnalisadas.indexOf(elements[i].properties[CategoriaId].displayValue)!=-1)){
                                   
                                    v.push(elements[i].dbId);
                                    var dadoModelo = {};
                                    dadoModelo['descricao'] = elements[i].properties[hidDescricao].displayValue;
                                    dadoModelo['unid'] = elements[i].properties[unidId].displayValue;
                                    executarEm = elements[i].properties[ExecutarEmId].displayValue;
                                    
                                    if((executarEm!=undefined)&
                                       (executarEm!="")&
                                       (executarEm!='') ){
                                        var arrDia = executarEm.split('/');
                                        var stringFormatada = arrDia[2] + '-' + arrDia[1] + '-' +arrDia[0];  
                                        dadoModelo['mes'] = /*new Date(*/stringFormatada /*)*/;
                                       
                                    }else{
                                        //console.log(executarEm);
                                        
                                        dadoModelo['mes'] ="2022-01-01";
                                    }
                                   
                                    cor = listaDeCores.find(o => String(o.mes) === String(dadoModelo['mes']));
                                   
                                    if(cor!=undefined){
                                        
                                        viewer.setThemingColor(elements[i].dbId,cor.cor);
                                        mesUsado = mesesUsado.find(o => String(o.mes) === String(dadoModelo['mes']));
                                        if(mesUsado==undefined){
                                            mesesUsado.push(cor);
                                        }    
                                    }

                                }
                            }
                        }

                   
                };
                console.log(mesesUsado);
                //viewer.isolate(v);    
                $("#paiTabelaCores").append('<table id="tabelaDeCores"></table>');
                $("#tabelaDeCores").append('<tr><th width="85px" class="tituloColuna">Mês</th><th width="50px" class="tituloColuna">Cor</th></tr>');
                mesesUsado.forEach(function(data1, index) { 
                    //$("#tabelaDeCores").append('<tr><td>'+data1['mes']+'</td><td id=\"cor'+data1['mes']+'\" bgcolor=\"'+rgba2hex(data1['textoCor'])+'\" ></td></tr>');
                    $("#tabelaDeCores").append('<tr><td>'+data1['mes']+'</td><td id=\"cor'+data1['mes']+'\" bgcolor=\"'+data1['corhex']+'\" ></td></tr>');
                    
                    var id ='cor'+data1['mes'];
                                  
                });
            
            });
        
         } , null, ['Material']);  
    }
    else{
        console.log("No arvore vazio")
    }
      
    
 }

 function rgba2hex(orig) {
    var a, isPercent,
      rgb = orig.replace(/\s/g, '').match(/^rgba?\((\d+),(\d+),(\d+),?([^,\s)]+)?/i),
      alpha = (rgb && rgb[4] || "").trim(),
      hex = rgb ?
      (rgb[1] | 1 << 8).toString(16).slice(1) +
      (rgb[2] | 1 << 8).toString(16).slice(1) +
      (rgb[3] | 1 << 8).toString(16).slice(1) : orig;
  
    if (alpha !== "") {
      a = alpha;
    } else {
      a = 01;
    }
    // multiply before convert to HEX
    a = ((a * 255) | 1 << 8).toString(16).slice(1)
    hex = hex + a;
  
    return hex;
  }
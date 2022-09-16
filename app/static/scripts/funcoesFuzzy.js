function mostrarValor() {
    alert("texto");
}
function obterDados(){
    let subcriterios = []
    subcriterios.push('CustoPreco')
    subcriterios.push('CustoPgto')
    subcriterios.push('CustoReajuste')
    subcriterios.push('QualiDevolucao')
    subcriterios.push('QualiDimensoes')
    subcriterios.push('QualiEquipe')

   
    
    subcriterios.push('PrazoPrazo')
    subcriterios.push('PrazoProducao')
    subcriterios.push('PrazoResposta')
  
   
    
    subcriterios.push('GestaoEntrega')
    subcriterios.push('GestaoCooperacao')
    subcriterios.push('GestaoParceria')
    subcriterios.push('GestaoTransparência')
    subcriterios.push('GestaoComunicacao')
    


    
    subcriterios.push('GeralLeis')
    subcriterios.push('GeralInteresses')
    subcriterios.push('GeralToxico')
    subcriterios.push('GeralHistoricoPrazo')
    subcriterios.push('GeralParceria')
    subcriterios.push('GeralHistorico')
    subcriterios.push('GeralSaudeESeguranca')

    var jsonData = {};
    for (let i = 0; i < subcriterios.length; i++) {
        var ele  = document.getElementById(subcriterios[i]);
        jsonData[subcriterios[i]] = ele.value;
    }
    var your_data =  jsonData
    return  fetch(`${window.origin}/your_url`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(your_data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
        }).then(response => response.json())
        .then(function(data){         
        data.forEach(function(data1, index) {
            
            if(data1["idHtml"].includes('imagem')){    
                var imagem = 'data:image/png;base64,'+ data1["valor"];
                document.getElementById(data1["idHtml"]).src = imagem;
            }
            else{

                document.getElementById(data1["idHtml"]).innerHTML = "Média da nota custo: "+ data1["valor"];
            }
           
            
            //ele.src =  'data:image/png;base64,'+ data1["valor"];
            
            }); 
        });
    }
    /*$.ajax({
        url: 'http://127.0.0.1:5000/your_url',
        type: "PUT",
        data : JSON.stringify(your_data),
        contentType:  'application/json' 
    })*/
    /*alert(`${window.origin}/your_url`)
    fetch(`${window.origin}/your_url`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(your_data),
    cache: "no-cache",
    headers: new Headers({
        "content-type": "application/json"
    })
    }).then(function (response){
        if(response.status !==200){
        
            console.log(response)
            return;
        }
        response.json().then(function (data){
            console.log(data)
        })
    })*/
   /* fetch(`${window.origin}/your_url`, {
        method : "PUT", 
        credentials: "include",
        cache: "no-cache",
        body : JSON.stringify( your_data),
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function (response){ 
    
        if(response.ok) {  
    
            response.json() 
            .then(function(response) {
                console.log(response)
            });
        }
        else {
            throw Error('Something went wrong');
        }
    })
    .catch(function(error) {
        console.log(error);
    });*/
    /*fetch(`${window.origin}/your_url`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // data is a parsed JSON object
    })*/
    /*fetch(`${window.origin}/your_url`, {
        method : "POST", 
        credentials: "include",
        cache: "no-cache",
        body : JSON.stringify( your_data),
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function (response){ 
    
        if(response.ok) {  
            
            alert(response.json())
            response.json() 
            .then(function(response) {
                console.log(response)
            });
        }
        else {
            throw Error('Something went wrong');
        }
    })
    .then(data => {
        alert(data)
        // data is a parsed JSON object
    })*/
   
        /*.then(r => r.json())
        .then(r => {
          console.log(r)
          this.setState({
            pyResp: r
          })
        })
        .catch(err => console.log(err))
    */
     
    /*fetch(`${window.origin}/your_url/10`, {
        "method": "POST",
        "body": your_data,
    }).then(function (response){ 
    
        if(response.ok) {  
            
            alert(response.json());
            alert(response)      ;    
            response.json() ;
           
        }
        else {
            throw Error('Something went wrong');
        }
    })
    .then(function (text) {
        alert('GET response:');
        alert(text); 
      });*/

function calcular() {
    obterDados();

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

    fetch(`${window.origin}/GetTreeViewPedidos`, {
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
             
           /* data.forEach(function(data1, index) { 
                var bucket = {};     
                    
                bucket['text'] = data1["text"];
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

                });   */
                $('#comprasId').jstree({
                    'core': {
                        "themes": {
                            "responsive": false
                        },
                        "check_callback": true,
                        'data': data
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
                      
                      /*var jsonData = {};
                      
                      jsonData['pedidoId'] = data["pedidoId"];
                      jsonData['fornecedorId'] = data["fornecedorId"];
                      
                      */
                      var your_data =  data.node.data;
                      console.log(your_data)
                      fetch(`${window.origin}/GetNotaPedidos`, {
                        method: "POST",
                        credentials: "include",
                        body: JSON.stringify(your_data),
                        cache: "no-cache",
                        headers: new Headers({
                            "content-type": "application/json"
                        })
                        }).then(response => response.json())
                        .then(function(dataPedido){ 
                            console.log(dataPedido);
                            
                        })
                    }
                  });
                //$('#comprasId').jstree(true).settings.core.data = data;
                $('#comprasId').jstree(true).refresh();
                $('#comprasId').jstree("open_all");
                $('#comprasId').jstree("deselect_all");
            console.log(jsonData);
        }
            //var jsonData = {};
            );
            
    }

function mostrarValor() {
    alert("texto");
}
function salvarDados(){
    
    dadosArqvore = $("#comprasId").jstree().get_selected(true)[0].data;
    //console.log($("#comprasId").jstree("get_selected").data())
    
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
    jsonData["dadosArvore"] = dadosArqvore;
    var your_data =  jsonData
    return  fetch(`${window.origin}/salvarDados`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(your_data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
        }).then(response => response.json())
        .then(function(data){         
          alert("Salvo com sucesso")

        });
    }
function obterDados(){
    
    $("#crispCriterioDeSelecao").remove();
    $("#imagemCriterioDeSelecao").remove();
    if($("#resumo").height()=='350'){
        $("#resumo").animate({height:'1px'}, 500);
    }
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
            
            $("#resumo").prepend('<img class=\"imagem300c\" id=imagemCriterioDeSelecao src=\"\"><br/>');
            $("#resumo").prepend("<h4 class=textoCentralizado id=crispCriterioDeSelecao>Classificação final</h4>");
            imagemCriterioDeSelecao = 'data:image/png;base64,';
           
            data.forEach(function(data1, index) {
            
            if(data1["idHtml"].includes('imagem')){    
                var imagem = 'data:image/png;base64,'+ data1["valor"];
                document.getElementById(data1["idHtml"]).src = imagem;
            }
            else{
                if(data1["idHtml"]=="crispCriterioDeSelecao")   {
                    console.log(data1["idHtml"])
                    document.getElementById(data1["idHtml"]).textContent = "Média classificação: " +data1["valor"];
                }
                else{
                    document.getElementById(data1["idHtml"]).innerHTML = "Média classificação: "+ data1["valor"];    
                }     
               
                
            }
           
            
            //ele.src =  'data:image/png;base64,'+ data1["valor"];
            
            }); 
            
            //$("#resumo").prepend("<img class='imagem300' id=imagemCriterioDeSelecao src=''>");

            $("#resumo").animate({height:'350px'}, 500);            
   
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
            //aqui alimenta o data do jstree
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
                    console.log(data);
                    console.log(data.node);
                    console.log(data.node.data);
                   
                 if (data != null && data.node != null && data.node.data != []) {
                   
                    document.getElementById("Titulo001").textContent = "Critérios para o: "+ data.node["text"];
                    if($("#resumo").height()=='350'){
                        $("#1001111").remove();
                        $("#resumo").animate({height:'1px'}, 500);
                    }
                    
                    
                    if(data.node.data["fornecedorId"]!=undefined){

                      var your_data =  data.node.data;
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
                           
                            dataPedido.forEach(function(item, index){
                            document.getElementById(item["htmlId"]).value = item["nota"];
                           /* if(item["htmlId"]=="CustoPreco")
                            {
                              console.log(item["htmlId"])
                              console.log(item["nota"])
                              document.getElementById(item["htmlId"]).setAttribute("value", item["nota"]);   
                            }
                            else{
                                console.log(item["htmlId"])
                                console.log(item["nota"])
                                document.getElementById(item["htmlId"]).value = item["nota"];
                            }*/
                          });
                            
                        })
                    }
                    else {
                       // alert("Selecione um fornecedor do pedido")
                    }
                    }
                  });
                //$('#comprasId').jstree(true).settings.core.data = data;
                $('#comprasId').jstree(true).refresh();
                $('#comprasId').jstree("open_all");
                $('#comprasId').jstree("deselect_all");
          
        }
            //var jsonData = {};
            );
            
    }

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

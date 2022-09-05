function mostrarValor() {
    alert("texto");
}
function obterDados(){
    var ele  = document.getElementById("1000114");
    alert(ele.title)
    let subcriterios = []
    subcriterios.push('CustoPreco')
    subcriterios.push('CustoPgto')
    subcriterios.push('CustoReajuste')
    for (let i = 0; i < subcriterios.length; i++) {
        var ele  = document.getElementById(subcriterios[i]);
        alert(ele.value)
        // more statements
      }
    var your_data =  JSON.stringify(subcriterios)
   
    var index = 33;
    fetch(`${window.origin}/your_url`, {
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
            alert(data1["nome"]);
            });
            //return data;
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
   

    j = obterDados()
}

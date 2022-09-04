function mostrarValor() {
    alert("texto");
}
function calcular() {
    let criterios = [];
    criterios.push(['01- Custo', 'crisp']);
    criterios.push(['02- Qualidade','fuzzy']);
    criterios.push(['03- Prazo','fuzzy' ]);
    criterios.push(['04- Gestão', 'fuzzy']);
    criterios.push(['05- Geral', 'fuzzy']);
    //alert(criterios.length);
    console.log(criterios.length);
    //ele = document.getElementById("gdgdgdg");
    //alert(ele.name);

    //alert(ele.tag);
    //ele.style.color = "blue";
       /*for (i = 0; i < criterios.length; i++) {
        alert(criterios[i]);
    }
    alert("texto1");/*/
    var your_data = {
        teste : 'teste'
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
    var index = 33;
    fetch(`${window.origin}/your_url/10`, {
        method: 'GET',
        mode:'no-cors',
        dataType: 'json'
      })
        .then(r => r.json())
        .then(r => {
          console.log(r)
          this.setState({
            pyResp: r
          })
        })
        .catch(err => console.log(err))
    
     
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
}

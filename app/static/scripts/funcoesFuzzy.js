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
    alert(criterios.length);
    console.log(criterios);
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
    $.ajax({
        url: 'http://127.0.0.1:5000/your_url',
        type: "PUT",
        data : JSON.stringify(your_data),
        contentType:  'application/json' 
    })
    /*fetch(`${window.origin}/your_url`, {
    method: "GET",
    credentials: "include",
    body: JSON.stringify(your_data),
    cache: "no-cache",
    headers: new Headers({
        "content-type": "application/json"
    })
    }).then(function (response){
        if(response.status !==200){
        return;
        }
        response.json().then(function (data){
            console.log(data)
        })
    })*/
}

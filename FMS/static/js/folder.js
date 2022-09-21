$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            type:"GET",
            url:"user_folder/",
            success: function(data){
                
                for(element in data.folder){
                    document.getElementById('append-folder').innerHTML +=
                    `
                    <a class="filename text-dark" href="${element.name}">${element.name}<i class="bi-folder text-warning"></i></a>
                    ` 
                };
            }
        })
    }, 1000)

})
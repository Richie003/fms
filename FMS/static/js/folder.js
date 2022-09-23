$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            type:"GET",
            url:"user_folder/",
            success: function(data){
                
                for(var obj in data.folder){
                    document.getElementById('append-folder').innerHTML +=
                    `
                    <a class="filename text-dark" href="${data.folder[obj].name}">${data.folder[obj].name}<i class="bi-folder text-warning"></i></a>
                    ` 
                };
            }
        })
    }, 1000)

})

console.log('hello world 3')

var folderBtns = document.getElementsByClassName('get_folder')
var quantity = document.getElementById('inputQuantity')

for (var i = 0; i < folderBtns.length; i++){
    folderBtns[i].addEventListener('click', function(){
        var folderId = this.dataset.folder
        console.log('folderId:', folderId)

        console.log('User:', user)
            updateUserOrder(folderId)
    })
}

function updateUserOrder(folderId){
    console.log('User is logged in, Processing...')

        var url = ''

        fetch(url, {
            method: 'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'folderId':folderId})
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data)
        });
}
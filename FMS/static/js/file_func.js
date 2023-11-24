// Start
    function getCookie(name){
        var cookieValue = null;
        if (document.cookie && document.cookie !== ''){
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++){
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')){
                    cookieValue = decodeURIComponent(cookie.substring(
                        name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function removeFile(fileURL, redirectURL) {
        /* The code you provided is making an XMLHttpRequest to the server to delete a file. */
        const csrftoken = getCookie('csrftoken');
        let xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE){
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
                    window.location.replace(redirectURL);
                }else{
                    alert('there was an error');
                }
            }
        }
        xmlhttp.open("DELETE", fileURL, true);
        xmlhttp.setRequestHeader("X-CSRFToken", csrftoken)
        xmlhttp.send();
    };
//
    function userFileOptions(element) {
    /* The code you provided is toggling the visibility of an element with the id 'Fileoption-dropdown'. */
        var userFileOptionvar = document.getElementById('Fileoption-dropdown')

        if (userFileOptionvar.classList.contains('d-none')){
            userFileOptionvar.classList.remove('d-none')
        }else{
            userFileOptionvar.classList.add('d-none')
        }
    }
//
    function selectOption(params) {
/* The code you provided is toggling the visibility of elements with the class name 'selector' and the
element with the id 'delete-all'. */
        var selecTor = document.getElementsByClassName('selector')
        var deleteAllBtn = document.getElementById('delete-all')
        for (let index = 0; index < selecTor.length; index++) {
            if (selecTor[index].classList.contains('d-none')){
                selecTor[index].classList.remove('d-none')
            }else{
                selecTor[index].classList.add('d-none')
            }
        }
        if(deleteAllBtn.classList.contains('d-none')){
            deleteAllBtn.classList.remove('d-none')
        }else{
            deleteAllBtn.classList.add('d-none')
        }
    }
//
// Sends the selected file(s) ids to the server side via an ajax `POST` request to delete from the database
$( document ).ready(function() {
    $('.delete_all_form').submit(function(e){
        e.preventDefault()
        /* In the given code, `const url = $(this).attr('action')` is retrieving the value of the
        `action` attribute from the form element that triggered the event. */
        const url = $(this).attr('action')
        /* The code is selecting all the checkboxes that are checked and retrieving their values. It then
        pushes these values into an array called `selectedValues`. */
        var selectedValues = [];
        $('input[type="checkbox"]:checked').each(function() {
            selectedValues.push($(this).val());
        });
        /* The code snippet is making an AJAX POST request to the server. */
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'files_ids': selectedValues,
            },
            success: function(response) {
                console.log('Deleted', response)
                setTimeout(function(){
                    location.reload();
                }, 2000);
            },
            error: function(response) {
                console.log('error', response)
            }
        })
    })
    // 
});
// Copy to clipboard funct
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
    .then(() => {
        console.log('Text copied to clipboard: ', text);
    })
    .catch(err => {
        console.error('Unable to copy text to clipboard: ', err);
    });
}
//
function shareFile(e){
    /*Sends the target file id to the server side and gets the unique share url as a response */
    const dataId = $(e).attr('data-fileID');
    const dataUrl = $(e).attr('data-url');
    $.ajax({
        url: dataUrl,
        type:"GET",
        data: {
            Id: dataId
        },
        success: function(data) {
        copyToClipboard(data.res);
        }
    });
}
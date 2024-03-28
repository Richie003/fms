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
// Copy to clipboard function
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
        alert(`Share link Copied to clipboard`)
        }
    });
}

// File search/filter algorithm
/* The above code is a JavaScript code snippet that handles the keyup event on an input field with the
id "search-input". */
$('#search-input').keyup((e)=>{
    const searchData = e.target.value;
    const folder_name = $('#folder_name').text();
    const initialContainer = $('#initial-container');
    const resultContainer = $('#result-container');
    resultContainer.empty();
    $.ajax({
        type:'GET',
        url:`/search/`,
        data:{
            "search_type":"files",
            "dts":searchData,
            "folder":folder_name
        },
        success: (response)=>{
            console.log(response)
            if(searchData != ""){
                response.res.forEach(function(i){
                    console.log()
                    const resultData = `
                    <div class="media text-muted pt-3">
                        <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                            <div class="d-flex justify-content-between align-items-center w-100">
                                <div class="w-50" id="fileN-box">
                                    <input type="checkbox" name="checked-file" value="${i["pk"]}" id="checked_all" class="d-none selector" checked>
                                    <span class="filename text-gray-dark font-weight-bolder">${i["filename"]}</span>
                                </div>
                                <div class="">
                                <button class="btn btn-sm btn-light px-2 flex-shrink-0 get_folder" type="button" onclick="removeFile('/delete/file/${i["pk"]}', '/folder/${i["folder"]}')">
                                <svg xmlns="http://www.w3.org/2000/svg" height="20" width="15" viewBox="0 0 448 512">
                                    <path d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12
                                    12 0 0 0-12 12v216a12 12 0 0 0 12 12zM432
                                    80h-82.41l-34-56.7A48 48 0 0 0 274.41 0H173.59a48 48 0 0 0-41.16 23.3L98.41 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48
                                    48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0-16-16zM171.84 50.91A6 6 0 0 1 177 48h94a6 6 0 0 1 5.15 2.91L293.61 80H154.39zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12z" fill="#ff0000"/>
                                </svg>
                                </button>
                                <a class="btn btn-sm btn-light buttss" href="/download/${i["filename"]}/${i["folder"]}" id="new_file" type="button">
                                    <svg xmlns="http://www.w3.org/2000/svg" height="20" width="15" viewBox="0 0 512 512">
                                        <path d="M216 0h80c13.3 0 24 10.7 24 24v168h87.7c17.8 0 26.7 21.5 14.1 34.1L269.7 378.3c-7.5 7.5-19.8 7.5-27.3 0L90.1 226.1c-12.6-12.6-3.7-34.1 14.1-34.1H192V24c0-13.3 10.7-24 24-24zm296 376v112c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V376c0-13.3 10.7-24 24-24h146.7l49 49c20.1 20.1 52.5 20.1 72.6 0l49-49H488c13.3 0 24 10.7 24 24zm-124 88c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20zm64 0c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20z" fill="#00e7ff"/>
                                    </svg>
                                </a>
                                <a class="btn btn-sm btn-light" data-url="/sharefile/" data-fileID="${i["pk"]}" id="liveToastBtn" onclick="shareFile(this)" >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-link-45deg" viewBox="0 0 16 16">
                                        <path d="M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1.002 1.002 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4.018 4.018 0 0 1-.128-1.287z"/>
                                        <path d="M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243L6.586 4.672z"/>
                                    </svg>
                                </a>
                                </div>
                            </div>
                            <span class="d-block">Uploaded~${i["created"]}</span>
                        </div>
                    </div>
                `
                resultContainer.append(resultData);
                resultContainer.removeClass('d-none');
                initialContainer.addClass('d-none');
                })
            }else{
                resultContainer.addClass('d-none');
                initialContainer.removeClass('d-none');
            }
        },
        error: (response)=>{
            console.log('Error')
        }
    })
})

/**
 * The function getCurrentDate returns the current date in the format MM/DD/YY.
 * @returns The function `getCurrentDate` returns the current date in the format "MM/DD/YY".
 */
function getCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
    var yy = String(today.getFullYear()).substr(-2);

    return mm + '/' + dd + '/' + yy;
}

// jQuery/AJax POST request to create sub_folder
/* The above code is a JavaScript snippet that handles a click event on an element with the id
"folder-btn". When the element is clicked, it sends a POST request to the "/subfolder/" endpoint
with some data including the CSRF token, the value of an input field with id "sub_folder", and the
text content of an element with id "folder_name". */
$("#folder-btn").click((e)=>{
    $.ajax({
        type:"POST",
        url:"/subfolder/",
        data:{
            "csrfmiddlewaretoken":getCookie('csrftoken'),
            "folder":$("#sub_folder").val(),
            "parent_folder":$('#folder_name').text(),
        },
        success: (response) => {
            var getDate = getCurrentDate();
            if(response.res === 'success'){
                $(".bg-modal4").css("display", "none !important");
                $("#sub-folder-container").append(
                    `
                    <div class="col-xl-4 col-sm-6">
                    <div class="card shadow-none border">
                    <div class="card-body p-3">
                    <div class="">
                    <div class="d-flex justify-content-between align-items-center">
                    <div>
                    <i class="bx bxs-folder h1 mb-0 text-warning"></i>
                    </div>
                    <div class="avatar-group">
                    <div class="avatar-group-item">
                    <a href="javascript: void(0);" class="d-inline-block">
                    <div class="avatar-sm">
                    <span class="avatar-title rounded-circle bg-info text-white font-size-16">
                    Y
                    </span>
                    </div>
                    </a>
                    </div>
                    <div class="avatar-group-item">
                        <a href="javascript: void(0);" class="d-inline-block">
                        <div class="avatar-sm">
                        <span class="avatar-title rounded-circle bg-info text-white font-size-16">
                        O
                        </span>
                        </div>
                        </a>
                        </div>
                        <div class="avatar-group-item">
                            <a href="javascript: void(0);" class="d-inline-block">
                            <div class="avatar-sm">
                            <span class="avatar-title rounded-circle bg-info text-white font-size-16">
                            U
                            </span>
                            </div>
                            </a>
                            </div>
                    </div>
                    </div>
                    <div class="d-flex justify-content-between mt-3">
                    <div class="overflow-hidden me-auto">
                    <h5 class="font-size-15 text-truncate mb-1"><a href="javascript: void(0);" class="text-body">${$("#sub_folder").val()}</a></h5>
                    <p class="text-muted text-truncate mb-0">20 Files</p>
                    </div>
                    <div class="align-self-end">
                    <p class="text-muted mb-0 font-size-13"><i class="mdi mdi-clock"></i>${getDate}</p>
                    </div>
                    </div>
                    </div>
                    </div>
                    </div>
                    </div>
                    `
                )
            }
        },
        error: () => {
            console.log("An error occurred")
        }
    });
});

// Dropzone functionality
Dropzone.autoDiscover = false;

const theDropZone = new Dropzone(".custom-dz", {
    url:"/dropzone_file/",
    maxFiles:5,
    maxFilesize:350,
    acceptedFiles: ".docx, .pdf, .ppt, .pptx, .xlsx, .txt, .png, .jpg, .jpeg, .mp3, .mp4, .py, .js, .html, .css, .scss, .zip"
})
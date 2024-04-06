/* The code block you provided is using jQuery to execute a function when the document is ready. Inside
this function, there is a setInterval function that repeatedly makes an AJAX GET request to the
"user_folder/" URL every 1000 milliseconds (1 second). */
// $(document).ready(function(){
//     setInterval(function(){
//         $.ajax({
//             type:"GET",
//             url:"user_folder/",
//             success: function(data){
//                 const idle = `<a class="filename text-dark" href="${data.folder[obj].name}">${data.folder[obj].name}<i class="bi-folder text-warning"></i></a>` 
//                 for(var obj in data.folder){
//                     document.getElementById('append-folder').innerHTML += idle
//                 };
//             }
//         })
//     }, 1000)

// })

/**
 * The function `getCookie` retrieves the value of a specific cookie by its name from the document's
 * cookies.
 * @param name - The `name` parameter is the name of the cookie you want to retrieve the value for.
 * @returns the value of the cookie with the specified name.
 */
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

/**
 * The function `removeFolder` sends a DELETE request to the specified `folderURL` and redirects to
 * `redirectURL` if the request is successful.
 * @param folderURL - The `folderURL` parameter is the URL of the folder that you want to
 * remove/delete. It should be a string representing the URL of the folder resource on the server.
 * @param redirectURL - The `redirectURL` parameter is the URL where the user will be redirected after
 * the folder is successfully removed.
 */
function removeFolder(folderURL, redirectURL) {
    const csrftoken = getCookie('csrftoken');
    let xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE){
            if (xmlhttp.status == 200){
                window.location.replace(redirectURL);
            }else{
                alert('there was an error');
            }
        }
    }
    xmlhttp.open("DELETE", folderURL, true);
    xmlhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xmlhttp.send();
}


$('#search-input').keyup((e)=>{
    const searchData = e.target.value;
    const initialContainer = $('#initial-container');
    const resultContainer = $('#result-container');
    resultContainer.empty();
    $.ajax({
        type:'GET',
        url:`/search/`,
        data:{
            search_type:"folders",
            dts:searchData,
        },
        success: (response)=>{
            if(searchData != ""){
                for(i of response.res){
                    const resultData = `
                    <div class="media text-muted pt-3">
                        <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                            <div class="d-flex justify-content-between align-items-center w-100" id="append-folder">
                                <a class="filename text-dark font-weight-bold" href="/folder/${i["folder"]}"><i class="bi-folder text-warning"></i> ${i["folder"]}</a>
                                <div class="">
                                    <button class="btn btn-sm btn-light px-2 flex-shrink-0 get_folder" type="button"
                                        data-folder='${i["folder"]}' onclick="removeFolder()">
                                        <svg xmlns="http://www.w3.org/2000/svg" height="20" width="15" viewBox="0 0 448 512">
                                            <path d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12
                                            12 0 0 0-12 12v216a12 12 0 0 0 12 12zM432
                                            80h-82.41l-34-56.7A48 48 0 0 0 274.41 0H173.59a48 48 0 0 0-41.16 23.3L98.41 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48
                                            48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0-16-16zM171.84 50.91A6 6 0 0 1 177 48h94a6 6 0 0 1 5.15 2.91L293.61 80H154.39zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12z" fill="#ff0000"/>
                                        </svg>
                                    </button>
                                    <button class="btn btn-sm btn-light buttss position-relative" id="new_file" onclick="userOptions(this, )"
                                            data-val=${i["folder"]} type="button">
                                            <svg xmlns="http://www.w3.org/2000/svg" height="20" width="15" viewBox="0 0 448 512">
                                                <path d="M352 240v32c0 6.6-5.4 12-12 12h-88v88c0 6.6-5.4 12-12 12h-32c-6.6 0-12-5.4-12-12v-88h-88c-6.6 0-12-5.4-12-12v-32c0-6.6 5.4-12 12-12h88v-88c0-6.6 5.4-12 12-12h32c6.6 0 12 5.4 12 12v88h88c6.6 0 12 5.4 12 12zm96-160v352c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V80c0-26.5 21.5-48 48-48h352c26.5 0 48 21.5 48 48zm-48 346V86c0-3.3-2.7-6-6-6H54c-3.3 0-6 2.7-6 6v340c0 3.3 2.7 6 6 6h340c3.3 0 6-2.7 6-6z" fill="#00e7ff"/>
                                            </svg>
                                            <div class="primary-bg px-3 py-2 d-none" id="option-dropdown-${i["Id"]}" style="
                                                position: absolute;
                                                transform: translate3d(-29px, 36px, 0px);
                                                top: 0px;
                                                right: 0px;
                                                will-change: transform;
                                                z-index: 3;
                                                border-radius: 43px 1px 24px 25px;
                                            ">
                                            <div class="dropdown-header text-white" style="cursor: text">
                                                Options For You:
                                            </div>
                                            <a class="dropdown-item d-flex justify-content-between align-items-center text-dark" href="#">Share
                                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="20" style="margin-left: 8px" viewBox="0 0 448 512">
                                                <path d="M352 320c-22.608 0-43.387 7.819-59.79 20.895l-102.486-64.054a96.551 96.551 0 0 0 0-41.683l102.486-64.054C308.613 184.181 329.392 192 352 192c53.019 0 96-42.981 96-96S405.019 0 352 0s-96 42.981-96 96c0 7.158.79 14.13 2.276 20.841L155.79 180.895C139.387 167.819 118.608 160 96 160c-53.019 0-96 42.981-96 96s42.981 96 96 96c22.608 0 43.387-7.819 59.79-20.895l102.486 64.054A96.301 96.301 0 0 0 256 416c0 53.019 42.981 96 96 96s96-42.981 96-96-42.981-96-96-96z"></path>
                                                </svg>
                                            </a>
                                            <a class="dropdown-item d-flex justify-content-between align-items-center text-dark" onclick="handleClick(this)">
                                                <i class="bi bi-paperclip font-weight-bold h4 text-light"></i>
                                                From Device
                                            </a>
                                            <div class="dropdown-divider"></div>
                                            <a class="dropdown-item d-flex justify-content-between align-items-center text-dark" href="#">Settings
                                                <i class="bi bi-dropbox"></i>
                                            </a>
                                            </div>
                                    </button>
                                </div>
                            </div>
                            <span class="d-block">${i["created"]}</span>
                        </div>
                    </div>
                `
                resultContainer.append(resultData);
                resultContainer.removeClass('d-none');
                initialContainer.addClass('d-none');
                }
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
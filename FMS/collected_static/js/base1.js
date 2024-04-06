/* This code is written in JavaScript and it is using the jQuery library. */
$(document).ready(() => {
    /**
     * The code listens for a keydown event and if the Ctrl key and the '/' key are pressed, it toggles the
     * visibility of a search container.
     */

    /* The code `$(document).keydown((event) => { ... })` is attaching a keydown event listener to the
    entire document. */
    $(document).keydown((event) => {
        if (event.ctrlKey && event.key === '/') {
            toggleSearchContainer();
        }
    });

    /* The code `$("#generate").click(() => { toggleSearchContainer(); });` is attaching a click event
    listener to the element with the id "generate". */
    $("#generate").click(() => {
        toggleSearchContainer();
    });

    /**
     * The function toggleSearchContainer toggles the visibility of the search container by adding or
     * removing classes and updating a data attribute.
     */
    function toggleSearchContainer() {
        const openedORclosed = $("#search-cont").attr('data-boolean');
        if (openedORclosed === "False") {
            $("#search-cont").removeClass('invincible').addClass('opaque').attr('data-boolean', 'True');
        } else {
            $("#search-cont").addClass('invincible').removeClass('opaque').attr('data-boolean', 'False');
        }
    }

});
// 
/**
 * The handleClick function displays a modal by changing the style of the ".bg-modal" element to
 * "display:flex!important;", while the cancelClick function hides the modal by changing the style to
 * "display:none!important;".
 * @param element - The `element` parameter represents the HTML element that triggered the click event.
 */
function handleClick(element) {
    document.querySelector(".bg-modal").style = "display:flex!important;";
}
function cancelClick(element) {
    document.querySelector(".bg-modal").style = "display:none!important;";
    // const addFileForm = document.getElementById('add-file')
}
// For the share button
/**
 * The above JavaScript code defines two functions, handleShareClicker and cancelShareClicker, which
 * respectively display and hide a modal with the class "bg-modal2".
 * @param element - The "element" parameter is a reference to the HTML element that triggered the click
 * event. It is passed to the functions as an argument when the click event occurs.
 */
function handleShareClicker(element) {
    document.querySelector(".bg-modal2").style = "display:flex!important;";
}
function cancelShareClicker(element) {
    document.querySelector(".bg-modal2").style = "display:none!important;";
}
// End

/**
 * The above JavaScript code defines two functions, `folderFormTrigger` and `folderFormCancel`, which
 * control the display of a modal window.
 * @param element - The "element" parameter is a reference to the HTML element that triggered the
 * function. It is used to identify which element was clicked or interacted with in order to perform
 * the desired action.
 */
function folderFormTrigger(element) {
    document.querySelector(".bg-modal4").style = "display:flex!important;";
}

function folderFormCancel(element) {
    document.querySelector(".bg-modal4").style = "display:none!important;";
}

/**
 * The function toggles the visibility of an element with the id "option-dropdown" when called.
 * @param element - The parameter "element" is not used in the given code snippet. It seems to be
 * unused and can be removed from the function definition.
 */
function userOptions(element, Id) {
    var userOptionvar = document.getElementById(`option-dropdown-${Id}`);

    if (userOptionvar.classList.contains("d-none")) {
        userOptionvar.classList.remove("d-none");
    } else {
        userOptionvar.classList.add("d-none");
    }
}

function loadpage(time) {
    setTimeout("location.reload(true);", time);
}

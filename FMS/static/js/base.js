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

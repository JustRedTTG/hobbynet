// Function to get the value of a query parameter from the URL
function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Function to remove the query parameter from the URL without refreshing the page
function removeQueryParam(name) {
    const url = new URL(window.location.href);
    url.searchParams.delete(name);
    window.history.replaceState({}, document.title, url.toString());
}

$(document).ready(function () {
    // Configure Toastr options
    toastr.options.positionClass = "toast-top-center";
    toastr.options.closeButton = true;

    // Check if the query parameter "success" is present
    const successParam = getQueryParam("success");
    if (successParam) {
        // Display Toastr notification
        toastr.success("Operation completed successfully");

        // Remove the query parameter from the URL without refreshing the page
        removeQueryParam("success");
    }
});
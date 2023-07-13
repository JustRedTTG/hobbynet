$(document).ready(function () {
    toastr.options.positionClass = "toast-top-center";
    toastr.options.closeButton = true;

    const deleteParam = getQueryParam("delete");
    if (deleteParam) {
        const deleteButton = $('#btn-delete');
        if (deleteButton.length === 0) {
            toastr.error("You don't have permission to delete this resource.");
        } else {
            deleteButton.click();
        }
        removeQueryParam("delete");
    }
});
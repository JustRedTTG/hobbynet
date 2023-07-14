$(document).ready(function () {
    function toggleClearImage(shouldShow) {
        if (shouldShow) {
            $('#post-image-clear').show();
        } else {
            $('#post-image-clear').hide();
        }
    }

    $('#post-image-icon').click(function () {
        $('#id_image').click();
    });

    $("#id_image").change(function () {
        var file = this.files[0];
        var reader = new FileReader();

        reader.onload = function (e) {
            $("#id_image_image").attr("src", e.target.result);
            toggleClearImage(true);
        };

        reader.readAsDataURL(file);
    });

    $('#post-image-clear').on('click', function () {
        // Reset the file input element
        $('#id_image').val(null);
        toggleClearImage(false);
        $("#id_image_image").attr("src", '');
    });
});
$(document).ready(function () {
    function toggleClearProfilePicture(shouldShow) {
        if (shouldShow) {
            $('#id_profile_picture_clear').show();
        } else {
            $('#id_profile_picture_clear').hide();
        }
    }

    $("#id_profile_picture_image").click(function () {
        $("#id_profile_picture").click();
    });

    $("#id_profile_picture").change(function () {
        var file = this.files[0];
        var reader = new FileReader();

        reader.onload = function (e) {
            $("#id_profile_picture_image").attr("src", e.target.result);
            toggleClearProfilePicture(true);
        };

        reader.readAsDataURL(file);
    });
    $('#id_profile_picture_clear').on('click', function () {
        // Reset the file input element
        $('#id_profile_picture').val(null);
        toggleClearProfilePicture(false);
        $("#id_profile_picture_image").attr("src", static_src_blank);
    });
    if ($("#id_profile_picture").get(0).files.length === 0 && $("#id_profile_picture_image").attr("src").includes(static_src_blank)) {
        toggleClearProfilePicture(false);
    }
});
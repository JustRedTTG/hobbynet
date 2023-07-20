$(document).ready(function () {
    $('[type="submit"]').on('click', function () {
        let form = $(this).closest('form');

        if (form[0].checkValidity() && !$(this).prop('submit-triggered')) {
            let spinner = $('<div>', {
                'role': 'status',
                'class': 'spinner-border spinner-border-sm ml-2 submit-button-spinner',
            });
            $(this).prop('submit-triggered', true);
            setTimeout(function () {
                $(this).prop('type', 'button');
            }, 0);
            $(this).append(spinner);
        }
    });
});

function copyToClipboard(target, url) {
    navigator.clipboard.writeText(url)
        .then(function () {
            $(target).tooltip("show");
            setTimeout(function () {
                $(target).tooltip("hide");
            }, 2000);
        })
        .catch(function (error) {
            console.error('Failed to copy text to clipboard: ', error);
        });
}


$(document).ready(function () {
    $('[data-toggle="copyurl"]').click(function (e) {
        e.preventDefault();
        var url = $(this).data("url");
        copyToClipboard(this, url);
    });
    $('[data-toggle="copyurl"]').tooltip({
        trigger: 'manual',
        placement: 'auto',
        title: "Copied!"
    });
    $('[data-toggle="copyhref"]').click(function (e) {
        e.preventDefault();
        var href = $(this).data("href");
        copyToClipboard(this, document.location.origin + href);
    });
    $('[data-toggle="copyhref"]').tooltip({
        trigger: 'manual',
        placement: 'auto',
        title: "Copied!"
    });
});
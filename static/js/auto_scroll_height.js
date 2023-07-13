$(document).ready(function () {
    $(".auto-scroll-height").on("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });
});
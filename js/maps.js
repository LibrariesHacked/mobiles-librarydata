$(function () {
    // Firstly load up the services
    mobiles.loadServices(function (services) {
        $.each(services, function (i, s) {
            $('#sel-services').append($('<option>', {
                value: s.code,
                text: s.authority
            }));
        });
    });
});
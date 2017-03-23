$(function () {
    // firstly load up the services
    mobiles.loadServices(function (services) {
        $.each(services, function (i, s) {
            $('#sel-services').append($('<option>', {
                value: s.code,
                text: s.authority
            }));
        });

        // event: select authority
        $('#sel-services').on('change', function (e) {
            var s = mobiles.getService($(e.target).val());
        });

    });
});
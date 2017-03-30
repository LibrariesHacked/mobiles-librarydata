$(function () {


    // Get the mini map up.


    // Load up the services
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
            $('#div-count-mobiles p').text(s.count);
            $('#div-count-mobiles').show();
            if (parseInt(s.count) > 0) {
                $('#div-website a').attr('href', s.website);
                $('#div-website').show();
            }
        });
    });
});
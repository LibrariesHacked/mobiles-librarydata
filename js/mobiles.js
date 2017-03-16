var mobiles = {
    services: [],
    /////////////////////////////////////////////////
    // Function: LoadServices
    /////////////////////////////////////////////////
    loadServices: function (callback) {
        Papa.parse(config.servicesfile, {
            download: true,
            complete: function (results) {
                this.services = results;
                callback(services);
            }
        });
    },
    getMobileData: function (service, mobile) {

    }
};
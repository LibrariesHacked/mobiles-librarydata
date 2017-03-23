var mobiles = {
    services: {},
    /////////////////////////////////////////////////
    // Function: loadServices
    /////////////////////////////////////////////////
    loadServices: function (callback) {
        Papa.parse(config.servicesfile, {
            download: true,
            header: true,
            complete: function (results) {
                for (x = 0; x < results.data.length; x++) this.services[results.data[x].code] = results.data[x]; 
                callback(this.services);
            }.bind(this)
        });
    },
    /////////////////////////////////////////////////
    // Function: getService
    /////////////////////////////////////////////////
    getService: function (service) {
        return this.services[service];
    },
    /////////////////////////////////////////////////
    // Function: getMobileData
    /////////////////////////////////////////////////
    getMobileData: function (service, mobile) {

    }
};
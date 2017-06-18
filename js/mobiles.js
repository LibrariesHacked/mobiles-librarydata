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

    },
    extractHostname: function (url) {
        var hostname;
        url.indexOf("://") > -1 ? hostname = url.split('/')[2] : hostname = url.split('/')[0];
        hostname = hostname.split(':')[0];
        hostname = hostname.split('?')[0];
        hostname = hostname.replace('www.', '');
        return hostname;
    }
};
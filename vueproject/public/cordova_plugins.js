cordova.define('cordova/plugin_list', function(require, exports, module) {
  module.exports = [
    {
      "id": "ptest01.ptest",
      "file": "plugins/ptest01/www/ptest.js",
      "pluginId": "ptest01",
      "clobbers": [
        "cordova.plugins.ptest"
      ]
    }
  ];
  module.exports.metadata = {
    "ptest01": "1.0.0"
  };
});
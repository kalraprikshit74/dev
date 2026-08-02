let spaceURL = "";
let spaceURLForWS = "";
let federatedURL = "";
let dashboardURL = "";

export function getLoginUser() {
  return new Promise((resolve, reject) => {
    requirejs(["DS/PlatformAPI/PlatformAPI"], function (PlatformAPI) {
      let user = PlatformAPI.getUser();
      user = user.login;
      resolve(user);
    });
  });
}

export function get3DSpaceURLWS() {
  return new Promise((resolve, reject) => {
    if (spaceURLForWS.length > 0) {
      resolve(spaceURLForWS);
      return;
    }
    requirejs(["DS/PlatformAPI/PlatformAPI"], function (PlatformAPI) {
      let appConfigs = PlatformAPI.getAllApplicationConfigurations();

      for (let index = 0; index < appConfigs.length; index++) {
        if (appConfigs[index]["propertyKey"] === "app.urls.myapps") {
          let url = appConfigs[index]["propertyValue"];
          spaceURLForWS = url;
          break;
        }
      }
      resolve(spaceURLForWS);
    });
  });
}

export function makeWSCall(
  url,
  httpMethod,
  loginTicket,
  ReqBody,
  userCallbackOnComplete,
  userCallbackOnFailure
) {
  requirejs(["DS/WAFData/WAFData"], function (WAFData) {
    let queryobject = {};
    queryobject.method = httpMethod;
    queryobject.timeout = 700000;
    queryobject.type = "jsonp";
    queryobject.crossOrigin = true;
    queryobject.headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };
    queryobject.data = ReqBody;
    queryobject.onComplete = function (dataResp) {
      userCallbackOnComplete(dataResp);
    };
    queryobject.onFailure = function (error, response, headers) {
      console.log("Error in calling url: " + url);
      console.error("Error Data: " + response);
      userCallbackOnFailure(error, response, headers);
    };
    WAFData.authenticatedRequest(url, queryobject);
  });
}

export function getImgUrl(imgName) {
  let appUrl = widget.getUrl();
  appUrl =
    appUrl.substring(0, appUrl.lastIndexOf("/")) + "/assets/images/" + imgName;
  return appUrl;
}

export function loadServiceUrls() {
  return new Promise((resolve, reject) => {
    let onComplete = function (data) {
      data = JSON.parse(data);
      let services = data["platforms"][0]["services"];
      services.forEach((item) => {
        if (item.id === "search") {
          federatedURL = item.url;
        }
        if (item.id === "3ddashboard") {
          dashboardURL = item.url;
        }
        if (item.id === "space") {
          spaceURL = item.url;
        }
      });
      resolve(services);
    };
    let urlPromise = get3DSpaceURLWS();
    urlPromise.then((url) => {
      url = url + "/resources/AppsMngt/api/v1/services";
      makeWSCall(url, "GET", "", {}, onComplete);
    });
  });
}

export function getFederatedURL() {
  return new Promise((resolve, reject) => {
    if (federatedURL.length > 0) {
      resolve(federatedURL);
    } else {
      let promise = loadServiceUrls();
      promise.then((data) => {
        resolve(federatedURL);
      });
    }
  });
}

export function getSpaceURLLink() {
  return new Promise((resolve, reject) => {
    if (spaceURL.length > 0) {
      resolve(spaceURL); //return;
    } else {
      let promise = loadServiceUrls();
      promise.then((data) => {
        resolve(spaceURL);
      });
    }
  });
}

export function getSecurityContext(options) {
  return new Promise((resolve, reject) => {
    get3DSpaceURLWS().then((url) => {
      url =
        url +
        "/resources/modeler/pno/person?current=true&select=preferredcredentials&select=collabspaces";
      var onComplete = function (dataResp) {
        resolve(dataResp);
      };
      var onFailure = function (error, response, headers) {
        console.log("Error in calling url: " + url);
        console.error("Error Data: " + response);
      };
      makeWSCall(url, "GET", "", {}, onComplete, onFailure);
    });
  });
}

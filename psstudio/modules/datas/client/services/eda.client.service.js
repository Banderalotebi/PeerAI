"use strict";

angular.module("app.projectDatas").factory("Eda", ["$resource","$http",
  function ($resource,$http) {
    this.startEda = startEda($resource);
    this.getFeatureInfo = getFeatureInfo($resource);
    this.getEdaProgress = getEdaProgress($resource);
    this.genarateEdaGraph = genarateEdaGraph($http);
    this.getEdaData = getEdaData($resource);

    function startEda($resource){
      return $resource("/api/projects/:projectId/eda", {
        projectId: "@pId"
      },{
        query:{
          method:"GET",
          isArray:true
        }
      });
    }

    function getFeatureInfo(){
      return $resource("/api/projects/:projectId/eda/feature", {
        featureName: "@pId"
      },{
        query:{
          method:"GET",
          isArray:true
        }
      });
    }

    function getEdaProgress($resource){
      return $resource("/api/projects/:projectId/edaprogress", {
        projectId: "@pId"
      },{
        query:{
          method:"GET",
          isArray:true
        }
      });
    }

    function getEdaData($resource){
      return $resource("/api/eda/:edaId/info", {
        edaId: "@edaId"
      },{
        query:{
          method:"GET",
          isArray:false
        }
      });
    }

    function genarateEdaGraph($http){
    }
    return this;
  }
]);

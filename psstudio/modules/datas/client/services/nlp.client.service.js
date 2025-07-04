"use strict";

angular.module("app.projectDatas").factory("nlpService", [function () {

    var nlpService = {};
    //Nlp languages
    nlpService.nlpLanguages = ["English","Portuguese"];
    nlpService.nFeatureCounts = [50,100,150,200];

    return nlpService;
  }
]);

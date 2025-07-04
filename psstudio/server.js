"use strict";

/**
 * Module dependencies.
 */
global.__basedir = __dirname;
var app = require("./config/lib/app");
var server = app.start();

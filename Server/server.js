
var express = require('express');
var https = require('https');
var http = require('http');
var bodyParser = require('body-parser')
var sleep = require('sleep');


var MongoClient = require('mongodb').MongoClient
  , assert = require('assert');

// Connection URL
//ex mongodb://localhost:27017/h2pro
var url = 'yours here';


MongoClient.connect(url, function(err, db) {
  var app = express();


  app.use( bodyParser.json() );       // to support JSON-encoded bodies
  app.use(bodyParser.urlencoded({
    extended: true
  }));
  //general url
  app.get('/', function(req, res){
    var userCreds = db.collection('cred');
    userCreds.findOne({"_id": req.user}, function(err, data) {
      console.log(data);
      res.send(data);
    });
  });
  //path used for verification
  app.get('/verify', function(req, res){
    var userCreds = db.collection('cred');
    console.log(req.query.user);
    userCreds.findOne({"_id": req.query.user}, function(err, data) {
      console.log(err);
      if (data == null) {
        res.send({"authenticated" : false, "found"  :true});
        return;
      }
      if (data._id == req.query.user) {
        if (data.pass == req.query.pass) {
          res.send({"authenticated" : true, "found"  :true});
          return;
        } else {
          res.send({"authenticated" : false, "found"  :true});
          return;
        }
      //user not found in database
      } else {
        res.send({"authenticated" : false, "found"  :false});
        return;
      }
    });
  });
  app.get('/register', function(req, res){
    var userCreds = db.collection('cred');
    console.log(req.query.user);
    userCreds.findOne({"_id": req.query.user}, function(err, data) {
      console.log(err);

      if (data == null) {
        userCreds.save({"_id":req.query.user, "pass":req.query.pass}, function(err, status) {
          console.log(err);
          if (status != null) {
            res.send({"status":"success","error":"none"});
          }
        });

      } else {
        res.send({"status":"failure","error":"exists"});
        return;
      }

    });
  });


  app.listen(3000);

});
// Use connect method to connect to the server

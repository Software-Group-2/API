//var http = require('http');

const express = require("express");
const app = express();

app.get("/", (req,res) => {
  console.log(req.url)
  res.send("<h1> Hello </h1>")
});

app.get("/old", (req,res) =>{
  res.redirect(301, "/new")
});

app.get("/new", (req,res) =>{
  res.send("<h2> NEW </h2>")
});


/*http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end('Hello World!');
}).listen(8080);*/


app.listen(3000, err =>{
  if (err) {
    console.log("There was a problem", err)
    return;
  }
  console.log("listening on port 3000")
} );
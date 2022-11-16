# API

We will use Node.js Express with MongoDB Architecture to make login and signup

The backend will provide these APIs:

Methods Urls Actions
POST /api/auth/signup signup new account
POST /api/auth/signin login an account
POST /api/auth/signout logout the account

## requirements

Express 4.17.1
cookie-session 1.4.0
bcryptjs 2.4.3
jsonwebtoken 8.5.1
mongoose 5.13.13
MongoDB

# Initialize setup

mkdir node-js-express-login--mongodb
cd node-js-express-login--mongodb

npm init
npm install express mongoose cors cookie-session jsonwebtoken bcryptjs --save

### inside the root folder, create a new server.js file

const express = require("express");
const cors = require("cors");
const cookieSession = require("cookie-session");

const app = express();

var corsOptions = {
origin: "http://localhost:8081"
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

app.use(
cookieSession({
name: "bezkoder-session",
secret: "COOKIE_SECRET", // should use as secret environment variable
httpOnly: true
})
);

// simple route
app.get("/", (req, res) => {
res.json({ message: "Welcome to bezkoder application." });
});

// set port, listen for requests
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
console.log(`Server is running on port ${PORT}.`);
});

node server.js

open your bowser with url http://localhost:8080/

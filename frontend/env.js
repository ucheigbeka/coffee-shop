require('dotenv').config({path: '../.env'})
const fs = require('fs');

const environmentFile = `export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: '${process.env.AUTH0_DOMAIN}', // the auth0 domain prefix
    audience: '${process.env.API_AUDIENCE}', // the audience set for the auth0 app
    clientId: '${process.env.CLIENT_ID}', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};`;

fs.writeFile('./src/environments/environment.ts', environmentFile, function (err) {
  if (err) {
    throw console.error(err);
  } else {
    console.log(`Angular environment.ts file generated`);
  }
});

module.exports = function (ctx) {
  console.log('Done generating environment.ts');
};

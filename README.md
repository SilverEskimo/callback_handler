# Callback Handler Plugins Application


## Table Of Content 

- [Introduction](#introduction)
- [Design](#design)
- [Base Plugins](#base-plugins)
  - [Transaction Validation](#transaction-validation-plugin)
  - [Extra Signature Validation](#extra-signature-validation)
## Introduction:

### Fireblocks API Co-Signer & Callback Handler
The Fireblocks API Co-Signer allows you to automate approvals and signing for transactions and workspace changes. \
This is ideal for any workspace expecting a high volume of transactions, frequent workspace activity, or requiring 24-hour access.\
You can configure the API Co-Signer with a Co-Signer Callback Handler. The Callback Handler is a predefined \HTTPS server that receives requests from the API Co-Signer and returns an action.

When your API Co-Signer is configured with a callback, it sends a POST request to the callback handler. The POST request contains a JSON Web Token (JWT) encoded message signed with the API Co-Signer's private key. The Callback Handler uses the API Co-Signer's public key to verify that every incoming JWT is signed correctly by the API Co-Signer.

The Callback Handler's response is a JWT-encoded message signed with the Callback Handler's private key. This private key must be paired with the public key provided to the API Co-Signer during the Callback Handler's setup.
For detailed documentation of the API Co-Signer Callback Handler Data objects please visit [Fireblocks Developer Portal](https://developers.fireblocks.com/reference/automated-signer-callback).

### Callback Handler Plugin Application
The Callback Handler Plugins Application is a boilerplate application that eases the Callback Handler installation and setup for Fireblocks users. \
The application is designed to work with plugins that any user can develop easily without spending any time or development efforts on the server application development.
The Plugins application comes with a number of pre-configured Plugins. Description for each such plugin can be found below.


## Design:
TBD

## Base Plugins:

### Transaction Validation Plugin
TBD

### Extra Signature Validation
TBD
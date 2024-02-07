# Callback Handler Plugins Application


## Table Of Content 

- [Introduction](#introduction)
- [Base Plugins](#base-plugins)
  - [Transaction Validation](#transaction-validation-plugin)
  - [Extra Signature Validation](#extra-signature-validation)
- [Adding New Plugins](#adding-new-plugins-and-setting-a-new-db-connection-)
  - [Adding New Plugins](#new-plugins-)
  - [New DB Connections](#setting-a-new-db-connection-)
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

## Base Plugins:
### Transaction Validation Plugin (`txid_validation.py/TxidValidation` class)
Being executed on `POST /v2/tx_sign_request`.
The plugin gets the transaction ID (txId) from the payload sent from the Co-Signer and check against a given DB if the same transaction ID exists.
Purpose - making sure that the arrived transaction was not initiated by some external actor and is known to the operator. 

#### Flow:
1. API client initiates transaction via Fireblocks API
2. Fireblocks API returns 200OK with a unique transaction identifier and status 'SUBMITTED'
3. The transaction ID is being saved in user's DB 
4. The transaction hits the Co-Signer machine that forwards the request to the configured callback handler
5. The callback handler runs the Transaction Validation Plugin 
6. The plugin extracts the transaction ID (txId) from the received data
7. The plugin accesses the provided DB instance and checks if the same txId exists
8. If true -> returns `APPROVE` else returns `REJECT`

#### Requirements:
TBD

### Extra Signature Validation (`extra_signature.py/ExtraSignature` class)
Being executed on `POST /v2/tx_sign_request`.
The plugin expects to receive an extra message and a signature of this message, checks that the message is signed by a known signer (by holding a pre-defined public key).
Purpose - making sure that the arrived transaction was initiated only by a pre-defined signer that holds a corresponding private key.

#### Flow:
1. API client initiates transaction via Fireblocks API
2. The transaction contains a `note` field with the message and an `extraSignature` string within the `extraParameters` object, transaction payload for example:
   ```javascript
    {
      assetId: 'BTC',
      amount: 1,
      source: { ... },
      destination: { ... },
      note: 'MyExampleMessage',
      extraParameters: {
        extraSignature: signed(MyExampleMessage)
      }
    }
   ```
3. Fireblocks API returns 200OK with a unique transaction identifier and status 'SUBMITTED'
4. The transaction hits the Co-Signer machine that forwards the request to the configured callback handler
5. The callback handler runs the Extra Signature Validation plugin
6. The plugin retrieves the message from the `note` field and signature from `extraSignature` field
7. The plugin load a pre-defined public key and verifies the given signature
8. If true -> returns `APPROVE` else returns `REJECT`

#### Requirements:
TBD

## Adding new plugins and setting a new DB connection
### New Plugins:
1. Create a new python file in the `src/plugins` directory and name it in snake_case, for example: my_example_plugin.py
2. Create a class in the newly created file in PascalCase, for example: MyExamplePlugin
   - Please make sure to follow the naming convention: `my_example_plugin.py` file name -> `MyExamplePlugin` class name
3. Inherit the abstract class `Plugin` from `src/plugins/interface.py`:
```python
from src.plugins.interface import Plugin

class MyExamplePlugin(Plugin)
.
.
.
```
4. Make sure to implement the required methods:
   - `async def process_request(self, data)`: The entry point to your plugin logic
   - `def _build_query(self, *args)`: In case a DB connection required - method that builds the required DB query. If DB access is not needed, simply `pass`
   - `def __repr__(self)`: Representation for logging purposes
5. Update the PLUGINS variable in .env file. Set the name of the plugin in snake_case. In case of running multiple plugins - separate by comma:
   - For example: `PLUGINS=plugin_one,plugin_two,my_example_plugin`
### Setting a new DB connection:
1. By default, MongoDB and Postgres are supported. If one of these works for you, update the required environment variables in .env file.
2. If a new type of DB connection is required, please follow the steps below:
   - Create a new file in `src/databases`, for example: `my_db_conn.py` 
   - Create a new class in the newly created file and inherit the abstract class `DatabaseInterface` from `src/databases/interface.py`
   ```python
   from src.databases.interface import DatabaseInterface
   
   class MyDbConn(DatabaseInterface):
   .
   .
   . 
   ```
   - Make sure to implement the required methods:
     - `def connect(self, *args)`: Initial connection to your DB
     - `def execute_query(self, *args)`: Executes a query to your DB
   - Update the `DB_TYPE` variable in the .env file, for example: `DB_TYPE=my_db_conn`
   - Update the `DB_CLASS_MAP` variable in `settings.py` while the key is the DB_TYPE and the value is the name of the DB connection class, for example: 
     ```python
     DB_CLASS_MAP = {
      'my_db_conn': MyDbConn
     }
     ```
   
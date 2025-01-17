# DVerse UI
# Author: @MingLi9
# Date: 2024-11-20
# Description: The main UI for DVerse.
# Version: 1.0.0
# License: MIT License
# Copyright (c) 2022 Ming Li

## How to run (Docker)
1. install docker
2. run `docker build -t dverse-ui .`
3. run `docker run -p 3000:3000 dverse-ui`
4. open your browser and navigate to `http://localhost:3000`
5. you can now interact with the DVerse UI

## How to run (Local)
1. install node.js and npm
2. run `npm install`
3. run `npm start`
4. open your browser and navigate to `http://localhost:3000`
5. you can now interact with the DVerse UI

## How to add a new page
1. create a new folder in the `src/pages` directory
2. create a new file in the new folder and name it `index.jsx`
3. add the page to the `src/components/apps.js`
4. add the page to the imports in `src/App.js`
5. add the route-element to the routes in `src/App.js`
If this part is unclear or somehow confuses you ask the (co-)author of this document.

## Login/Registration
Login and Registration is managed by Matrix.org.
Currently only SSO is being used within the frontend.
If other methods are required, feel free to contact @MingLi9.
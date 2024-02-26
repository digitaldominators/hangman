The frontend and backend are running as separate applications. The frontend is not really using any framework and 
is just using vanilla javascript with a few libraries to allow is to behave like a single page app.

The frontend is organized into a few folders:

partials - contains the html template pages. These files are statically built into every page. This includes the header, footer, and the navbar.

src/js - contains the javascript files. This is where the main logic of the app is. The main file is main.js. This file is the entry point for the app. 
It sets up the event listeners and the routing for the app. All the other javascript files are imported here and the initialization for each page is done
by the page's load<X>Page method using Barba.js. The main.js page is also responsible for setting up gsap.

src/css - contains the css files. This is where the styles for the app are. The style.css file is the entry point for the app and it imports all the other css files and fonts.

src/images - contains the images for the game.

src/sounds - contains the sounds for the game.

all the html pages are in the src folder. The html pages are built using the partials and the main.js file.
The html pages are all built using the handlebars templating engine.

To run the frontend you need to have node installed. You can install node from the node website. Once you have node installed you can run the following commands to start the frontend:

```bash
cd frontend
npm install
npm run dev
```

to build the frontend for production you can run:

```bash
npm run build
```
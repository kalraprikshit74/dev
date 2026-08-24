import App from "./components/app.vue";
import { createApp } from "vue";
const app = createApp(App);

import PrimeVue from "primevue/config";
import "/node_modules/primeflex/primeflex.css";
//theme
import "primevue/resources/themes/lara-light-indigo/theme.css";
//core
import "primevue/resources/primevue.min.css";

import Button from "primevue/button";

function start() {
  app.use(PrimeVue);

  app.component("Button", Button);

  app.mount("app");
}
export default function () {
  widget.addEvent("onLoad", () => {
    start();
  });
}

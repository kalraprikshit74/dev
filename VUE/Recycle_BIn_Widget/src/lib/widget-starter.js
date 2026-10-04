import { initWidget } from "./widget";

initWidget((widget) => {
  import("../main.js").then((module) => {
    module.default();
  });
});

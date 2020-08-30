import { readable, writable } from "svelte/store";

import Editor from "./Editor.svelte";

export const dbData = readable({}, (set) => {
    set(JSON.parse(document.getElementById("db-data").textContent));
    return () => {};
});

const initDataElement = document.getElementById("init-data");
const initData = initDataElement && JSON.parse(initDataElement.textContent);

export const columns = writable(
    initData
        ? initData.columns
        : [
              { name: "heart", kinks: [] },
              { name: "check", kinks: [] },
              { name: "tilde", kinks: [] },
              { name: "no", kinks: [] },
          ]
);

const app = new Editor({
    target: document.querySelector("main"),
    props: {
        action: initData ? initData.action : undefined,
    },
});

import { writable } from "svelte/store";

import Editor from "./Editor.svelte";

export const dbData = JSON.parse(
    document.getElementById("db-data").textContent
);

const initDataElement = document.getElementById("init-data");
const initData = initDataElement && JSON.parse(initDataElement.textContent);

let initColumns, initCustoms;
if (initData) {
    initColumns = initData.columns;
    initCustoms = [];

    let customID = 1;
    // extract customs
    for (let column of initColumns) {
        for (let kink of column.kinks) {
            if (kink.custom) {
                let { name, description } = kink;
                delete kink.name;
                delete kink.description;
                kink.id = customID;
                initCustoms.push({ id: customID, name, description });
                customID++;
            }
        }
    }
} else {
    initColumns = [
        { name: "heart", kinks: [] },
        { name: "check", kinks: [] },
        { name: "tilde", kinks: [] },
        { name: "no", kinks: [] },
    ];
    initCustoms = [];
}

export const columns = writable(initColumns);

export const customData = writable(initCustoms);

const app = new Editor({
    target: document.querySelector("main"),
    props: {
        action: initData ? initData.action : undefined,
    },
});

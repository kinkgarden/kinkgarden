import Editor from './Editor.svelte';

const initDataElement = document.getElementById('init-data');

const app = new Editor({
    target: document.querySelector('main'),
    props: {
        dbData: JSON.parse(document.getElementById('db-data').textContent),
        initData: initDataElement === undefined ? undefined : JSON.parse(initDataElement.textContent),
    },
});

function fixPageWidth() {
    document.documentElement.style.setProperty('--page-width', document.documentElement.clientWidth + 'px');
}

setTimeout(fixPageWidth, 1);

window.addEventListener('resize', fixPageWidth);
document.addEventListener('domContentLoaded', fixPageWidth);

import Editor from './Editor.svelte';

const app = new Editor({
    target: document.querySelector('main'),
    props: {
        dbData: JSON.parse(document.getElementById('db-data').textContent),
    },
});

function fixPageWidth() {
    document.documentElement.style.setProperty('--page-width', document.documentElement.clientWidth + 'px');
}

setTimeout(fixPageWidth, 1);

window.addEventListener('resize', fixPageWidth);
document.addEventListener('domContentLoaded', fixPageWidth);

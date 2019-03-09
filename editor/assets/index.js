import Editor from './Editor.html';

const app = new Editor({
	target: document.querySelector('main'),
});

function fixPageWidth() {
	document.documentElement.style.setProperty('--page-width', document.documentElement.clientWidth + 'px');
}

setTimeout(fixPageWidth, 1);

window.addEventListener('resize', fixPageWidth);
document.addEventListener('domContentLoaded', fixPageWidth);

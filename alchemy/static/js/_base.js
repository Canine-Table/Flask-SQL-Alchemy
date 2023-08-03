#!/usr/bin/node

let currentPageTitle = document.title;

window.addEventListener('blur', () => document.title = 'Come Back to Flask!');
window.addEventListener('focus', () => document.title = currentPageTitle);

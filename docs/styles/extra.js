const MODE_KEY = 'robot-framework-manual-mode';

function toggleTestTaskMode() {
    const mode = getNewMode();
    setDisplay(mode);
    setHeaders(mode);
    setData(mode);
}

function getNewMode() {
    const mode = localStorage.getItem(MODE_KEY) == 'task' ? 'test' : 'task';
    localStorage.setItem(MODE_KEY, mode);
    return mode;
}

function setDisplay(mode) {
    for (const test of document.getElementsByClassName('test')) {
        test.style.display = mode == 'test' ? 'inline' : 'none';
    }
    for (const task of document.getElementsByClassName('task')) {
        task.style.display = mode == 'task' ? 'inline' : 'none';
    }
}

function setHeaders(mode) {
    const newHeader = mode == 'test' ? '*** Test Cases ***' : '*** Tasks ***';
    const oldHeader = mode == 'test' ? '*** Tasks ***' : '*** Test Cases ***';
    for (const elem of document.querySelectorAll('.language-robotframework .gh')) {
        if (elem.innerHTML == oldHeader) {
            elem.innerHTML = newHeader;
        }
    }
}

function setData(mode) {
    if (mode == 'test') {
        document.querySelector('#rpa-toggle input').checked = false;
        document.getElementById('test-mode-icon').setAttribute('data-robot-narrow', 'show');
        document.getElementById('task-mode-icon').setAttribute('data-robot-narrow', 'hide');
    } else {
        document.querySelector('#rpa-toggle input').checked = true;
        document.getElementById('test-mode-icon').setAttribute('data-robot-narrow', 'hide');
        document.getElementById('task-mode-icon').setAttribute('data-robot-narrow', 'show');
    }
}

document$.subscribe(function () {
    if (localStorage.getItem(MODE_KEY) == 'task') {
        setHeaders('task');
    }
});

const MODE_KEY = 'robot-framework-manual-mode';

function toggleTestTaskMode() {
    const mode = getNewMode();
    setDisplay(mode);
    setHeaders(mode);
    setData(mode);
}

function getNewMode() {
    const oldMode = localStorage.getItem(MODE_KEY) || 'test';
    const newMode = oldMode == 'test' ? 'task' : 'test';
    localStorage.setItem(MODE_KEY, newMode);
    return newMode;
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
    setAttribute('robot-mode-toggle', 'data-robot-mode', mode);
    setAttribute('robot-test-icon', 'data-robot-narrow', mode == 'test' ? 'show' : 'hide');
    setAttribute('robot-task-icon', 'data-robot-narrow', mode == 'task' ? 'show' : 'hide');
}

function setAttribute(elemId, name, value) {
    document.getElementById(elemId).setAttribute(name, value);
}

document$.subscribe(function () {
    if (localStorage.getItem(MODE_KEY) == 'task') {
        setHeaders('task');
    }
});

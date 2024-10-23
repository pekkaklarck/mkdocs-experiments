// Show tests/tasks after the mode is changed. On page load styles are updated directly.
function setTaskMode(enabled) {
    setTaskDisplay(enabled);
    setTaskHeaders(enabled);
    document.querySelector('#rpa-toggle input').checked = enabled;
    localStorage.setItem('robot-framework-manual-mode', enabled ? 'task' : 'test');
}

function setTaskDisplay(enabled) {
    for (const test of document.getElementsByClassName('test')) {
        test.style.display = enabled ? 'none' : 'inline';
    }
    for (const task of document.getElementsByClassName('task')) {
        task.style.display = enabled ? 'inline' : 'none';
    }
}

function setTaskHeaders(enabled) {
    const newText = enabled ? '*** Tasks ***' : '*** Test Cases ***';
    const oldText = enabled ? '*** Test Cases ***' : '*** Tasks ***';
    for (const header of document.querySelectorAll('.language-robotframework .gh')) {
        if (header.innerHTML == oldText) {
            header.innerHTML = newText;
        }
    }
}

document$.subscribe(function () {
    if (localStorage.getItem('robot-framework-manual-mode') == 'task') {
        setTaskHeaders(true);
    }
});

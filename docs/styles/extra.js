function toggleTestOrTask(rpa) {
    const toggle = document.querySelector('#rpa-toggle input');
    const tests = document.getElementsByClassName('test');
    const tasks = document.getElementsByClassName('task');
    const headers = document.querySelectorAll('.language-robotframework .gh');
    if (rpa) {
        toggle.checked = true;
        setDisplay(tests, 'none');
        setDisplay(tasks, 'inline');
    } else {
        setDisplay(tests, 'inline');
        setDisplay(tasks, 'none');
        toggle.checked = false;
    }
    setHeader(headers, rpa);
}

function setDisplay(elements, value) {
    for (const elem of elements) {
        elem.style.display = value;
    }
}

function setHeader(headers, rpa) {
    const newText = rpa ? '*** Tasks ***' : '*** Test Cases ***';
    const oldText = rpa ? '*** Test Cases ***' : '*** Tasks ***';
    for (const elem of headers) {
        if (elem.innerHTML == oldText) {
            elem.innerHTML = newText;
        }
    }
}

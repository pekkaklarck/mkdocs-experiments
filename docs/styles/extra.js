function toggleTestOrTask(rpa) {
    const toggle = document.querySelector('#rpa-toggle input');
    const tests = document.getElementsByClassName('test');
    const tasks = document.getElementsByClassName('task');
    if (rpa) {
        toggle.checked = true;
        setDisplay(tests, 'none');
        setDisplay(tasks, 'inline');
    } else {
        setDisplay(tests, 'inline');
        setDisplay(tasks, 'none');
        toggle.checked = false;
    }
}
function setDisplay(elements, value) {
    for (const elem of elements) {
        elem.style.display = value;
    }
}

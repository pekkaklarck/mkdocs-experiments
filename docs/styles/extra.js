function toggleTestOrTask(checked) {
    const tests = document.getElementsByClassName('test');
    const tasks = document.getElementsByClassName('task');
    if (checked) {
        setDisplay(tests, 'none');
        setDisplay(tasks, 'inline');
    } else {
        setDisplay(tests, 'inline');
        setDisplay(tasks, 'none');
    }
}
function setDisplay(elements, value) {
    for (const elem of elements) {
        elem.style.display = value;
    }
}

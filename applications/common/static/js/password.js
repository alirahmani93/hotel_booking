window.onload = () => {
    document.querySelectorAll('.show-password').forEach((item) => {
        item.addEventListener('mousedown', (event) => {
            document.querySelector(`input[name='${item.id}']`).type = 'text';
        });
        item.addEventListener('touchstart', (event) => {
            document.querySelector(`input[name='${item.id}']`).type = 'text';
        });
        item.addEventListener('mouseup', (event) => {
            document.querySelector(`input[name='${item.id}']`).type = 'password';
        });
        item.addEventListener('touchend', (event) => {
            document.querySelector(`input[name='${item.id}']`).type = 'password';
        });
        setTimeout(() => {
            document.querySelector(`input[name='${item.id}']`).type = 'password';
            document.querySelector(`input[name='${item.id}']`).style = {'color': 'default'};
        }, 1000);
    });
};

const copy_password = (name) => {
    const elem = document.querySelector(`input[name='${name}']`);
    elem.focus();
    elem.select();
    elem.setSelectionRange(0, 99999); /* For mobile devices */
    navigator.clipboard.writeText(elem.value);
}
let ping_interval = 10;
let services_status = {}

function update_ping(interval) {
    try {
        let val = parseInt(document.getElementById('interval').value);
        if (val < 1) {
            alert('Minimum interval is 1 seconds.');
            return;
        }
        ping_interval = val;
    } catch (e) {
        alert("Invalid value");
    }
}

function show_rows(state) {
    document.querySelectorAll('.app-item.up').forEach((element) => {
        element.style.display = (state == 0) || (state == 1) ? 'flex' : 'none';
    })
    document.querySelectorAll('.app-item.down').forEach((element) => {
        element.style.display = (state == 0) || (state == -1) ? 'flex' : 'none';
    })
}

const set_controls = (services_name, status) => {
    document.querySelector(`.app-item.${services_name} .state .running`).style.display = status ? 'block' : 'none';
    document.querySelector(`.app-item.${services_name} .state .stopped`).style.display = status ? 'none' : 'block';
    document.querySelector(`.app-item.${services_name} .name`).style.color = status ? 'black' : 'red';
    if (status) {
        document.querySelector(`.app-item.${services_name} `).classList.add('up');
        document.querySelector(`.app-item.${services_name} `).classList.remove('down');
        if (services_name != 'DB') {
            document.querySelector(`.app-item.${services_name} .control .start`).classList.add('disabled-link');
            document.querySelector(`.app-item.${services_name} .control .stop`).classList.remove('disabled-link');
            document.querySelector(`.app-item.${services_name} .control .restart`).classList.add('disabled-link');
        }
    } else {
        document.querySelector(`.app-item.${services_name} `).classList.add('down');
        document.querySelector(`.app-item.${services_name} `).classList.remove('up');
        if (services_name != 'DB') {
            document.querySelector(`.app-item.${services_name} .control .start`).classList.remove('disabled-link');
            if (services_name != 'Trader')
                document.querySelector(`.app-item.${services_name} .control .stop`).classList.add('disabled-link');
            document.querySelector(`.app-item.${services_name} .control .restart`).classList.remove('disabled-link');
        }
    }

}
const start = () => {
    const ping = async (url) => {
        return true;
        try {
            let response = await fetch(`${url}ping`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`,
                }
            });
            return (response.status == 200);
        } catch (e) {
            return (false);
        }
    }

    services.forEach(async function (service) {
        let status = service.name == 'DB' ? true : await ping(service.url);
        if (services_status[service.name] != status) {
            services_status[service.name] = status;
            set_controls(service.name, services_status[service.name])
        }
    })
    document.getElementById('last_ping').classList.remove('play');
    setTimeout(() => {
        document.getElementById('last_ping').innerText = new Date();
        document.getElementById('last_ping').classList.add('play');
    }, 1000);
    setTimeout(start, ping_interval * 1000);
}

services.forEach(function (service) {
    services_status[service.name] = false;
    set_controls(service.name, false)
});

window.onload = () => {
    document.querySelector('input[name="keyword"]').addEventListener('keyup', (event) => {
        let tooltip;
        const filter = event.target.value.toLowerCase();
        const items = document.querySelectorAll('div.app-item')
        items.forEach((item) => {
            tooltip = item.querySelector('.name img').title.toLowerCase();
            item.classList.remove('display-none');
            item.classList.remove('display-flex');
            item.classList.add(tooltip.indexOf(filter) > -1 ? 'display-flex' : 'display-none');
        });
        document.querySelector('.service-counter').innerHTML = document.querySelectorAll('div.app-item.display-flex').length;
    });
    start();
}

const toggle_view = (view) => {
    const container = document.querySelector('div.service-container');
    container.classList.add('fade-out');
    switch (view) {
        case 1:
            setTimeout(() => {
                container.classList.add('grid');
                container.classList.remove('fade-out');
                container.classList.add('fade-in');
                setTimeout(() => {
                    container.classList.remove('fade-in');
                    container.classList.add('opaque')
                }, 700)
            }, 700)
            break;
        default:
            setTimeout(() => {
                container.classList.remove('fade-out');
                container.classList.remove('opaque')
                // container.classList.add('fade-in');
                setTimeout(() => {
                    container.classList.remove('grid');
                    container.classList.add('fade-in');
                }, 700)
            }, 700)
            break;
    }
    return false;
}

window.onload = function () {
    const current_vm = document.getElementById('id_current_vm');
    const edit = document.getElementById('change_id_current_vm');
    const add = document.getElementById('add_id_current_vm');
    const delet = document.getElementById('delete_id_current_vm');
    const current_vm_container = document.querySelector('.field-current_vm');
    const request_types_container = document.querySelector('.field-type .readonly');
    const request_types = document.getElementById('id_type');
    const request_new = document.getElementById('id_type_0');
    const request_delete = document.getElementById('id_type_3');
    let vm_delete_container;
    let vm_deploy_container = [];
    document.querySelectorAll('h2').forEach(
        (item) => {
            if (item.innerText === 'VM deletion by IT team')
                vm_delete_container = item.parentElement;
        }
    )
    document.querySelectorAll('h2').forEach(
        (item) => {
            if (['IT operator', 'Product owner', 'VM deployment by IT team', 'Deployed VM', 'VM deployment by backend team'].includes(item.innerText))
                vm_deploy_container.push(item.parentElement);
        }
    )
    if (request_types_container)
        if (request_types_container.innerText === 'Remove') {
            vm_delete_container.setAttribute('style', 'display:block;');
            for (item of vm_deploy_container) {
                item.setAttribute('style', 'display:none;');
            }
        } else {
            vm_delete_container.setAttribute('style', 'display:none;');
        }

    if (request_types)
        if (request_new.checked && current_vm_container) {
            current_vm_container.setAttribute('style', 'display:none;');
            vm_delete_container.setAttribute('style', 'display:none;');
            if (edit)
                edit.setAttribute('style', 'display:none;');
            if (delet)
                delet.setAttribute('style', 'display:none;');
            if (add)
                add.setAttribute('style', 'display:none;');
        } else {
            if (request_delete.checked && vm_delete_container) {
                vm_delete_container.setAttribute('style', 'display:block;');
                for (item of vm_deploy_container) {
                    item.setAttribute('style', 'display:none;');
                }
            }
        }
    if (request_types)
        request_types.onchange = () => {
            if (request_new.checked) {
                current_vm_container.setAttribute('style', 'display:none;');
                vm_delete_container.setAttribute('style', 'display:none;');
                for (item of vm_deploy_container) {
                    item.setAttribute('style', 'display:block;');
                }
            } else {
                current_vm_container.setAttribute('style', 'display:block;');
                if (request_delete.checked) {
                    vm_delete_container.setAttribute('style', 'display:block;');
                    for (item of vm_deploy_container) {
                        item.setAttribute('style', 'display:none;');
                    }
                } else {
                    vm_delete_container.setAttribute('style', 'display:none;');
                    for (item of vm_deploy_container) {
                        item.setAttribute('style', 'display:block;');
                    }
                }
                current_vm.onchange = () => {
                    $.ajax({
                        url: `${url}?vm=${current_vm.value}`,
                        type: "GET",
                        dataType: "json",
                        success: (data) => {
                            document.getElementById('id_service').value = data['service'];
                            document.getElementById('id_service_type').value = data['service_type'];
                            document.getElementById('id_url').value = data['domain'];
                            document.getElementById('id_interface').value = data['admin'];
                            document.getElementById('id_usr_description').value = data['description'];
                            document.getElementById('id_os').value = data['os'];
                            document.getElementById('id_storage').value = data['storage'];
                            document.getElementById('id_memory').value = data['memory'];
                            document.getElementById('id_cpu').value = data['cpu'];
                        },
                        error: (error) => {
                            document.getElementById('id_service').value = '';
                            document.getElementById('id_service_type').value = '';
                            document.getElementById('id_url').value = '';
                            document.getElementById('id_interface').value = '';
                            document.getElementById('id_usr_description').value = '';
                            document.getElementById('id_os').value = '';
                            document.getElementById('id_storage').value = '';
                            document.getElementById('id_memory').value = '';
                            document.getElementById('id_cpu').value = '';
                        }
                    });
                };
            }
        };
}

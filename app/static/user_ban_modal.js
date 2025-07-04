'use strict';

function modalShown(event) {
    let button = event.relatedTarget;
    let userId = button.dataset.userId;
    let newUrl = `/moderation/ban/${userId}`;
    let form = document.getElementById('deleteModalForm');
    form.action = newUrl;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);
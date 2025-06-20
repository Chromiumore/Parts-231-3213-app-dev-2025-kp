'use strict';

function modalShown(event) {
    let button = event.relatedTarget;
    let gameId = button.dataset.gameId;
    let newUrl = `/creator-hub/delete/${gameId}`;
    let form = document.getElementById('deleteModalForm');
    form.action = newUrl;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);
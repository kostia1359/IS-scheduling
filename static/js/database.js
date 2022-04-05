let dialog;
let save;

let currentTable = "teachers";

function tableChanged(){
    currentTable = $("#table-select").val();
    reload();
}

$(document).ready(function () {
    reload();
});

function reload() {
    switch (currentTable) {
        case "teachers":
            load_teachers_table();
            break;
        case "classrooms":
            load_classrooms_table();
            break;
    }



    $('#btnAdd').on('click', function () {
        dialog.open('Add item');
    });

    $('#btnSave').on('click', save);
    $('#btnCancel').on('click', function () {
        dialog.close();
    });
}

function load_teachers_table() {
    let address = '/database/teachers';
    let grid = $('#grid').grid({
        dataSource: address,
        inlineEditing: {mode: 'command'},
        columns: [
            {field: 'name', title: "Name", editor: true},
            {field: 'min_load', title: "Min load", editor: true},
            {field: 'max_load', title: "Max load", editor: true},
        ]
    });
    grid.reload();
    grid.on('rowDataChanged', function (e, id, record) {
        $.ajax({
            url: address,
            type: 'PUT',
            data: record
        });
        grid.reload()
    });
    grid.on('rowRemoving', function (e, $row, id, record) {
        if (confirm('Are you sure?')) {
            $.ajax({url: address, data: {id: record['id']}, method: 'DELETE'})
                .done(function () {
                    grid.reload();
                })
                .fail(function () {
                    alert('Failed to delete.');
                });
        }
    });

    $('#teacher-dialog').removeClass('display-none');
    dialog = $('#teacher-dialog').dialog({
        autoOpen: false,
        resizable: false,
        modal: true,
        width: 360
    });

    save = function () {
        let item = {
            'name': $('#teacher-name').val(),
            'min_load': $('#teacher-min_load').val(),
            'max_load': $('#teacher-max_load').val()
        };
        $.post(address, item);
        dialog.close();
        grid.reload();
    }
}


function load_classrooms_table() {
    let address = '/database/classrooms';
    let grid = $('#grid').grid({
        dataSource: address,
        inlineEditing: {mode: 'command'},
        columns: [
            {field: 'id', title: "ID", editor: true},
            {field: 'capacity', title: "Capacity", editor: true},
        ]
    });
    grid.reload();
    grid.on('rowDataChanged', function (e, id, record) {
        $.ajax({
            url: address,
            type: 'PUT',
            data: record
        });
        grid.reload()
    });
    grid.on('rowRemoving', function (e, $row, id, record) {
        if (confirm('Are you sure?')) {
            $.ajax({url: address, data: {id: record['id']}, method: 'DELETE'})
                .done(function () {
                    grid.reload();
                })
                .fail(function () {
                    alert('Failed to delete.');
                });
        }
    });

    $('#classroom-dialog').removeClass('display-none');
    dialog = $('#classroom-dialog').dialog({
        autoOpen: false,
        resizable: false,
        modal: true,
        width: 360
    });

    save = function () {
        let item = {
            'id': $('#classroom-id').val(),
            'capacity': $('#classroom-capacity').val(),
        };
        $.post(address, item);
        dialog.close();
        grid.reload();
    }
}

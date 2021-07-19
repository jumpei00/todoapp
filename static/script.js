class BackEndApi {

    constructor() {
        this.send_data = {};
    }

    data_get() {
        $.get('/todo').done(function (res) {
            var todo_list = [];
            var timestamp = '';
            var contents = '';
            var priority = '';

            todo_list = res['todo'];
            if (todo_list != null) {
                for (var i = 0; i < todo_list.length; i++) {
                    timestamp = todo_list[i]['timestamp'];
                    contents = todo_list[i]['contents'];
                    priority = todo_list[i]['priority'];
                    $('#todoBody').append(tablepart_html(timestamp, contents, priority));
                }   
            }
        })
    }

    data_post() {
        var contents = this.send_data['contents'];
        var priority = this.send_data['priority'];

        $.ajax({
            url: '/todo',
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(this.send_data),
            success: function (res) {
                var timestamp = res['timestamp'];
                $('#todoBody').prepend(tablepart_html(timestamp, contents, priority));
            },
            error: function (res) {
                alert(res['error']);
            }
        })
    }

    data_put() {
        var timestamp = this.send_data['timestamp'];
        var contents = this.send_data['contents'];
        var priority = this.send_data['priority'];

        $.ajax({
            url: '/todo',
            method: 'PUT',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(this.send_data),
            success: function (res) {
                $('#' + timestamp).find('#contents').html(contents);
                $('#' + timestamp).find('#priority').html(priority);
            },
            error: function (res) {
                alert(res['error']);
            }
        })
    }

    data_delete() {
        var timestamp = this.send_data['timestamp'];

        $.ajax({
            url: '/todo',
            method: 'DELETE',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(this.send_data),
            success: function (res) {
                $('#' + timestamp).remove();
            },
            error: function (res) {
                alert(res['error']);
            }
        })

    }
}

get_todo_list = () => {
    var backend_api = new BackEndApi();
    backend_api.data_get();
}

popup_process = () => {
    $('#exampleModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var button_name = button.data('whatever');
        var modal = $(this);

        if (button_name == 'Create') {
            modal.find('.modal-title').text('Todo ' + button_name);

            $('#resister').off('click')
            $('#resister').on('click', function () {
                var backend_api = new BackEndApi();
                backend_api.send_data['contents'] = modal.find('#contents-text').val();
                backend_api.send_data['priority'] = modal.find('#inputPriority').val();
                backend_api.data_post();
            })
        }

        else if (button_name == 'Edit') {
            var table = button.closest('.todoData');
            var timestamp = table.attr('id');
            var contents = table.find('#contents').text();
            var priority = table.find('#priority').text();

            modal.find('.modal-title').text('Todo ' + button_name);
            modal.find('#contents-text').val(contents);
            modal.find('#inputPriority').val(priority);

            $('#resister').off('click')
            $('#resister').on('click', function () {
                var backend_api = new BackEndApi();
                backend_api.send_data['timestamp'] = timestamp;
                backend_api.send_data['contents'] = modal.find('#contents-text').val();
                backend_api.send_data['priority'] = modal.find('#inputPriority').val();
                backend_api.data_put();
            })
        }
    })

    $('#exampleModal').on('hidden.bs.modal', function () {
        var modal = $(this);
        modal.find('#contents-text').val('');
        modal.find('#inputPriority').val('...');
    })
}

table_delete = () => {
    $(document).on('click', '#delete', function () {
        var backend_api = new BackEndApi();
        var table = $(this).closest('.todoData');
        backend_api.send_data['timestamp'] = table.attr('id');
        backend_api.data_delete();
    })
}

tablepart_html = (timestamp, contents, priority) => {
    var html = '<tr class="todoData" id="' + timestamp + '">' +
        '<td id="contents">' + contents + '</td>' +
        '<td id="priority">' + priority + '</td>' +
        '<td>' +
        '<button type="button" class="btn btn-info" data-toggle="modal" data-target="#exampleModal"' +
        'data-whatever="Edit">Edit</button>' +
        '</td>' +
        '<td>' +
        '<button id="delete" type="button" class="btn btn-danger">Delete</button>' +
        '</td>' +
        '</tr>'
    return html
}

window.onload = () => {
    get_todo_list();
    table_delete();
    popup_process();
}

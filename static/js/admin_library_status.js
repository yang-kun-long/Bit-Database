$(document).ready(function () {
    let currentPage = 1;
    const perPage = 8;
    let totalPages = 0;
    // 获取用户状态并显示在表格中
    function fetchLibraryStatus(page) {

        $.ajax({
            url: `/api/libraryS_setting/get_libraryS_status?page=${page}&per_page=${perPage}`,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                populateTable(response.users);
                updatePagination(response);
            },
            error: function (error) {
                console.log('Error fetching library status:', error);
            }
        });
    }
    //为每页生成按钮 
    function generatePagination(totalPages) {
        // 为每页生成按钮
        for (let i = 1; i <= totalPages; i++) {
            let button = $('<button>', {
                text: i,
                class: (i === currentPage) ? 'active' : '',
                click: function () {
                    fetchLibraryStatus(i);
                }
            });
            $('#pagination').append(button);
        }
    }
    // 更新分页控件
    function updatePagination(data) {
        // 清空现有分页按钮
        $('#pagination').empty();
        // 计算总页数
        totalPages = Math.ceil(data.total / perPage);
        generatePagination(totalPages);

    }
    // 将用户状态填充到表格中
    function populateTable(data) {
        var table = $('#user-status-table');
        table.empty(); // 清空现有数据
        data.forEach(function (user) {
            table.append(
                '<tr>' +
                '<td>' + user.username + '</td>' +
                '<td>' + user.work_id + '</td>' +
                '<td>' + user.user_type + '</td>' +
                '<td>' + user.interval_date + '</td>' +
                '<td>' + user.borrow_period + '</td>' +
                '<td>' + user.overdue_reminder_days + '</td>' +
                '<td>' + user.borrow_limit + '</td>' +
                '<td>' + user.violation_limit + '</td>' +
                '<td>' + (user.is_book_admin ? '是' : '否') + '</td>' +
                '<td>' +
                '<button class="btn btn-primary edit-button" ' +
                'data-username="' + user.username + '" ' +
                'data-work-id="' + user.work_id + '" ' +
                'data-user-type="' + user.user_type + '" ' +
                'data-interval-date="' + user.interval_date + '" ' +
                'data-borrow-period="' + user.borrow_period + '" ' +
                'data-overdue-reminder-days="' + user.overdue_reminder_days + '" ' +
                'data-borrow-limit="' + user.borrow_limit + '" ' +
                'data-violation-limit="' + user.violation_limit + '" ' +
                'data-is-book-admin="' + user.is_book_admin + '">' +
                '修改</button>' +
                '</td>' +
                '</tr>'
            );
        });
    }
    // 点击分页按钮获取数据
    $('#pagination').on('click', 'button', function () {
        // 更新当前页码
        currentPage = parseInt($(this).text()); // 确保 currentPage 是数字类型
        // 重新获取数据并更新分页
        fetchLibraryStatus(currentPage);
        console.log(currentPage);
        generatePagination(totalPages)
    });
    $('#saveChanges').on('click', function() {
        // 阻止模态框关闭
        event.preventDefault();
        
        // 获取模态框中的表单数据
        var formData = {
            work_id: $('#modal-work-id').text(), 
            interval_date: $('#interval_date').val(),
            borrow_period: $('#borrow_period').val(),
            overdue_reminder_days: $('#overdue_reminder_days').val(),
            borrow_limit: $('#borrow_limit').val(),
            violation_limit: $('#violation_limit').val(),
            is_book_admin: $('#is_book_admin').val()
        };
        // 显示formData
        for (var key in formData) {
            console.log(key + ':'+ formData[key]);
        }
            
        // 发送AJAX请求到后端API
        $.ajax({
            url: '/api/libraryS_setting/modify_libraryS_status',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            dataType: 'json',
            success: function(response) {
                // 请求成功，处理返回的数据
                if(response.message === '修改成功') {
                    alert('图书馆状态更新成功');
                    // 关闭模态框
                    $('#editModal').modal('hide');
                    // 刷新页面
                    fetchLibraryStatus(currentPage);
                } else {
                    alert('更新失败，请稍后重试');
                }
            },
            error: function(xhr, status, error) {
                // 请求失败，处理错误
                console.error('修改失败:', xhr.responseText);
                alert('更新失败，请稍后重试');
            }
        });
    });
    // 当表格行中的修改按钮被点击时
    $('#user-status-table').on('click', '.edit-button', function () {
        // 获取当前用户的数据
        const userData = {
            username: $(this).data('username'),
            workId: $(this).data('work-id'),
            user_type: $(this).data('user-type'),
            interval_date: $(this).data('interval-date'),
            borrow_period: $(this).data('borrow-period'),
            overdue_reminder_days: $(this).data('overdue-reminder-days'),
            borrow_limit: $(this).data('borrow-limit'),
            violation_limit: $(this).data('violation-limit'),
            is_book_admin: $(this).data('is-book-admin')
        };

        // 填充模态框中的基本信息字段
        $('#modal-username').text(userData.username);
        $('#modal-work-id').text(userData.workId);
        $('#modal-user-type').text(userData.user_type);
        // 填充其他基本信息字段...

        // 填充模态框中的表单字段
        $('#interval_date').val(userData.interval_date);
        $('#borrow_period').val(userData.borrow_period);
        $('#overdue_reminder_days').val(userData.overdue_reminder_days);
        $('#borrow_limit').val(userData.borrow_limit);
        $('#violation_limit').val(userData.violation_limit);
        $('#is_book_admin').val(userData.is_book_admin);

        // 显示模态框
        $('#editModal').modal('show');
    });

    // 页面加载完毕后获取数据
    fetchLibraryStatus(currentPage);
});
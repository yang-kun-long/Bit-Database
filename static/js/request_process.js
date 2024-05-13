$(document).ready(function() {// 页面加载完成后执行
    loadRequests();

    function loadRequests() {
        $.ajax({
            url: '/api/request_process/all',
            type: 'GET',
            dataType: 'json',
            success: function(requests) {
                var tableBody = $('#requestsTableBody');
                tableBody.empty(); // 清空现有内容
                requests.forEach(function(request) {
                    var row = $('<tr>');
                    row.append(`<td>${request.id}</td>`);
                    row.append(`<td>${request.requester_name}</td>`);
                    row.append(`<td>${request.book.name}</td>`);
                    row.append(`<td>${request.request_date}</td>`);
                    row.append(`<td>${request.request_reason}</td>`);
                    var actionsTd = $('<td>');
                    if (request.status === '待处理') {
                        var approveBtn = $('<button class="btn btn-success approve">批准</button>')
                            .data('id', request.id)
                            .data('request_type',request.request_type);
                        var rejectBtn = $('<button class="btn btn-danger reject">拒绝</button>')
                            .data('id', request.id)
                            .data('request_type',request.request_type);
                        actionsTd.append(approveBtn);
                        actionsTd.append(rejectBtn);
                    }
                    row.append(actionsTd);
                    tableBody.append(row);
                });
            },
            error: function(xhr) {
                console.error('获取请求列表出错:', xhr.responseText);
            }
        });
    }

    // 监听批准按钮的点击事件
    $('#requestsTableBody').on('click', '.approve', function() {
        var requestId = $(this).data('id');
        var requesType=$(this).data('request_type');
        processRequest(requestId, '同意',requesType);
        console.log('类型:', requesType);
    });

    // 监听拒绝按钮的点击事件
    $('#requestsTableBody').on('click', '.reject', function() {
        var requestId = $(this).data('id');//获取按钮的data-id属性值
        var requesType=$(this).data('request_type');
        processRequest(requestId, '拒绝',requesType);
    });

    function processRequest(requestId, action,requesType) {
        var note = prompt('请输入操作备注:');
        if (!note) return; // 如果用户取消输入或未输入内容，则不进行操作
        if (requesType=='借阅')
            var url = `/api/request_process/browse/${requestId}`;
        else if (requesType=='还书')
            var url = `/api/request_process/return/${requestId}`;
        console.log('url:', url);
        $.ajax({
            url: url,
            type: 'PUT',
            data: JSON.stringify({ action: action, note: note }),
            contentType: 'application/json',
            success: function(response) {
                alert(response.message);
                loadRequests(); // 刷新请求列表
            },
            error: function(xhr) {
                alert('操作失败');
                console.error('处理请求出错:', xhr.responseText);
            }
        });
    }
});
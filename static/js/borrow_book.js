$(document).ready(function() {
    loadBooks();

    // 监听搜索框输入以进行筛选
    $('#searchBox').on('keyup', function() {
        var searchValue = $(this).val().toLowerCase();
        filterBooks(searchValue);
    });

    // 监听图书列表项的点击事件以发起借阅申请
    $('#booksList').on('click', '.apply-btn', function() {
        var bookId = $(this).data('book-id');
        requestBorrowBook(bookId);
    });
});

// 加载书籍列表
function loadBooks() {
    $.ajax({
        url: '/api/books',
        type: 'GET',
        dataType: 'json',
        success: function(books) {
            renderBooks(books);
        },
        error: function(error) {
            console.error('获取图书列表出错:', error);
        }
    });
}

// 渲染书籍列表
function renderBooks(books) {
    var booksList = $('#booksList');
    booksList.empty(); // 清空现有内容

    books.forEach(function(book) {
        var bookItem = $('<li class="book-item list-group-item"></li>');
        bookItem.text(`${book.name} by ${book.authors} (ID: ${book.id})`);
        bookItem.data('book-id', book.id);
        // 添加申请借阅按钮
        var applyButton = $('<button class="btn btn-primary apply-btn">申请借阅</button>');
        applyButton.data('book-id', book.id);
        bookItem.append(applyButton);
        booksList.append(bookItem);
    });
}

// 筛选书籍列表
function filterBooks(searchValue) {
    $('#booksList .book-item').each(function() {
        var bookName = $(this).text().toLowerCase();
        $(this).toggle(bookName.indexOf(searchValue) > -1);
    });
}

// 发起借阅申请
function requestBorrowBook(bookId) {
    // 显示模态框
    $('#borrowModal').modal('show');
    // 将当前图书的 ID 存储在闭包变量中，以便在模态框提交时使用
    var currentBookId = bookId;
    $('#submitBorrowButton').on('click', function() {
        $('#borrowForm').submit(); // 触发表单的提交事件
    });
    $('#borrowModal').on('submit', '#borrowForm', function(e) {
        e.preventDefault(); // 阻止表单默认提交行为
        // 从模态框中获取申请理由
        var requestReason = $('#requestReason').val();
        // 隐藏模态框
        $('#borrowModal').modal('hide');
        // 发送 AJAX 请求提交借阅申请
        alert('借阅申请已提交，等待管理员审批');
        submitBorrowRequest(currentBookId, requestReason);

    });


}

// 提交借阅申请
function submitBorrowRequest(bookId, requestReason) {
    $.ajax({
        url: `/api/books_loans/request_borrow/${bookId}`,
        type: 'POST',
        data: JSON.stringify({ reason: requestReason }),
        contentType: 'application/json',
        success: function(response) {
            alert('借阅申请已提交，等待管理员审批');
            // 清空申请理由文本框
            $('#requestReason').val('');
            // 可以在这里添加逻辑，比如刷新页面或更新图书列表状态
        },
        error: function(xhr) {
            var errorText = JSON.parse(xhr.responseText).error;
            alert('申请失败：' + errorText);
        }
    });
}
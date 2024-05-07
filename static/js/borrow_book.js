$(document).ready(function() {
    loadBooks();

    // 监听搜索框输入以进行筛选
    $('#searchBox').on('keyup', function() {
        var searchValue = $(this).val().toLowerCase();
        filterBooks(searchValue);
    });

    // 监听图书列表项的点击事件以借阅图书
    $('#booksList').on('click', '.book-item', function() {
        var bookId = $(this).data('book-id');
        borrowBook(bookId, $(this));
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
        bookItem.append('<span class="badge badge-primary float-right">借阅</span>'); // 添加借阅按钮
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

// 借阅图书
function borrowBook(bookId, bookItem) {
    $.ajax({
        url: `/api/books_loans/borrow/${bookId}`,
        type: 'POST',
        success: function(response) {
            alert('借阅成功');
            bookItem.remove(); // 从列表中移除借阅的书籍项
        },
        error: function(xhr) {
             var errorText = JSON.parse(xhr.responseText).error;
            alert('借阅失败：' + errorText);
        }
    });
}
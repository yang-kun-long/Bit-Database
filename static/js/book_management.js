$(document).ready(function() {
    loadBooks();

    // 添加事件监听器以处理图书的删除
    $('#bookList').on('click', '.delete-book', function(e) {
        const bookId = $(this).data('id');
        if (confirm('确定要删除这本书吗?')) {
            $.ajax({
                url: `/api/books/${bookId}`,
                type: 'DELETE',
                success: function() {
                    loadBooks();
                },
                error: function(error) {
                    console.error('删除图书出错:', error);
                }
            });
        }
    });
});

function loadBooks() {
    $.ajax({
        url: '/api/books',
        type: 'GET',
        dataType: 'json',
        success: function(books) {
            const bookList = $('#bookList');
            bookList.empty(); // 清空现有内容

            books.forEach(function(book) {
                const bookItem = $('<div class="book-item">');
                bookItem.append(`<h4>${book.name}</h4>`);
                bookItem.append(`<p>作者: ${book.authors}</p>`);
                bookItem.append(`<p>出版年份: ${book.publish_year}</p>`);
                bookItem.append(`<div class="book-actions">`);
                bookItem.append(`<button class="btn btn-danger delete-book" data-id="${book.id}">删除</button>`);

                bookList.append(bookItem);
            });
        },
        error: function(error) {
            console.error('获取图书列表出错:', error);
        }
    });
}
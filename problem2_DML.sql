USE library;

INSERT INTO author (author_id, name, country) VALUES
(1, 'Naguib Mahfouz','Egypt'),
(2, 'Jane Austen','United Kingdom'),
(3, 'Gabriel Garcia','Colombia');

INSERT INTO book (book_id, title, price, author_id) VALUES
(1, 'Palace Walk', 15.50, 1),
(2, 'Midaq Alley', 12.00, 1),
(3, 'Pride and Prejudice', 9.99, 2),
(4, 'Emma', 11.25, 2),
(5, 'One Hundred Years of Solitude', 18.75, 3),
(6, 'Love in the Time of Cholera', 16.40, 3);

SELECT * FROM author;
SELECT * FROM book;

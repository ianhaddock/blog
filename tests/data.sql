
INSERT INTO user (username, password, email)
VALUES
    ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'test@example.com'),
    ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'other@example.com');

INSERT INTO post (title, body, author_id, created)
VALUES
     ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00'),
     ('test title 2', 'test 2' || x'0a' || 'body 2', 1, '2018-02-02 00:00:00');

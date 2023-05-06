DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    tfv_code VARCHAR(6)
);
INSERT INTO users (email, username, password) VALUES ('sudmit082@mail.ru', 'dima', 'pbkdf2:sha256:600000$WLlo4uTqXK2rxWnE$c227356f0291be82bbda5a8fcd47589edff320a506ab31850431e268d9dca95a');
INSERT INTO users (email, username, password) VALUES ('denis.ne.povs@gmail.com', 'danil', 'pbkdf2:sha256:600000$IhKogcPPcs1BIBsE$1d8bd9e9c439046070deac602184c923c0a13ff4216c349c6ba4755e7bf1a409');
INSERT INTO users (email, username, password) VALUES ('artem.skr456@gmail.com', 'artem', 'pbkdf2:sha256:600000$g97sRUNMAwQokCAv$ed0483d4d4cafe45a8a76d2d4c8603aa476bea1818ef015892f78fc700194e9f');
INSERT INTO users (email, username, password) VALUES ('something_special7@mail.ru', 'kostya', 'pbkdf2:sha256:600000$HM5n63I63oWEGzKh$a3bdf3a081c3afc7265fc110f24567e353dbf59080a8b0c3d658a8182683f0d9');
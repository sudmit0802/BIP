DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tfv CASCADE;
DROP TABLE IF EXISTS plans CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS deadlines CASCADE;

CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    tg_chat_id VARCHAR(15) UNIQUE
);

CREATE TABLE IF NOT EXISTS tfv (
    id SERIAL PRIMARY KEY,
    tfv_code VARCHAR(6),
    tfv_time TIMESTAMP,
    tfv_address VARCHAR(64),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    status VARCHAR(16) NOT NULL,
    group_id VARCHAR(16) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    plan_id INT NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS deadlines (
    id SERIAL PRIMARY KEY,
    deadline_time TIMESTAMP NOT NULL,
    deadline_status BOOLEAN NOT NULL,
    specifier VARCHAR(32) NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);


INSERT INTO users (email, username, password) VALUES ('sudmit082@mail.ru', 'dima', 'pbkdf2:sha256:600000$WLlo4uTqXK2rxWnE$c227356f0291be82bbda5a8fcd47589edff320a506ab31850431e268d9dca95a');
INSERT INTO users (email, username, password) VALUES ('123@mail.ru', 'danil', 'pbkdf2:sha256:600000$IhKogcPPcs1BIBsE$1d8bd9e9c439046070deac602184c923c0a13ff4216c349c6ba4755e7bf1a409');
INSERT INTO users (email, username, password) VALUES ('artem.skr456@gmail.com', 'artem', 'pbkdf2:sha256:600000$g97sRUNMAwQokCAv$ed0483d4d4cafe45a8a76d2d4c8603aa476bea1818ef015892f78fc700194e9f');
INSERT INTO users (email, username, password) VALUES ('something_special7@mail.ru', 'kostya', 'pbkdf2:sha256:600000$HM5n63I63oWEGzKh$a3bdf3a081c3afc7265fc110f24567e353dbf59080a8b0c3d658a8182683f0d9');

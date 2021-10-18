CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    api_key VARCHAR(100) NOT NULL,
    requests INTEGER NOT NULL DEFAULT 0,
    unsafe_requests INTEGER NOT NULL DEFAULT 0
);
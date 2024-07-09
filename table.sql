CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    first_name VARCHAR(70),
    last_name VARCHAR(70),
    username VARCHAR(200),
    phone_number VARCHAR(20),
    language VARCHAR(2), -- UZ, RU, EN
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ
);

CREATE TABLE appeals (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    appeal_text TEXT NOT NULL,
    file_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

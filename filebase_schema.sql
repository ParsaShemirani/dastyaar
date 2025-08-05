CREATE TABLE nodes (
    id BIGSERIAL PRIMARY KEY,
    type VARCHAR(30),
    created_ts TIMESTAMP
);

CREATE TABLE files (
    id BIGINT PRIMARY KEY REFERENCES nodes(id),
    root_name VARCHAR(160),
    version_number INTEGER,
    hash CHAR(64),
    extension VARCHAR(16),
    size BIGINT,
    created_ts TIMESTAMP,
    specific_metadata JSONB,
    description TEXT
);

CREATE TABLE collections (
    id BIGINT PRIMARY KEY REFERENCES nodes(id),
    name VARCHAR(160),
    description TEXT
);

CREATE TABLE storage_devices (
    id BIGINT PRIMARY KEY REFERENCES nodes(id),
    name VARCHAR(160),
    size BIGINT
);

CREATE TABLE relationships (
    source_id BIGINT REFERENCES nodes(id),
    target_id BIGINT REFERENCES nodes(id),
    type VARCHAR(50),
    created_ts TIMESTAMP,
    specific_metadata JSONB
);
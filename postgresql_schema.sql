CREATE TABLE files (
    id              SERIAL PRIMARY KEY,
    name            TEXT        NOT NULL,
    created_ts      TIMESTAMPTZ NOT NULL DEFAULT now(),
    ingested_ts     TIMESTAMPTZ,
    version_number  INTEGER,
    extension       TEXT,
    size            BIGINT,
    hash            CHAR(64)    NOT NULL,
    description     TEXT,
    description_tsv tsvector GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(description, ''))
    ) STORED,

    CONSTRAINT unique_file_name UNIQUE (name),
    CONSTRAINT unique_file_hash UNIQUE (hash)
);

CREATE TYPE grouping_type AS ENUM ('collection', 'version', 'proxy', 'take');
CREATE TABLE groupings (
    id              SERIAL PRIMARY KEY,
    name            TEXT,
    type            grouping_type,
    description     TEXT,
    description_tsv tsvector GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(description, ''))
    ) STORED
);

CREATE TABLE files_groupings (  
    file_id     INTEGER NOT NULL REFERENCES files(id),
    grouping_id INTEGER NOT NULL REFERENCES groupings(id),
    PRIMARY KEY (file_id, grouping_id)
);

CREATE TABLE locations (
    id   SERIAL PRIMARY KEY,
    name TEXT,
    path TEXT NOT NULL,
    CONSTRAINT unique_location_path UNIQUE (path)
);

CREATE TABLE files_locations (
    file_id     INTEGER NOT NULL REFERENCES files(id),
    location_id INTEGER NOT NULL REFERENCES locations(id),
    PRIMARY KEY (file_id, location_id)
);

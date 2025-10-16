CREATE OR REPLACE FUNCTION update_metadata()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = NOW() AT TIME ZONE 'UTC';
    NEW.updated_by = CURRENT_USER;
    RETURN NEW;
END
$$ language 'plpgsql';

CREATE TABLE versions(
    id UUID PRIMARY KEY,
    version TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_version 
BEFORE UPDATE ON versions 
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

CREATE TABLE scripts(
    name TEXT PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_scripts
BEFORE UPDATE ON scripts
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

INSERT INTO scripts(name) VALUES 
    ('LATIN'),
    ('CYRILLIC'),
    ('ARABIC'),
    ('GREEK');

CREATE TABLE languages(
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    script TEXT REFERENCES scripts(name) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_languages
BEFORE UPDATE ON languages
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

CREATE TABLE countries(
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_countries
BEFORE UPDATE ON countries
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

CREATE TABLE regions(
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    country UUID references countries(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_regions
BEFORE UPDATE ON regions
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

CREATE TABLE language_to_countries(
    country_id UUID NOT NULL,
    language_id UUID NOT NULL,
    official BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT language_to_country_unique UNIQUE(country_id, language_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_language_to_countries
BEFORE UPDATE ON language_to_countries
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

CREATE TABLE dialects(
    id UUID NOT NULL UNIQUE,
    name TEXT NOT NULL,
    language_id UUID REFERENCES languages(id) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    PRIMARY KEY(id, language_id)
);

CREATE TRIGGER update_dialects
BEFORE UPDATE ON dialects
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

-- Homophone case?
CREATE TABLE base_words(
    id UUID PRIMARY KEY,
    word TEXT NOT NULL,
    language_id UUID REFERENCES languages(id) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_base_words
BEFORE UPDATE ON base_words
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

CREATE TABLE word_variants(
    id UUID PRIMARY KEY,
    word TEXT NOT NULL,
    base_word UUID REFERENCES base_words(id),
    dialect UUID REFERENCES dialects(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_word_variants
BEFORE UPDATE ON word_variants
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

-- Split into requested variants and base words?
CREATE TABLE requested_words(
    id UUID PRIMARY KEY,
    word TEXT NOT NULL,
    variant TEXT,
    country UUID references countries(id) NOT NULL,
    region UUID references regions(id),
    requested_by TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_requested_words
BEFORE UPDATE ON requested_words
FOR EACH ROW EXECUTE PROCEDURE update_metadata();
-- PATH for regions? allows for a closed geometric path (Polygon type is similar)

CREATE TABLE users( -- Meant for contributors to the corpus
    id UUID PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    default_dialect UUID references dialects(id),
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_users 
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE update_metadata();

CREATE TABLE session_tokens(
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    token TEXT NOT NULL,
    expires TIMESTAMP NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    updated_by TEXT NOT NULL DEFAULT CURRENT_USER,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL
);

CREATE TRIGGER update_session_tokens
BEFORE UPDATE ON session_tokens
FOR EACH ROW EXECUTE PROCEDURE update_metadata();
CREATE TABLE IF NOT EXISTS tusee_encrypted_keys (
    uuid        character varying(200) NOT NULL,
    user       character varying(200),
    key       text,

    PRIMARY KEY (uuid)
)
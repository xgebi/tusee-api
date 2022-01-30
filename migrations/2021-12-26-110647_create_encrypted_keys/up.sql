CREATE TABLE IF NOT EXISTS tusee_encrypted_keys (
    key_uuid        character varying(200) NOT NULL,
    tusee_user       character varying(200) NOT NULL,
    key       text NOT NULL,

    PRIMARY KEY (key_uuid)
)
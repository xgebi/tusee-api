CREATE TABLE IF NOT EXISTS tusee_encrypted_keys (
    key_uuid        character varying(200) NOT NULL,
    tusee_user       character varying(200) NOT NULL,
    key       text NOT NULL,
    boardless   boolean NOT NULL DEFAULT FALSE,

    PRIMARY KEY (key_uuid),
    CONSTRAINT user_fkey FOREIGN KEY (tusee_user)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
CREATE TYPE tusee_access_types AS ENUM ('login', 'logout');

CREATE TABLE IF NOT EXISTS tusee_access_audit_log
(
    uuid        character varying(200) NOT NULL,
    tusee_user       character varying(200),
    ip       character varying(200),
    event tusee_access_types,

    PRIMARY KEY (uuid),
    CONSTRAINT user_fkey FOREIGN KEY (tusee_user)
        REFERENCES tusee_users (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
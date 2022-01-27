CREATE TABLE IF NOT EXISTS tusee_permissions_audit_log
(
    uuid        character varying(200) NOT NULL,
    tusee_user       character varying(200) NOT NULL,
    ip       character varying(200) NOT NULL,
    event character varying(100) NOT NULL CHECK (event IN ('WrongPermissions')),

    PRIMARY KEY (uuid),
    CONSTRAINT user_fkey FOREIGN KEY (tusee_user)
        REFERENCES tusee_users (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
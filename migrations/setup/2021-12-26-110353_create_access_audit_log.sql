CREATE TABLE IF NOT EXISTS tusee_access_audit_log
(
    entry_uuid        character varying(200) NOT NULL,
    tusee_user       character varying(200) NOT NULL,
    ip       character varying(200) NOT NULL,
    event character varying(100) NOT NULL CHECK (event IN ('Login', 'Logout')),

    PRIMARY KEY (entry_uuid),
    CONSTRAINT user_fkey FOREIGN KEY (tusee_user)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
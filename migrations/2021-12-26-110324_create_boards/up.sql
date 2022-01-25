CREATE TABLE IF NOT EXISTS tusee_boards
(
    uuid        character varying(200) NOT NULL,
    name        text DEFAULT '',
    description text DEFAULT '',
    owner       character varying(200) NOT NULL,

    PRIMARY KEY (uuid),
    CONSTRAINT user_fkey FOREIGN KEY (owner)
        REFERENCES tusee_users (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
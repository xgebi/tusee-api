CREATE TABLE IF NOT EXISTS tusee_boards
(
    uuid        character varying(200) NOT NULL,
    name        text,
    description text,
    owner       character varying(200),

    PRIMARY KEY (uuid),
    CONSTRAINT user_fkey FOREIGN KEY (owner)
        REFERENCES tusee_users (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS tusee_tasks
(
    uuid        character varying(200) NOT NULL,
    creator       character varying(200),
    board       character varying(200),
    description text,
    updated text,
    created text,

    PRIMARY KEY (uuid),
    CONSTRAINT creator_fkey FOREIGN KEY (creator)
        REFERENCES tusee_users (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_fkey FOREIGN KEY (board)
        REFERENCES tusee_boards (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
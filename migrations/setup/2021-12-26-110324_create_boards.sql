CREATE TABLE IF NOT EXISTS tusee_boards
(
    board_uuid  character varying(200) NOT NULL,
    name        text DEFAULT '',
    description text DEFAULT '',
    owner       character varying(200) NOT NULL,

    PRIMARY KEY (board_uuid),
    CONSTRAINT user_fkey FOREIGN KEY (owner)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
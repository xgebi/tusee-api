CREATE TABLE IF NOT EXISTS tusee_available_user_boards
(
    uuid        character varying(200) NOT NULL,
    tusee_user       character varying(200) NOT NULL,
    board       character varying(200) NOT NULL,

    PRIMARY KEY (uuid),
    CONSTRAINT user_fkey FOREIGN KEY (tusee_user)
        REFERENCES tusee_users (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT board_fkey FOREIGN KEY (board)
        REFERENCES tusee_boards (uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
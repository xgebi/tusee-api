CREATE TABLE IF NOT EXISTS tusee_available_user_boards
(
    board_uuid        character varying(200) NOT NULL,
    tusee_user       character varying(200) NOT NULL,
    board       character varying(200) NOT NULL,

    PRIMARY KEY (board_uuid),
    CONSTRAINT user_fkey FOREIGN KEY (tusee_user)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT board_fkey FOREIGN KEY (board)
        REFERENCES tusee_boards (board_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
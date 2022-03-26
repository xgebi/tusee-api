CREATE TABLE IF NOT EXISTS tusee_tasks
(
    task_uuid        character varying(200) NOT NULL,
    creator       character varying(200) NOT NULL,
    board       character varying(200) NOT NULL,
    description text NOT NULL,
    updated text NOT NULL,
    created text NOT NULL,

    PRIMARY KEY (task_uuid),
    CONSTRAINT creator_fkey FOREIGN KEY (creator)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_fkey FOREIGN KEY (board)
        REFERENCES tusee_boards (board_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
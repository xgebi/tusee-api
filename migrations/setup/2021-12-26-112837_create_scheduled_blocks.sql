CREATE TABLE IF NOT EXISTS tusee_scheduled_blocks
(
    block_uuid        character varying(200) NOT NULL,
    task       character varying(200) NOT NULL,
    start_time text NOT NULL,
    end_time text NOT NULL,

    PRIMARY KEY (block_uuid),
    CONSTRAINT task_fkey FOREIGN KEY (task)
        REFERENCES tusee_tasks (task_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
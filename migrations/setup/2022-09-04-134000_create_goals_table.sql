CREATE TABLE IF NOT EXISTS tusee_goals
(
    goal_uuid           character varying(200) NOT NULL,
    user_uuid           character varying(200) NOT NULL,
    goal                text,
    target_date         TIMESTAMP WITH TIME ZONE,
    added_date          TIMESTAMP WITH TIME ZONE NOT NULL,
    done_date           TIMESTAMP WITH TIME ZONE,
    done                BOOLEAN NOT NULL DEFAULT FALSE,

    PRIMARY KEY (goal_uuid),
    CONSTRAINT user_fkey FOREIGN KEY (user_uuid)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
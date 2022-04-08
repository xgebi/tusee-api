CREATE TABLE IF NOT EXISTS tusee_events
(
    event_uuid          character varying(200) NOT NULL,
    user_uuid           character varying(200) NOT NULL,
    name                character varying(200) NOT NULL,
    start_timedate      TIMESTAMP WITH TIME ZONE NOT NULL,
    end_timedate        TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY (event_uuid),
    CONSTRAINT user_fkey FOREIGN KEY (user_uuid)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
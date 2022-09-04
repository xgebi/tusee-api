CREATE TABLE IF NOT EXISTS tusee_statistics
(
    stat_uuid           character varying(200) NOT NULL,
    user_uuid           character varying(200) NOT NULL,
    stat_name           character varying(200) NOT NULL,
    stat_value          text NOT NULL,
    recorded_at         TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at         TIMESTAMP WITH TIME ZONE NOT NULL,
    stat_type           character varying(200) NOT NULL,
    note                text,

    PRIMARY KEY (stat_uuid),
    CONSTRAINT user_fkey FOREIGN KEY (user_uuid)
        REFERENCES tusee_users (user_uuid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
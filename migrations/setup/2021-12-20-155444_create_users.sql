-- Your SQL goes here
CREATE TABLE IF NOT EXISTS tusee_users (
    user_uuid character varying(200) NOT NULL PRIMARY KEY,
	display_name text NOT NULL DEFAULT 'human',
	password character varying(500) NOT NULL,
	email character varying(350) UNIQUE NOT NULL ,
	token character varying(350) NOT NULL DEFAULT '',
	expiry_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	first_login boolean NOT NULL DEFAULT TRUE,
	uses_totp boolean NOT NULL DEFAULT FALSE,
	totp_secret character varying(100)
)
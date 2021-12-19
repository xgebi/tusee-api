use postgres::{Client, Error, NoTls};
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct Config {
    db_host: String,
    db_port: u16,
    db_user: String,
    db_password: String,
    db_name: String,
}

pub(crate) fn create_database_connection() -> Client {
    match envy::from_env::<Config>() {
        Ok(config) => {
            let connection_string = format!("host={} port={} user={} password='{}' dbname={}",
                                            config.db_host, config.db_port.to_string(), config.db_user,
                                            config.db_password, config.db_name);
            let mut client = Client::connect(connection_string.as_str(), NoTls);
            match client {
                Ok(c) => { return c; }
                Err(error) => panic!("{:#?}", error)
            }
        },
        Err(error) => panic!("{:#?}", error)
    }
}

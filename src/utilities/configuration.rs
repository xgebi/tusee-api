use justconfig::{ Config, ConfPath, sources::text::ConfigText, sources::env::Env, sources::defaults::Defaults, processors::Explode, validators::Range, item::ValueExtractor };
use std::ffi::OsStr;
use std::fs::File;
use serde::Deserialize;

#[derive(Deserialize)]
pub(crate) struct Configuration {
    database: String,
    url: String,
    secret: String,
}

impl Configuration {
    pub(crate) fn new() -> Self {
        let mut conf = Config::default();
        let config_file = File::open("tusee.conf").expect("Could not open config file.");
        conf.add_source(ConfigText::new(config_file, "tusee.conf").expect("Loading configuration file failed."));

        Configuration {
            database: conf.get(conf.root().push("database")).value().unwrap(),
            url: conf.get(conf.root().push("url")).value().unwrap(),
            secret: conf.get(conf.root().push("secret")).value().unwrap(),
        }
    }

    pub(crate) fn get_database(&self) -> String {
        return self.database.clone();
    }

    pub(crate) fn get_url(&self) -> String {
        return self.url.clone();
    }

    pub(crate) fn get_secret(&self) -> String {
        return self.secret.clone();
    }
}
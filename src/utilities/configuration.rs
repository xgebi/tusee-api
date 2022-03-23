use justconfig::{ Config, ConfPath, sources::text::ConfigText, sources::env::Env, sources::defaults::Defaults, processors::Explode, validators::Range, item::ValueExtractor };
use std::ffi::OsStr;
use std::fs::File;
use serde::Deserialize;

#[derive(Deserialize, Clone)]
pub(crate) struct Configuration {
    database: String,
    url: String,
    fe_url: String,
    secret: String,
    cookie_secret: String,
}

impl Configuration {
    pub(crate) fn new() -> Self {
        let mut conf = Config::default();
        let config_file = File::open("tusee.conf").expect("Could not open config file.");
        conf.add_source(ConfigText::new(config_file, "tusee.conf").expect("Loading configuration file failed."));

        Configuration {
            database: conf.get(conf.root().push("database")).value().unwrap(),
            url: conf.get(conf.root().push("url")).value().unwrap(),
            fe_url: conf.get(conf.root().push("fe_url")).value().unwrap(),
            secret: conf.get(conf.root().push("secret")).value().unwrap(),
            cookie_secret: conf.get(conf.root().push("cookie_secret")).value().unwrap() // Probably should do a check so it's 16 characters :/
        }
    }

    pub(crate) fn get_database(&self) -> String {
        return self.database.clone();
    }

    pub(crate) fn get_url(&self) -> String {
        return self.url.clone();
    }

    pub(crate) fn get_fe_url(&self) -> String {
        return self.fe_url.clone();
    }

    pub(crate) fn get_secret(&self) -> String {
        return self.secret.clone();
    }

    pub(crate) fn get_cookie_secret(&self) -> String {
        return self.cookie_secret.clone();
    }
}
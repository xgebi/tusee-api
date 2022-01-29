#![allow(unused)]
#![allow(clippy::all)]
use crate::schema::tusee_users;
use serde::{Serialize, Deserialize};
use diesel::prelude::*;

#[derive(Queryable, Debug, Identifiable, Serialize)]
#[table_name = "tusee_users"]
#[primary_key(uuid)]
pub struct User {
    pub uuid: String,
    pub display_name: String,
    pub password: String,
    pub email: String,
    pub token: String,
    pub expiry_date: f64,
    pub(crate) first_login: bool,
}
use diesel::prelude::*;

#[derive(Queryable, Insertable)]
pub struct User {
    pub uuid: String,
    pub display_name: String,
    pub password: String,
    pub email: String,
    pub token: String,
    pub expiry_date: f64,
}